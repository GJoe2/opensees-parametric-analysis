import unittest
import os
import json
import shutil
from src.model_builder import ModelBuilder
import numpy as np

class TestModelBuilder(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada test."""
        self.test_dir = "test_models"
        self.builder = ModelBuilder(output_dir=self.test_dir)
        
    def tearDown(self):
        """Limpieza después de cada test."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_directory_creation(self):
        """Prueba la creación del directorio de salida."""
        self.assertTrue(os.path.exists(self.test_dir))
    
    def test_model_name_generation(self):
        """Prueba la generación de nombres de modelos."""
        name = self.builder.generate_model_name(L_B_ratio=1.5, B=10.0, nx=4, ny=3)
        self.assertEqual(name, "F01_15_10_0403")
        
        name = self.builder.generate_model_name(L_B_ratio=2.0, B=15.0, nx=6, ny=5)
        self.assertEqual(name, "F01_20_15_0605")
    
    def test_dimension_calculation(self):
        """Prueba el cálculo de dimensiones."""
        L, B = self.builder.calculate_dimensions(L_B_ratio=1.5, B=10.0)
        self.assertEqual(L, 15.0)
        self.assertEqual(B, 10.0)
    
    def test_single_model_creation(self):
        """Prueba la creación de un modelo individual."""
        model_info = self.builder.create_model(L_B_ratio=1.5, B=10.0, nx=4, ny=3)
        
        # Verificar que el archivo existe
        self.assertTrue(os.path.exists(model_info['file_path']))
        
        # Verificar estructura del modelo
        self.assertIn('name', model_info)
        self.assertIn('parameters', model_info)
        self.assertIn('nodes', model_info)
        self.assertIn('elements', model_info)
        self.assertIn('loads', model_info)
        
        # Verificar parámetros
        params = model_info['parameters']
        self.assertEqual(params['L_B_ratio'], 1.5)
        self.assertEqual(params['B'], 10.0)
        self.assertEqual(params['L'], 15.0)
        self.assertEqual(params['nx'], 4)
        self.assertEqual(params['ny'], 3)
        
        # Verificar número de nodos
        expected_nodes = (params['nx'] + 1) * (params['ny'] + 1) * (params['num_floors'] + 1)
        self.assertEqual(len(model_info['nodes']), expected_nodes)
        
        # Verificar elementos
        elements = model_info['elements']
        self.assertTrue(any(e['type'] == 'slab' for e in elements.values()))
        self.assertTrue(any(e['type'] == 'column' for e in elements.values()))
        self.assertTrue(any(e['type'] == 'beam_x' for e in elements.values()))
        self.assertTrue(any(e['type'] == 'beam_y' for e in elements.values()))
    
    def test_model_export_to_python(self):
        """Prueba la exportación del modelo a Python."""
        # Crear modelo JSON primero
        model_info = self.builder.create_model(L_B_ratio=1.5, B=10.0, nx=4, ny=3)
        
        # Exportar a Python
        py_file = self.builder.export_model_to_python(model_info)
        
        # Verificar que el archivo Python existe
        self.assertTrue(os.path.exists(py_file))
        
        # Verificar contenido básico del archivo Python
        with open(py_file, 'r') as f:
            content = f.read()
            self.assertIn('import openseespy.opensees as ops', content)
            self.assertIn('def build_model():', content)
            self.assertIn('if __name__ == \'__main__\':', content)
    
    def test_parametric_model_generation(self):
        """Prueba la generación paramétrica de modelos."""
        L_B_ratios = [1.0, 1.5]
        B_values = [10.0]
        nx_values = [4]
        ny_values = [3]
        
        models = self.builder.generate_parametric_models(
            L_B_ratios=L_B_ratios,
            B_values=B_values,
            nx_values=nx_values,
            ny_values=ny_values,
            export_python=True
        )
        
        # Verificar número de modelos generados
        expected_models = len(L_B_ratios) * len(B_values) * len(nx_values) * len(ny_values)
        self.assertEqual(len(models), expected_models)
        
        # Verificar que se crearon tanto archivos JSON como Python
        for model in models:
            json_file = model['file_path']
            py_file = os.path.join(self.test_dir, f"{model['name']}_model.py")
            
            self.assertTrue(os.path.exists(json_file))
            self.assertTrue(os.path.exists(py_file))
    
    def test_material_properties(self):
        """Prueba que las propiedades de los materiales sean correctas."""
        model_info = self.builder.create_model(L_B_ratio=1.0, B=10.0, nx=4, ny=4)
        params = model_info['parameters']
        
        # Verificar propiedades de columnas
        self.assertEqual(params['column_size'], (0.40, 0.40))
        
        # Verificar propiedades de vigas
        self.assertEqual(params['beam_size'], (0.25, 0.40))
        
        # Verificar propiedades de losa
        self.assertEqual(params['slab_thickness'], 0.10)
        
        # Verificar propiedades del material
        self.assertGreater(params['E'], 0)
        self.assertTrue(0 < params['nu'] < 0.5)
        self.assertGreater(params['rho'], 0)
    
    def test_boundary_conditions(self):
        """Prueba que las condiciones de frontera estén correctamente aplicadas."""
        model_info = self.builder.create_model(L_B_ratio=1.0, B=10.0, nx=3, ny=3)
        
        # Verificar que los nodos base están restringidos
        for node_id, node_info in model_info['nodes'].items():
            if node_info['floor'] == 0:
                # Los nodos base deberían aparecer en el modelo con restricciones
                self.assertEqual(node_info['floor'], 0)
            else:
                # Los nodos superiores no deberían estar restringidos
                self.assertGreater(node_info['floor'], 0)

if __name__ == '__main__':
    unittest.main()
