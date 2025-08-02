"""
Tests para VisualizationHelper - Helper de visualización con opstool.
Verifica la funcionalidad de manejo de visualizaciones y ODB.
"""

import unittest
import tempfile
import os
import shutil
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.visualization_helper import VisualizationHelper


class TestVisualizationHelper(unittest.TestCase):
    """Tests para la clase VisualizationHelper."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.temp_dir = tempfile.mkdtemp()
        self.results_dir = os.path.join(self.temp_dir, "results")
        os.makedirs(self.results_dir)
        
        self.viz_helper = VisualizationHelper(
            results_dir=self.results_dir,
            odb_tag=1
        )
    
    def tearDown(self):
        """Limpieza después de cada test."""
        shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test de inicialización del helper."""
        self.assertEqual(self.viz_helper.results_dir, self.results_dir)
        self.assertEqual(self.viz_helper.odb_tag, 1)
        self.assertIsNone(self.viz_helper._odb)
    
    def test_initialization_with_defaults(self):
        """Test de inicialización con valores por defecto."""
        helper = VisualizationHelper()
        
        self.assertEqual(helper.results_dir, "results")
        self.assertEqual(helper.odb_tag, 1)
        self.assertIsNone(helper._odb)
    
    @patch('opstool.post.CreateODB')
    def test_create_odb_if_needed_success(self, mock_create_odb):
        """Test de creación exitosa de ODB."""
        mock_odb = MagicMock()
        mock_create_odb.return_value = mock_odb
        
        # Crear ODB
        result = self.viz_helper.create_odb_if_needed()
        
        # Verificar resultado
        self.assertTrue(result)
        self.assertEqual(self.viz_helper._odb, mock_odb)
        mock_create_odb.assert_called_once_with(
            odb_tag=1,
            project_gauss_to_nodes="extrapolate"
        )
    
    @patch('opstool.post.CreateODB')
    def test_create_odb_if_needed_failure(self, mock_create_odb):
        """Test de manejo de errores al crear ODB."""
        mock_create_odb.side_effect = Exception("ODB creation failed")
        
        # Intentar crear ODB
        result = self.viz_helper.create_odb_if_needed()
        
        # Verificar que falló correctamente
        self.assertFalse(result)
        self.assertIsNone(self.viz_helper._odb)
    
    @patch('opstool.post.CreateODB')
    def test_create_odb_if_needed_already_exists(self, mock_create_odb):
        """Test cuando ODB ya existe."""
        # Configurar ODB existente
        existing_odb = MagicMock()
        self.viz_helper._odb = existing_odb
        
        # Intentar crear ODB
        result = self.viz_helper.create_odb_if_needed()
        
        # Verificar que no se creó uno nuevo
        self.assertTrue(result)
        self.assertEqual(self.viz_helper._odb, existing_odb)
        mock_create_odb.assert_not_called()
    
    def test_capture_response_step_no_odb(self):
        """Test de captura de respuesta sin ODB."""
        result = self.viz_helper.capture_response_step()
        
        self.assertFalse(result)
    
    def test_capture_response_step_success(self):
        """Test de captura exitosa de respuesta."""
        # Configurar ODB mock
        mock_odb = MagicMock()
        mock_odb.fetch_response_step.return_value = None
        self.viz_helper._odb = mock_odb
        
        # Capturar respuesta
        result = self.viz_helper.capture_response_step()
        
        # Verificar resultado
        self.assertTrue(result)
        mock_odb.fetch_response_step.assert_called_once()
    
    def test_capture_response_step_failure(self):
        """Test de manejo de errores al capturar respuesta."""
        # Configurar ODB mock con error
        mock_odb = MagicMock()
        mock_odb.fetch_response_step.side_effect = Exception("Fetch failed")
        self.viz_helper._odb = mock_odb
        
        # Intentar capturar respuesta
        result = self.viz_helper.capture_response_step()
        
        # Verificar que falló correctamente
        self.assertFalse(result)
    
    def test_save_responses_no_odb(self):
        """Test de guardado de respuestas sin ODB."""
        result = self.viz_helper.save_responses()
        
        self.assertFalse(result)
    
    def test_save_responses_success(self):
        """Test de guardado exitoso de respuestas."""
        # Configurar ODB mock
        mock_odb = MagicMock()
        mock_odb.save_response_step.return_value = None
        self.viz_helper._odb = mock_odb
        
        # Guardar respuestas
        result = self.viz_helper.save_responses()
        
        # Verificar resultado
        self.assertTrue(result)
        mock_odb.save_response_step.assert_called_once()
    
    def test_save_responses_failure(self):
        """Test de manejo de errores al guardar respuestas."""
        # Configurar ODB mock con error
        mock_odb = MagicMock()
        mock_odb.save_response_step.side_effect = Exception("Save failed")
        self.viz_helper._odb = mock_odb
        
        # Intentar guardar respuestas
        result = self.viz_helper.save_responses()
        
        # Verificar que falló correctamente
        self.assertFalse(result)
    
    @patch('opstool.post.CreateModeShapeODB')
    def test_create_modal_odb_if_needed_success(self, mock_create_modal_odb):
        """Test de creación exitosa de ODB modal."""
        mock_modal_odb = MagicMock()
        mock_create_modal_odb.return_value = mock_modal_odb
        
        # Crear ODB modal
        result = self.viz_helper.create_modal_odb_if_needed()
        
        # Verificar resultado
        self.assertTrue(result)
        mock_create_modal_odb.assert_called_once_with(
            odb_tag=1,
            mode_tags="all"
        )
    
    @patch('opstool.post.CreateModeShapeODB')
    def test_create_modal_odb_if_needed_failure(self, mock_create_modal_odb):
        """Test de manejo de errores al crear ODB modal."""
        mock_create_modal_odb.side_effect = Exception("Modal ODB creation failed")
        
        # Intentar crear ODB modal
        result = self.viz_helper.create_modal_odb_if_needed()
        
        # Verificar que falló correctamente
        self.assertFalse(result)
    
    @patch('os.path.exists')
    def test_generate_static_deformed_plot_file_not_exists(self, mock_exists):
        """Test cuando el archivo de visualización no existe."""
        mock_exists.return_value = False
        
        result = self.viz_helper.generate_static_deformed_plot("test_model")
        
        self.assertFalse(result)
    
    @patch('os.path.exists')
    @patch('opstool.vis.plotly.deformed_shape')
    def test_generate_static_deformed_plot_success(self, mock_deformed_shape, mock_exists):
        """Test de generación exitosa de gráfico deformado."""
        mock_exists.return_value = True
        mock_fig = MagicMock()
        mock_deformed_shape.return_value = mock_fig
        
        # Configurar ODB
        mock_odb = MagicMock()
        self.viz_helper._odb = mock_odb
        
        # Generar gráfico
        result = self.viz_helper.generate_static_deformed_plot("test_model")
        
        # Verificar resultado
        self.assertTrue(result)
        mock_deformed_shape.assert_called_once()
        mock_fig.write_html.assert_called_once()
    
    @patch('os.path.exists')
    @patch('opstool.vis.plotly.deformed_shape')
    def test_generate_static_deformed_plot_failure(self, mock_deformed_shape, mock_exists):
        """Test de manejo de errores al generar gráfico deformado."""
        mock_exists.return_value = True
        mock_deformed_shape.side_effect = Exception("Plot generation failed")
        
        # Configurar ODB
        mock_odb = MagicMock()
        self.viz_helper._odb = mock_odb
        
        # Intentar generar gráfico
        result = self.viz_helper.generate_static_deformed_plot("test_model")
        
        # Verificar que falló correctamente
        self.assertFalse(result)
    
    @patch('os.path.exists')
    def test_generate_mode_shapes_plot_file_not_exists(self, mock_exists):
        """Test cuando el archivo de formas modales no existe."""
        mock_exists.return_value = False
        
        result = self.viz_helper.generate_mode_shapes_plot("test_model", 3)
        
        self.assertFalse(result)
    
    @patch('os.path.exists')
    @patch('opstool.vis.plotly.mode_shape')
    def test_generate_mode_shapes_plot_success(self, mock_mode_shape, mock_exists):
        """Test de generación exitosa de gráfico de formas modales."""
        mock_exists.return_value = True
        mock_fig = MagicMock()
        mock_mode_shape.return_value = mock_fig
        
        # Generar gráfico
        result = self.viz_helper.generate_mode_shapes_plot("test_model", 3)
        
        # Verificar resultado
        self.assertTrue(result)
        self.assertEqual(mock_mode_shape.call_count, 3)  # 3 modos
        self.assertEqual(mock_fig.write_html.call_count, 3)  # 3 archivos HTML
    
    def test_clean_up_odb(self):
        """Test de limpieza de ODB."""
        # Configurar ODB
        mock_odb = MagicMock()
        self.viz_helper._odb = mock_odb
        
        # Limpiar
        self.viz_helper.clean_up_odb()
        
        # Verificar que se limpió
        self.assertIsNone(self.viz_helper._odb)


if __name__ == '__main__':
    unittest.main()
