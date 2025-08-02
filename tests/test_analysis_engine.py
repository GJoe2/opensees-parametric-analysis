"""
Tests para AnalysisEngine - Motor principal de análisis.
Verifica la funcionalidad correcta del motor refactorizado.
"""

import unittest
import tempfile
import os
import json
import shutil
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.analysis_engine import AnalysisEngine


class TestAnalysisEngine(unittest.TestCase):
    """Tests para la clase AnalysisEngine."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.temp_dir = tempfile.mkdtemp()
        self.models_dir = os.path.join(self.temp_dir, "models")
        self.results_dir = os.path.join(self.temp_dir, "results")
        os.makedirs(self.models_dir)
        
        # Crear modelo de prueba
        self.test_model = {
            "name": "test_model",
            "nodes": {
                "1": {"coords": [0, 0, 0], "floor": 0},
                "2": {"coords": [0, 0, 3], "floor": 1}
            },
            "elements": {
                "1": {
                    "type": "ElasticBeamColumn",
                    "nodes": [1, 2],
                    "section": "W18X35",
                    "transformation": "Linear"
                }
            },
            "materials": {
                "Steel": {
                    "type": "Steel01",
                    "Fy": 250000000,
                    "E0": 200000000000,
                    "b": 0.003
                }
            },
            "sections": {
                "W18X35": {
                    "type": "WFSection2d",
                    "material": "Steel",
                    "d": 0.4445,
                    "tw": 0.00599,
                    "bf": 0.15399,
                    "tf": 0.00940
                }
            },
            "constraints": {
                "1": [1, 1, 1, 1, 1, 1]
            },
            "loads": {
                "static": {
                    "2": [100, 0, 0, 0, 0, 0]
                }
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
                    "enabled": False
                }
            }
        }
        
        # Guardar modelo de prueba
        self.model_file = os.path.join(self.models_dir, "test_model.json")
        with open(self.model_file, 'w') as f:
            json.dump(self.test_model, f)
    
    def tearDown(self):
        """Limpieza después de cada test."""
        shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test de inicialización del motor."""
        engine = AnalysisEngine(self.models_dir, self.results_dir)
        
        self.assertEqual(engine.models_dir, self.models_dir)
        self.assertEqual(engine.results_dir, self.results_dir)
        self.assertTrue(os.path.exists(self.results_dir))
    
    def test_load_model_from_file(self):
        """Test de carga de modelo desde archivo."""
        engine = AnalysisEngine(self.models_dir, self.results_dir)
        loaded_model = engine.load_model_from_file(self.model_file)
        
        self.assertEqual(loaded_model['name'], 'test_model')
        self.assertIn('nodes', loaded_model)
        self.assertIn('elements', loaded_model)
        self.assertIn('analysis_config', loaded_model)
    
    def test_load_nonexistent_file(self):
        """Test de manejo de archivos inexistentes."""
        engine = AnalysisEngine(self.models_dir, self.results_dir)
        
        with self.assertRaises(FileNotFoundError):
            engine.load_model_from_file("nonexistent.json")
    
    @patch('openseespy.opensees.wipe')
    @patch('openseespy.opensees.model')
    @patch('openseespy.opensees.node')
    def test_build_model_in_opensees(self, mock_node, mock_model, mock_wipe):
        """Test de construcción del modelo en OpenSees."""
        engine = AnalysisEngine(self.models_dir, self.results_dir)
        
        # Ejecutar construcción
        engine.build_model_in_opensees(self.test_model)
        
        # Verificar que se llamaron las funciones OpenSees
        mock_wipe.assert_called_once()
        mock_model.assert_called_once_with('basic', '-ndm', 3, '-ndf', 6)
        self.assertEqual(mock_node.call_count, 2)  # 2 nodos
    
    @patch('src.analysis_engine.StaticAnalysis')
    def test_run_static_analysis(self, mock_static_class):
        """Test de ejecución de análisis estático."""
        # Configurar mock
        mock_static = MagicMock()
        mock_static.run.return_value = {'success': True, 'max_displacement': 0.001}
        mock_static_class.return_value = mock_static
        
        engine = AnalysisEngine(self.models_dir, self.results_dir)
        
        # Ejecutar análisis
        results = engine.run_static_analysis(self.test_model)
        
        # Verificar resultados
        self.assertIsInstance(results, dict)
        mock_static_class.assert_called_once_with(self.test_model)
        mock_static.run.assert_called_once()
    
    @patch('src.analysis_engine.ModalAnalysis')
    def test_run_modal_analysis(self, mock_modal_class):
        """Test de ejecución de análisis modal."""
        # Agregar configuración modal al modelo
        self.test_model['analysis_config']['modal'] = {
            "system": "ProfileSPD",
            "solver": "frequency",
            "num_modes": 5
        }
        
        # Configurar mock
        mock_modal = MagicMock()
        mock_modal.run.return_value = {
            'success': True, 
            'frequencies': [1.0, 2.0, 3.0],
            'periods': [1.0, 0.5, 0.33]
        }
        mock_modal_class.return_value = mock_modal
        
        engine = AnalysisEngine(self.models_dir, self.results_dir)
        
        # Ejecutar análisis
        results = engine.run_modal_analysis(self.test_model)
        
        # Verificar resultados
        self.assertIsInstance(results, dict)
        self.assertTrue(results['success'])
        mock_modal_class.assert_called_once_with(self.test_model)
        mock_modal.run.assert_called_once()
    
    @patch('src.analysis_engine.DynamicAnalysis')
    def test_run_dynamic_analysis(self, mock_dynamic_class):
        """Test de ejecución de análisis dinámico."""
        # Agregar configuración dinámica al modelo
        self.test_model['analysis_config']['dynamic'] = {
            "system": "ProfileSPD",
            "integrator": "Newmark",
            "dt": 0.01,
            "total_time": 10.0
        }
        
        # Configurar mock
        mock_dynamic = MagicMock()
        mock_dynamic.run.return_value = {
            'success': True,
            'max_displacement': 0.005,
            'time_steps': 1000
        }
        mock_dynamic_class.return_value = mock_dynamic
        
        engine = AnalysisEngine(self.models_dir, self.results_dir)
        
        # Ejecutar análisis
        results = engine.run_dynamic_analysis(self.test_model)
        
        # Verificar resultados
        self.assertIsInstance(results, dict)
        self.assertTrue(results['success'])
        mock_dynamic_class.assert_called_once_with(self.test_model)
        mock_dynamic.run.assert_called_once()
    
    def test_save_results(self):
        """Test de guardado de resultados."""
        engine = AnalysisEngine(self.models_dir, self.results_dir)
        
        test_results = {
            'model': 'test_model',
            'static': {'success': True, 'max_displacement': 0.001},
            'modal': {'success': True, 'frequencies': [1.0, 2.0]}
        }
        
        # Guardar resultados
        engine.save_results('test_model', test_results)
        
        # Verificar que se guardó el archivo
        results_file = os.path.join(self.results_dir, "test_model_results.json")
        self.assertTrue(os.path.exists(results_file))
        
        # Verificar contenido
        with open(results_file, 'r') as f:
            saved_results = json.load(f)
        
        self.assertEqual(saved_results['model'], 'test_model')
        self.assertIn('static', saved_results)
        self.assertIn('modal', saved_results)
    
    def test_process_single_model_success(self):
        """Test de procesamiento exitoso de un modelo individual."""
        engine = AnalysisEngine(self.models_dir, self.results_dir)
        
        with patch.object(engine, 'build_model_in_opensees'), \
             patch.object(engine, 'run_static_analysis') as mock_static, \
             patch.object(engine, 'save_results') as mock_save:
            
            mock_static.return_value = {'success': True, 'max_displacement': 0.001}
            
            # Procesar modelo
            results = engine.process_single_model(self.model_file)
            
            # Verificar resultados
            self.assertIsInstance(results, dict)
            self.assertEqual(results['model'], 'test_model')
            mock_static.assert_called_once()
            mock_save.assert_called_once()
    
    def test_process_single_model_error_handling(self):
        """Test de manejo de errores durante procesamiento."""
        engine = AnalysisEngine(self.models_dir, self.results_dir)
        
        # Test con archivo inexistente
        with self.assertRaises(FileNotFoundError):
            engine.process_single_model("nonexistent.json")


if __name__ == '__main__':
    unittest.main()
