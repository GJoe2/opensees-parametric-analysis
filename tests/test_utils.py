"""
Tests para ModelBuilderHelpers - helpers de conveniencia para ModelBuilder.
Verifica la funcionalidad correcta de los métodos de conveniencia.
"""

import unittest
import tempfile
import os
import shutil
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.model_helpers import ModelBuilderHelpers, create_model_helpers
from src.utils.model_helpers import create_static_only_model, create_modal_only_model, create_complete_model


class TestModelBuilderHelpers(unittest.TestCase):
    """Tests para la clase ModelBuilderHelpers."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Mock del ModelBuilder
        self.mock_builder = MagicMock()
        self.mock_builder.create_model.return_value = {
            'name': 'test_model',
            'success': True,
            'file_path': os.path.join(self.temp_dir, 'test_model.json')
        }
        
        # Crear helpers con mock
        self.helpers = ModelBuilderHelpers(self.mock_builder)
    
    def tearDown(self):
        """Limpieza después de cada test."""
        shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test de inicialización de ModelBuilderHelpers."""
        self.assertEqual(self.helpers.builder, self.mock_builder)
    
    def test_create_static_only_model(self):
        """Test de creación de modelo solo estático."""
        # Ejecutar método
        result = self.helpers.create_static_only_model(
            L_B_ratio=2.0,
            B=10.0,
            nx=3,
            ny=3,
            model_name="static_test",
            steps=15,
            visualize=True
        )
        
        # Verificar resultado
        self.assertIsInstance(result, dict)
        self.assertTrue(result['success'])
        
        # Verificar llamada al builder
        self.mock_builder.create_model.assert_called_once()
        call_args = self.mock_builder.create_model.call_args
        
        # Verificar parámetros geométricos
        self.assertEqual(call_args[0][0], 2.0)  # L_B_ratio
        self.assertEqual(call_args[0][1], 10.0)  # B
        self.assertEqual(call_args[0][2], 3)     # nx
        self.assertEqual(call_args[0][3], 3)     # ny
        self.assertEqual(call_args[0][4], "static_test")  # model_name
        
        # Verificar análisis habilitados
        kwargs = call_args[1]
        self.assertEqual(kwargs['enabled_analyses'], ['static'])
        
        # Verificar parámetros de análisis
        analysis_params = kwargs['analysis_params']
        self.assertEqual(analysis_params['static']['steps'], 15)
        self.assertTrue(analysis_params['visualization']['enabled'])
    
    def test_create_static_only_model_defaults(self):
        """Test de creación de modelo estático con valores por defecto."""
        result = self.helpers.create_static_only_model(
            L_B_ratio=1.5,
            B=8.0,
            nx=2,
            ny=2
        )
        
        # Verificar que se usaron los defaults
        call_args = self.mock_builder.create_model.call_args
        kwargs = call_args[1]
        
        # Verificar parámetros por defecto
        analysis_params = kwargs['analysis_params']
        self.assertEqual(analysis_params['static']['steps'], 10)
        self.assertFalse(analysis_params['visualization']['enabled'])
    
    def test_create_modal_only_model(self):
        """Test de creación de modelo solo modal."""
        result = self.helpers.create_modal_only_model(
            L_B_ratio=1.8,
            B=12.0,
            nx=4,
            ny=4,
            model_name="modal_test",
            num_modes=8,
            visualize=True
        )
        
        # Verificar resultado
        self.assertIsInstance(result, dict)
        self.assertTrue(result['success'])
        
        # Verificar llamada al builder
        call_args = self.mock_builder.create_model.call_args
        kwargs = call_args[1]
        
        # Verificar análisis habilitados
        self.assertEqual(kwargs['enabled_analyses'], ['modal'])
        
        # Verificar parámetros de análisis
        analysis_params = kwargs['analysis_params']
        self.assertEqual(analysis_params['modal']['num_modes'], 8)
        self.assertTrue(analysis_params['visualization']['enabled'])
    
    def test_create_dynamic_model(self):
        """Test de creación de modelo dinámico (estático + dinámico)."""
        result = self.helpers.create_dynamic_model(
            L_B_ratio=2.2,
            B=15.0,
            nx=5,
            ny=3,
            model_name="dynamic_test",
            dt=0.005,
            total_time=20.0
        )
        
        # Verificar llamada al builder
        call_args = self.mock_builder.create_model.call_args
        kwargs = call_args[1]
        
        # Verificar análisis habilitados
        self.assertEqual(kwargs['enabled_analyses'], ['static', 'dynamic'])
        
        # Verificar parámetros dinámicos
        analysis_params = kwargs['analysis_params']
        self.assertEqual(analysis_params['dynamic']['dt'], 0.005)
        self.assertEqual(analysis_params['dynamic']['total_time'], 20.0)
    
    def test_create_complete_model(self):
        """Test de creación de modelo completo (todos los análisis)."""
        result = self.helpers.create_complete_model(
            L_B_ratio=1.6,
            B=9.0,
            nx=3,
            ny=4,
            model_name="complete_test",
            visualize=True
        )
        
        # Verificar llamada al builder
        call_args = self.mock_builder.create_model.call_args
        kwargs = call_args[1]
        
        # Verificar que se habilitaron todos los análisis
        enabled_analyses = kwargs['enabled_analyses']
        self.assertIn('static', enabled_analyses)
        self.assertIn('modal', enabled_analyses)
        self.assertIn('dynamic', enabled_analyses)
        
        # Verificar visualización
        analysis_params = kwargs['analysis_params']
        self.assertTrue(analysis_params['visualization']['enabled'])
    
    def test_create_quick_prototype(self):
        """Test de creación de prototipo rápido."""
        result = self.helpers.create_quick_prototype(
            L_B_ratio=2.0,
            B=6.0
        )
        
        # Verificar llamada al builder con parámetros mínimos
        call_args = self.mock_builder.create_model.call_args
        
        # Verificar que se usaron valores por defecto para nx, ny
        self.assertEqual(call_args[0][2], 2)  # nx default
        self.assertEqual(call_args[0][3], 2)  # ny default
        
        # Verificar configuración minimalista
        kwargs = call_args[1]
        analysis_params = kwargs['analysis_params']
        self.assertEqual(analysis_params['static']['steps'], 5)
        self.assertEqual(analysis_params['modal']['num_modes'], 3)
        self.assertFalse(analysis_params['visualization']['enabled'])


class TestGlobalConvenienceFunctions(unittest.TestCase):
    """Tests para las funciones de conveniencia globales."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Limpieza después de cada test."""
        shutil.rmtree(self.temp_dir)
    
    @patch('src.utils.model_helpers.create_model_helpers')
    def test_create_static_only_model_global(self, mock_create_helpers):
        """Test de función global create_static_only_model."""
        # Configurar mock
        mock_helpers = MagicMock()
        mock_helpers.create_static_only_model.return_value = {'success': True}
        mock_create_helpers.return_value = mock_helpers
        
        # Llamar función global
        result = create_static_only_model(
            L_B_ratio=1.5,
            B=8.0,
            nx=3,
            ny=3,
            output_dir=self.temp_dir,
            model_name="global_static"
        )
        
        # Verificar resultado
        self.assertTrue(result['success'])
        
        # Verificar que se crearon los helpers correctamente
        mock_create_helpers.assert_called_once_with(self.temp_dir)
        
        # Verificar que se llamó el método correcto
        mock_helpers.create_static_only_model.assert_called_once_with(
            1.5, 8.0, 3, 3, model_name="global_static"
        )
    
    @patch('src.utils.model_helpers.create_model_helpers')
    def test_create_modal_only_model_global(self, mock_create_helpers):
        """Test de función global create_modal_only_model."""
        # Configurar mock
        mock_helpers = MagicMock()
        mock_helpers.create_modal_only_model.return_value = {'success': True}
        mock_create_helpers.return_value = mock_helpers
        
        # Llamar función global
        result = create_modal_only_model(
            L_B_ratio=2.0,
            B=10.0,
            nx=4,
            ny=2,
            output_dir=self.temp_dir,
            num_modes=6
        )
        
        # Verificar resultado
        self.assertTrue(result['success'])
        
        # Verificar llamadas
        mock_create_helpers.assert_called_once_with(self.temp_dir)
        mock_helpers.create_modal_only_model.assert_called_once_with(
            2.0, 10.0, 4, 2, num_modes=6
        )
    
    @patch('src.utils.model_helpers.create_model_helpers')
    def test_create_complete_model_global(self, mock_create_helpers):
        """Test de función global create_complete_model."""
        # Configurar mock
        mock_helpers = MagicMock()
        mock_helpers.create_complete_model.return_value = {'success': True}
        mock_create_helpers.return_value = mock_helpers
        
        # Llamar función global
        result = create_complete_model(
            L_B_ratio=1.8,
            B=12.0,
            nx=5,
            ny=3,
            output_dir=self.temp_dir
        )
        
        # Verificar resultado
        self.assertTrue(result['success'])
        
        # Verificar llamadas
        mock_create_helpers.assert_called_once_with(self.temp_dir)
        mock_helpers.create_complete_model.assert_called_once_with(
            1.8, 12.0, 5, 3
        )
    
    @patch('src.utils.model_helpers.ModelBuilder')
    def test_create_model_helpers_function(self, mock_model_builder_class):
        """Test de función create_model_helpers."""
        # Configurar mock
        mock_builder_instance = MagicMock()
        mock_model_builder_class.return_value = mock_builder_instance
        
        # Llamar función
        helpers = create_model_helpers(self.temp_dir)
        
        # Verificar que se creó ModelBuilder correctamente
        mock_model_builder_class.assert_called_once_with(output_dir=self.temp_dir)
        
        # Verificar que se retornó ModelBuilderHelpers
        self.assertIsInstance(helpers, ModelBuilderHelpers)
        self.assertEqual(helpers.builder, mock_builder_instance)
    
    @patch('src.utils.model_helpers.ModelBuilder')
    def test_create_model_helpers_default_dir(self, mock_model_builder_class):
        """Test de create_model_helpers con directorio por defecto."""
        mock_builder_instance = MagicMock()
        mock_model_builder_class.return_value = mock_builder_instance
        
        # Llamar función sin especificar directorio
        helpers = create_model_helpers()
        
        # Verificar que se usó el directorio por defecto
        mock_model_builder_class.assert_called_once_with(output_dir="models")


if __name__ == '__main__':
    unittest.main()
