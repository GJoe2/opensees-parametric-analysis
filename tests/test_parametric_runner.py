"""
Tests para ParametricRunner - Runner de estudios paramétricos.
Verifica la funcionalidad correcta del runner paramétrico.
"""

import unittest
import tempfile
import os
import json
import shutil
from unittest.mock import patch, MagicMock
import pandas as pd

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.parametric_runner import ParametricRunner


class TestParametricRunner(unittest.TestCase):
    """Tests para la clase ParametricRunner."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.temp_dir = tempfile.mkdtemp()
        self.results_dir = os.path.join(self.temp_dir, "results")
        self.output_dir = os.path.join(self.temp_dir, "output")
        os.makedirs(self.results_dir)
        os.makedirs(self.output_dir)
        
        # Crear runner
        self.runner = ParametricRunner(
            results_dir=self.results_dir,
            output_dir=self.output_dir
        )
        
        # Datos de parámetros de prueba
        self.test_parameters = {
            'L_B_ratio': [1.5, 2.0, 2.5],
            'B': [8.0, 10.0, 12.0],
            'nx': [2, 3],
            'ny': [2, 3]
        }
        
        # Resultados de modelos simulados
        self.mock_results = {
            'model_1_5_8_0_2_2': {
                'static': {'success': True, 'max_displacement': 0.001},
                'modal': {'success': True, 'frequencies': [1.5, 3.2, 5.1]}
            },
            'model_2_0_10_0_3_3': {
                'static': {'success': True, 'max_displacement': 0.0008},
                'modal': {'success': True, 'frequencies': [1.8, 3.5, 5.4]}
            }
        }
    
    def tearDown(self):
        """Limpieza después de cada test."""
        shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test de inicialización del runner."""
        self.assertEqual(self.runner.results_dir, self.results_dir)
        self.assertEqual(self.runner.output_dir, self.output_dir)
        self.assertTrue(os.path.exists(self.results_dir))
        self.assertTrue(os.path.exists(self.output_dir))
    
    def test_initialization_with_defaults(self):
        """Test de inicialización con valores por defecto."""
        runner = ParametricRunner()
        
        self.assertEqual(runner.results_dir, "results")
        self.assertEqual(runner.output_dir, "parametric_output")
    
    def test_generate_parameter_combinations(self):
        """Test de generación de combinaciones de parámetros."""
        combinations = self.runner.generate_parameter_combinations(self.test_parameters)
        
        # Verificar que se generaron todas las combinaciones
        expected_count = 3 * 3 * 2 * 2  # 36 combinaciones
        self.assertEqual(len(combinations), expected_count)
        
        # Verificar estructura de una combinación
        first_combo = combinations[0]
        self.assertIn('L_B_ratio', first_combo)
        self.assertIn('B', first_combo)
        self.assertIn('nx', first_combo)
        self.assertIn('ny', first_combo)
        
        # Verificar valores están en rangos esperados
        for combo in combinations:
            self.assertIn(combo['L_B_ratio'], [1.5, 2.0, 2.5])
            self.assertIn(combo['B'], [8.0, 10.0, 12.0])
            self.assertIn(combo['nx'], [2, 3])
            self.assertIn(combo['ny'], [2, 3])
    
    def test_generate_parameter_combinations_single_values(self):
        """Test con parámetros de un solo valor."""
        single_params = {
            'L_B_ratio': [2.0],
            'B': [10.0],
            'nx': [3],
            'ny': [3]
        }
        
        combinations = self.runner.generate_parameter_combinations(single_params)
        
        self.assertEqual(len(combinations), 1)
        self.assertEqual(combinations[0]['L_B_ratio'], 2.0)
        self.assertEqual(combinations[0]['B'], 10.0)
    
    def test_create_model_name(self):
        """Test de creación de nombres de modelos."""
        params = {'L_B_ratio': 1.5, 'B': 8.0, 'nx': 2, 'ny': 3}
        
        name = self.runner.create_model_name(params)
        
        # Verificar formato esperado
        self.assertEqual(name, "model_1_5_8_0_2_3")
    
    def test_create_model_name_with_prefix(self):
        """Test de creación de nombres con prefijo personalizado."""
        params = {'L_B_ratio': 2.0, 'B': 10.0, 'nx': 3, 'ny': 3}
        
        name = self.runner.create_model_name(params, prefix="test")
        
        self.assertEqual(name, "test_2_0_10_0_3_3")
    
    @patch('src.parametric_runner.ModelBuilder')
    def test_run_single_model_success(self, mock_model_builder_class):
        """Test de ejecución exitosa de un modelo individual."""
        # Configurar mock del ModelBuilder
        mock_builder = MagicMock()
        mock_builder.create_model.return_value = {
            'success': True,
            'file_path': '/path/to/model.json'
        }
        mock_model_builder_class.return_value = mock_builder
        
        # Configurar mock del AnalysisEngine
        with patch('src.parametric_runner.AnalysisEngine') as mock_engine_class:
            mock_engine = MagicMock()
            mock_engine.process_single_model.return_value = {
                'static': {'success': True, 'max_displacement': 0.001}
            }
            mock_engine_class.return_value = mock_engine
            
            # Ejecutar modelo
            params = {'L_B_ratio': 1.5, 'B': 8.0, 'nx': 2, 'ny': 2}
            result = self.runner.run_single_model(params)
            
            # Verificar resultado
            self.assertIsInstance(result, dict)
            self.assertIn('model_name', result)
            self.assertIn('parameters', result)
            self.assertIn('results', result)
            
            # Verificar que se llamaron los métodos correctos
            mock_builder.create_model.assert_called_once()
            mock_engine.process_single_model.assert_called_once()
    
    @patch('src.parametric_runner.ModelBuilder')
    def test_run_single_model_creation_failure(self, mock_model_builder_class):
        """Test de manejo de falla en creación de modelo."""
        # Configurar mock para falla
        mock_builder = MagicMock()
        mock_builder.create_model.return_value = {
            'success': False,
            'error': 'Model creation failed'
        }
        mock_model_builder_class.return_value = mock_builder
        
        # Ejecutar modelo
        params = {'L_B_ratio': 1.5, 'B': 8.0, 'nx': 2, 'ny': 2}
        result = self.runner.run_single_model(params)
        
        # Verificar que se manejó la falla
        self.assertFalse(result['results']['success'])
        self.assertIn('error', result['results'])
    
    def test_run_parametric_study_small_batch(self):
        """Test de estudio paramétrico con lote pequeño."""
        # Usar solo 2 combinaciones para test rápido
        small_params = {
            'L_B_ratio': [1.5, 2.0],
            'B': [8.0],
            'nx': [2],
            'ny': [2]
        }
        
        with patch.object(self.runner, 'run_single_model') as mock_run_single:
            # Configurar retornos del mock
            mock_run_single.side_effect = [
                {
                    'model_name': 'model_1_5_8_0_2_2',
                    'parameters': {'L_B_ratio': 1.5, 'B': 8.0, 'nx': 2, 'ny': 2},
                    'results': {'static': {'success': True, 'max_displacement': 0.001}}
                },
                {
                    'model_name': 'model_2_0_8_0_2_2',
                    'parameters': {'L_B_ratio': 2.0, 'B': 8.0, 'nx': 2, 'ny': 2},
                    'results': {'static': {'success': True, 'max_displacement': 0.0008}}
                }
            ]
            
            # Ejecutar estudio
            summary = self.runner.run_parametric_study(
                parameters=small_params,
                study_name="test_study"
            )
            
            # Verificar resultados
            self.assertIsInstance(summary, dict)
            self.assertEqual(summary['total_models'], 2)
            self.assertEqual(summary['successful_models'], 2)
            self.assertEqual(summary['failed_models'], 0)
            
            # Verificar que se ejecutaron todos los modelos
            self.assertEqual(mock_run_single.call_count, 2)
    
    def test_create_results_dataframe(self):
        """Test de creación de DataFrame de resultados."""
        # Crear datos de resultados simulados
        results_data = [
            {
                'model_name': 'model_1_5_8_0_2_2',
                'parameters': {'L_B_ratio': 1.5, 'B': 8.0, 'nx': 2, 'ny': 2},
                'results': {
                    'static': {'success': True, 'max_displacement': 0.001},
                    'modal': {'success': True, 'frequencies': [1.5, 3.2]}
                }
            },
            {
                'model_name': 'model_2_0_10_0_3_3',
                'parameters': {'L_B_ratio': 2.0, 'B': 10.0, 'nx': 3, 'ny': 3},
                'results': {
                    'static': {'success': True, 'max_displacement': 0.0008},
                    'modal': {'success': True, 'frequencies': [1.8, 3.5]}
                }
            }
        ]
        
        # Crear DataFrame
        df = self.runner.create_results_dataframe(results_data)
        
        # Verificar estructura
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        
        # Verificar columnas principales
        self.assertIn('model_name', df.columns)
        self.assertIn('L_B_ratio', df.columns)
        self.assertIn('B', df.columns)
        self.assertIn('nx', df.columns)
        self.assertIn('ny', df.columns)
        
        # Verificar columnas de resultados
        self.assertIn('static_success', df.columns)
        self.assertIn('static_max_displacement', df.columns)
        self.assertIn('modal_success', df.columns)
        self.assertIn('modal_frequency_1', df.columns)
        
        # Verificar valores
        self.assertEqual(df.iloc[0]['L_B_ratio'], 1.5)
        self.assertEqual(df.iloc[0]['static_max_displacement'], 0.001)
        self.assertEqual(df.iloc[1]['modal_frequency_1'], 1.8)
    
    def test_save_results_summary(self):
        """Test de guardado de resumen de resultados."""
        summary = {
            'study_name': 'test_study',
            'total_models': 4,
            'successful_models': 3,
            'failed_models': 1,
            'parameters': self.test_parameters,
            'timestamp': '2024-01-01 12:00:00'
        }
        
        # Guardar resumen
        file_path = self.runner.save_results_summary(summary, "test_study")
        
        # Verificar que se guardó el archivo
        self.assertTrue(os.path.exists(file_path))
        
        # Verificar contenido
        with open(file_path, 'r') as f:
            saved_summary = json.load(f)
        
        self.assertEqual(saved_summary['study_name'], 'test_study')
        self.assertEqual(saved_summary['total_models'], 4)
        self.assertEqual(saved_summary['successful_models'], 3)
    
    def test_save_results_dataframe(self):
        """Test de guardado de DataFrame de resultados."""
        # Crear DataFrame de prueba
        df = pd.DataFrame({
            'model_name': ['model_1', 'model_2'],
            'L_B_ratio': [1.5, 2.0],
            'B': [8.0, 10.0],
            'static_max_displacement': [0.001, 0.0008]
        })
        
        # Guardar DataFrame
        file_path = self.runner.save_results_dataframe(df, "test_study")
        
        # Verificar que se guardó el archivo
        self.assertTrue(os.path.exists(file_path))
        
        # Verificar contenido
        loaded_df = pd.read_csv(file_path)
        self.assertEqual(len(loaded_df), 2)
        self.assertEqual(list(loaded_df['model_name']), ['model_1', 'model_2'])
    
    def test_filter_successful_results(self):
        """Test de filtrado de resultados exitosos."""
        results_data = [
            {
                'model_name': 'model_1',
                'results': {'static': {'success': True}, 'modal': {'success': True}}
            },
            {
                'model_name': 'model_2',
                'results': {'static': {'success': False}, 'modal': {'success': True}}
            },
            {
                'model_name': 'model_3',
                'results': {'static': {'success': True}, 'modal': {'success': False}}
            }
        ]
        
        # Filtrar solo resultados completamente exitosos
        successful = self.runner.filter_successful_results(results_data)
        
        # Verificar filtrado
        self.assertEqual(len(successful), 1)
        self.assertEqual(successful[0]['model_name'], 'model_1')
    
    def test_calculate_study_statistics(self):
        """Test de cálculo de estadísticas del estudio."""
        results_data = [
            {
                'results': {
                    'static': {'success': True, 'max_displacement': 0.001},
                    'modal': {'success': True, 'frequencies': [1.5, 3.2]}
                }
            },
            {
                'results': {
                    'static': {'success': True, 'max_displacement': 0.002},
                    'modal': {'success': True, 'frequencies': [1.8, 3.5]}
                }
            },
            {
                'results': {
                    'static': {'success': False},
                    'modal': {'success': False}
                }
            }
        ]
        
        # Calcular estadísticas
        stats = self.runner.calculate_study_statistics(results_data)
        
        # Verificar estadísticas
        self.assertEqual(stats['total_models'], 3)
        self.assertEqual(stats['successful_models'], 2)
        self.assertEqual(stats['failed_models'], 1)
        self.assertAlmostEqual(stats['success_rate'], 66.67, places=1)
        
        # Verificar estadísticas de desplazamientos
        self.assertEqual(stats['static_analysis']['successful'], 2)
        self.assertEqual(stats['static_analysis']['max_displacement_range']['min'], 0.001)
        self.assertEqual(stats['static_analysis']['max_displacement_range']['max'], 0.002)


if __name__ == '__main__':
    unittest.main()
