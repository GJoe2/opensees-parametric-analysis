"""
Tests para clases de análisis específicos - StaticAnalysis, ModalAnalysis, DynamicAnalysis.
Verifica la funcionalidad correcta de cada tipo de análisis.
"""

import unittest
import tempfile
import os
import shutil
from unittest.mock import patch, MagicMock
import numpy as np

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.analysis_types import BaseAnalysis, StaticAnalysis, ModalAnalysis, DynamicAnalysis


class TestBaseAnalysis(unittest.TestCase):
    """Tests para la clase BaseAnalysis."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.test_model_data = {
            "name": "test_model",
            "nodes": {
                "1": {"coords": [0, 0, 0], "floor": 0},
                "2": {"coords": [0, 0, 3], "floor": 1},
                "3": {"coords": [3, 0, 3], "floor": 1}
            },
            "analysis_config": {
                "static": {
                    "system": "ProfileSPD",
                    "numberer": "RCM",
                    "constraints": "Plain",
                    "algorithm": "Linear",
                    "analysis": "Static"
                }
            }
        }
    
    def test_initialization(self):
        """Test de inicialización de BaseAnalysis."""
        analysis = BaseAnalysis(self.test_model_data)
        
        self.assertEqual(analysis.model_data, self.test_model_data)
        self.assertEqual(analysis.model_name, "test_model")
    
    @patch('openseespy.opensees.system')
    @patch('openseespy.opensees.numberer')
    @patch('openseespy.opensees.constraints')
    @patch('openseespy.opensees.algorithm')
    @patch('openseespy.opensees.analysis')
    def test_setup_opensees_analysis(self, mock_analysis, mock_algorithm, 
                                   mock_constraints, mock_numberer, mock_system):
        """Test de configuración de análisis OpenSees."""
        analysis = BaseAnalysis(self.test_model_data)
        config = self.test_model_data['analysis_config']['static']
        
        analysis.setup_opensees_analysis(config)
        
        mock_system.assert_called_once_with("ProfileSPD")
        mock_numberer.assert_called_once_with("RCM")
        mock_constraints.assert_called_once_with("Plain")
        mock_algorithm.assert_called_once_with("Linear")
        mock_analysis.assert_called_once_with("Static")
    
    @patch('openseespy.opensees.nodeDisp')
    def test_get_max_displacement(self, mock_node_disp):
        """Test de cálculo de desplazamiento máximo."""
        # Configurar retornos del mock
        mock_node_disp.side_effect = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Nodo 1 (base)
            [0.01, 0.02, 0.0, 0.0, 0.0, 0.0],  # Nodo 2
            [0.015, 0.025, 0.0, 0.0, 0.0, 0.0]  # Nodo 3
        ]
        
        analysis = BaseAnalysis(self.test_model_data)
        max_disp = analysis.get_max_displacement()
        
        # Verificar que se calculó correctamente
        expected_max = np.sqrt(0.015**2 + 0.025**2)  # Nodo 3 tiene mayor desplazamiento
        self.assertAlmostEqual(max_disp, expected_max, places=6)
        
        # Verificar que solo se consultaron nodos superiores (floor > 0)
        self.assertEqual(mock_node_disp.call_count, 2)


class TestStaticAnalysis(unittest.TestCase):
    """Tests para la clase StaticAnalysis."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.test_model_data = {
            "name": "static_test_model",
            "nodes": {
                "1": {"coords": [0, 0, 0], "floor": 0},
                "2": {"coords": [0, 0, 3], "floor": 1}
            },
            "analysis_config": {
                "static": {
                    "system": "ProfileSPD",
                    "numberer": "RCM",
                    "constraints": "Plain",
                    "algorithm": "Linear",
                    "analysis": "Static",
                    "integrator": "LoadControl",
                    "steps": 10
                },
                "visualization": {
                    "enabled": True,
                    "static_deformed": True
                }
            }
        }
    
    @patch('openseespy.opensees.analyze')
    @patch('openseespy.opensees.integrator')
    def test_run_success_without_visualization(self, mock_integrator, mock_analyze):
        """Test de ejecución exitosa sin visualización."""
        # Configurar retornos exitosos
        mock_analyze.return_value = 0  # Éxito
        
        # Deshabilitar visualización
        self.test_model_data['analysis_config']['visualization']['enabled'] = False
        
        analysis = StaticAnalysis(self.test_model_data)
        
        with patch.object(analysis, 'setup_opensees_analysis'), \
             patch.object(analysis, 'get_max_displacement', return_value=0.001):
            
            results = analysis.run()
        
        # Verificar resultados
        self.assertTrue(results['success'])
        self.assertEqual(results['max_displacement'], 0.001)
        self.assertFalse(results['responses_available'])
        
        # Verificar llamadas a OpenSees
        mock_integrator.assert_called_once_with("LoadControl", 0.1)  # 1.0/10 steps
        self.assertEqual(mock_analyze.call_count, 10)
    
    @patch('openseespy.opensees.analyze')
    @patch('openseespy.opensees.integrator')
    def test_run_success_with_visualization(self, mock_integrator, mock_analyze):
        """Test de ejecución exitosa con visualización."""
        # Configurar retornos exitosos
        mock_analyze.return_value = 0  # Éxito
        
        # Crear mock del helper de visualización
        mock_viz_helper = MagicMock()
        mock_viz_helper.create_odb_if_needed.return_value = True
        mock_viz_helper.capture_response_step.return_value = True
        mock_viz_helper.save_responses.return_value = True
        
        analysis = StaticAnalysis(self.test_model_data)
        
        with patch.object(analysis, 'setup_opensees_analysis'), \
             patch.object(analysis, 'get_max_displacement', return_value=0.002):
            
            results = analysis.run(viz_helper=mock_viz_helper)
        
        # Verificar resultados
        self.assertTrue(results['success'])
        self.assertEqual(results['max_displacement'], 0.002)
        self.assertTrue(results['responses_available'])
        
        # Verificar llamadas al helper
        mock_viz_helper.create_odb_if_needed.assert_called_once()
        mock_viz_helper.save_responses.assert_called_once()
    
    @patch('openseespy.opensees.analyze')
    def test_run_analysis_failure(self, mock_analyze):
        """Test de manejo de falla en el análisis."""
        # Configurar falla
        mock_analyze.return_value = -1  # Falla
        
        analysis = StaticAnalysis(self.test_model_data)
        
        with patch.object(analysis, 'setup_opensees_analysis'):
            results = analysis.run()
        
        # Verificar que se manejó la falla
        self.assertFalse(results['success'])
        self.assertEqual(results['error'], 'Analysis failed to converge')
        self.assertFalse(results['responses_available'])


class TestModalAnalysis(unittest.TestCase):
    """Tests para la clase ModalAnalysis."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.test_model_data = {
            "name": "modal_test_model",
            "nodes": {
                "1": {"coords": [0, 0, 0], "floor": 0},
                "2": {"coords": [0, 0, 3], "floor": 1}
            },
            "analysis_config": {
                "modal": {
                    "system": "ProfileSPD",
                    "solver": "frequency",
                    "num_modes": 3
                },
                "visualization": {
                    "enabled": True,
                    "mode_shapes": True
                }
            }
        }
    
    @patch('openseespy.opensees.eigen')
    def test_run_success(self, mock_eigen):
        """Test de ejecución exitosa de análisis modal."""
        # Configurar eigenvalores
        mock_eigen.return_value = [39.478, 157.914, 354.808]  # λ = (2πf)²
        
        analysis = ModalAnalysis(self.test_model_data)
        
        with patch.object(analysis, 'setup_opensees_analysis'):
            results = analysis.run()
        
        # Verificar resultados
        self.assertTrue(results['success'])
        self.assertEqual(len(results['frequencies']), 3)
        self.assertEqual(len(results['periods']), 3)
        
        # Verificar cálculos (aproximados)
        expected_freq_1 = np.sqrt(39.478) / (2 * np.pi)
        self.assertAlmostEqual(results['frequencies'][0], expected_freq_1, places=3)
        
        expected_period_1 = 1.0 / expected_freq_1
        self.assertAlmostEqual(results['periods'][0], expected_period_1, places=3)
    
    @patch('openseespy.opensees.eigen')
    def test_run_with_visualization(self, mock_eigen):
        """Test con visualización de formas modales."""
        mock_eigen.return_value = [39.478, 157.914, 354.808]
        
        # Crear mock del helper de visualización
        mock_viz_helper = MagicMock()
        mock_viz_helper.create_modal_odb_if_needed.return_value = True
        mock_viz_helper.generate_mode_shapes_plot.return_value = True
        
        analysis = ModalAnalysis(self.test_model_data)
        
        with patch.object(analysis, 'setup_opensees_analysis'):
            results = analysis.run(viz_helper=mock_viz_helper)
        
        # Verificar que se usó el helper
        mock_viz_helper.create_modal_odb_if_needed.assert_called_once()
        mock_viz_helper.generate_mode_shapes_plot.assert_called_once()
    
    @patch('openseespy.opensees.eigen')
    def test_run_eigenvalue_failure(self, mock_eigen):
        """Test de manejo de falla en cálculo de eigenvalores."""
        # Configurar falla
        mock_eigen.side_effect = Exception("Eigenvalue computation failed")
        
        analysis = ModalAnalysis(self.test_model_data)
        
        with patch.object(analysis, 'setup_opensees_analysis'):
            results = analysis.run()
        
        # Verificar que se manejó la falla
        self.assertFalse(results['success'])
        self.assertIn('error', results)


class TestDynamicAnalysis(unittest.TestCase):
    """Tests para la clase DynamicAnalysis."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.test_model_data = {
            "name": "dynamic_test_model",
            "nodes": {
                "1": {"coords": [0, 0, 0], "floor": 0},
                "2": {"coords": [0, 0, 3], "floor": 1}
            },
            "analysis_config": {
                "dynamic": {
                    "system": "ProfileSPD",
                    "numberer": "RCM",
                    "constraints": "Plain",
                    "algorithm": "Newton",
                    "analysis": "Transient",
                    "integrator": "Newmark",
                    "dt": 0.01,
                    "total_time": 1.0
                },
                "visualization": {
                    "enabled": False
                }
            }
        }
    
    @patch('openseespy.opensees.analyze')
    @patch('openseespy.opensees.integrator')
    def test_run_success(self, mock_integrator, mock_analyze):
        """Test de ejecución exitosa de análisis dinámico."""
        # Configurar retornos exitosos
        mock_analyze.return_value = 0  # Éxito
        
        analysis = DynamicAnalysis(self.test_model_data)
        
        with patch.object(analysis, 'setup_opensees_analysis'), \
             patch.object(analysis, 'get_max_displacement', return_value=0.005):
            
            results = analysis.run()
        
        # Verificar resultados
        self.assertTrue(results['success'])
        self.assertEqual(results['max_displacement'], 0.005)
        self.assertEqual(results['time_steps'], 100)  # 1.0 / 0.01
        
        # Verificar llamadas a OpenSees
        mock_integrator.assert_called_once_with("Newmark", 0.5, 0.25)
        self.assertEqual(mock_analyze.call_count, 100)  # total_time / dt
    
    @patch('openseespy.opensees.analyze')
    def test_run_convergence_failure(self, mock_analyze):
        """Test de manejo de falla de convergencia."""
        # Configurar falla parcial
        mock_analyze.side_effect = [0, 0, -1, 0]  # Falla en el 3er paso
        
        analysis = DynamicAnalysis(self.test_model_data)
        
        with patch.object(analysis, 'setup_opensees_analysis'):
            results = analysis.run()
        
        # Verificar que se completó parcialmente
        self.assertFalse(results['success'])
        self.assertIn('error', results)
        self.assertIn('convergence', results['error'].lower())
    
    def test_run_missing_config(self):
        """Test con configuración dinámica faltante."""
        # Eliminar configuración dinámica
        del self.test_model_data['analysis_config']['dynamic']
        
        analysis = DynamicAnalysis(self.test_model_data)
        results = analysis.run()
        
        # Verificar que se manejó la falta de configuración
        self.assertTrue(results['skipped'])
        self.assertFalse(results['success'])


if __name__ == '__main__':
    unittest.main()
