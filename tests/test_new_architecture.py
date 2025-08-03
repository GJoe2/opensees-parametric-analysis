"""
Tests for the new improved ModelBuilder architecture.

These tests verify that the new domain objects and specialized builders
work correctly and provide better functionality than the original implementation.
"""

import unittest
import os
import tempfile
import shutil
from typing import Dict, Any

# Import the new architecture components
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from domain import StructuralModel, Geometry, Node, Element, Sections, Section, Loads, Load, AnalysisConfig
from builders import GeometryBuilder, SectionsBuilder, LoadsBuilder, AnalysisConfigBuilder
from model_builder_v2 import ModelBuilder


class TestDomainObjects(unittest.TestCase):
    """Test domain objects functionality."""
    
    def test_node_creation(self):
        """Test Node object creation and validation."""
        node = Node(tag=1, coords=[0.0, 0.0, 0.0], floor=0, grid_pos=(0, 0))
        
        self.assertEqual(node.tag, 1)
        self.assertEqual(node.coords, [0.0, 0.0, 0.0])
        self.assertEqual(node.floor, 0)
        self.assertEqual(node.grid_pos, (0, 0))
        
        # Test validation
        with self.assertRaises(ValueError):
            Node(tag=1, coords=[0.0, 0.0], floor=0)  # Wrong coordinate dimensions
        
        with self.assertRaises(ValueError):
            Node(tag=1, coords=[0.0, 0.0, 0.0], floor=-1)  # Negative floor
    
    def test_element_creation(self):
        """Test Element object creation and validation."""
        element = Element(
            tag=1,
            element_type='column',
            nodes=[1, 2],
            floor=0,
            section_tag=1
        )
        
        self.assertEqual(element.tag, 1)
        self.assertEqual(element.element_type, 'column')
        self.assertEqual(element.nodes, [1, 2])
        self.assertEqual(element.floor, 0)
        self.assertEqual(element.section_tag, 1)
        
        # Test validation
        with self.assertRaises(ValueError):
            Element(tag=1, element_type='column', nodes=[], floor=0, section_tag=1)  # Empty nodes
    
    def test_geometry_methods(self):
        """Test Geometry object methods."""
        # Create test nodes
        nodes = {
            1: Node(1, [0.0, 0.0, 0.0], 0, (0, 0)),
            2: Node(2, [5.0, 0.0, 0.0], 0, (1, 0)),
            3: Node(3, [0.0, 5.0, 0.0], 0, (0, 1)),
            4: Node(4, [5.0, 5.0, 0.0], 0, (1, 1)),
            5: Node(5, [0.0, 0.0, 3.0], 1, (0, 0)),
            6: Node(6, [5.0, 0.0, 3.0], 1, (1, 0))
        }
        
        # Create test elements
        elements = {
            1: Element(1, 'column', [1, 5], 0, 1),
            2: Element(2, 'column', [2, 6], 0, 1)
        }
        
        geometry = Geometry(
            nodes=nodes,
            elements=elements,
            L=5.0,
            B=5.0,
            nx=1,
            ny=1,
            num_floors=1,
            floor_height=3.0
        )
        
        # Test methods
        self.assertEqual(geometry.get_total_height(), 3.0)
        self.assertEqual(geometry.get_footprint_area(), 25.0)
        self.assertEqual(geometry.get_aspect_ratio(), 1.0)
        
        # Test floor nodes
        floor_0_nodes = geometry.get_floor_nodes(0)
        self.assertEqual(len(floor_0_nodes), 4)
        
        floor_1_nodes = geometry.get_floor_nodes(1)
        self.assertEqual(len(floor_1_nodes), 2)
        
        # Test boundary nodes
        boundary_nodes = geometry.get_boundary_nodes()
        self.assertEqual(len(boundary_nodes), 6)  # All nodes are on boundary for 1x1 grid
        
        # Test elements by type
        columns = geometry.get_elements_by_type('column')
        self.assertEqual(len(columns), 2)


class TestBuilders(unittest.TestCase):
    """Test specialized builders."""
    
    def test_geometry_builder(self):
        """Test GeometryBuilder functionality."""
        geometry = GeometryBuilder.create(
            L_B_ratio=2.0,
            B=10.0,
            nx=2,
            ny=1,
            num_floors=2,
            floor_height=3.0
        )
        
        self.assertEqual(geometry.L, 20.0)  # 2.0 * 10.0
        self.assertEqual(geometry.B, 10.0)
        self.assertEqual(geometry.nx, 2)
        self.assertEqual(geometry.ny, 1)
        self.assertEqual(geometry.num_floors, 2)
        self.assertEqual(geometry.floor_height, 3.0)
        
        # Check node count: (nx+1) * (ny+1) * (num_floors+1) = 3 * 2 * 3 = 18
        expected_nodes = (2 + 1) * (1 + 1) * (2 + 1)
        self.assertEqual(len(geometry.nodes), expected_nodes)
        
        # Check that elements were created
        self.assertGreater(len(geometry.elements), 0)
        
        # Check element types
        columns = geometry.get_elements_by_type('column')
        beams_x = geometry.get_elements_by_type('beam_x')
        beams_y = geometry.get_elements_by_type('beam_y')
        slabs = geometry.get_elements_by_type('slab')
        
        # For 2x1 grid with 2 floors:
        # Columns: (nx+1) * (ny+1) * num_floors = 3 * 2 * 2 = 12
        # Beams X: nx * (ny+1) * num_floors = 2 * 2 * 2 = 8
        # Beams Y: (nx+1) * ny * num_floors = 3 * 1 * 2 = 6
        # Slabs: nx * ny * num_floors = 2 * 1 * 2 = 4
        self.assertEqual(len(columns), 12)
        self.assertEqual(len(beams_x), 8)
        self.assertEqual(len(beams_y), 6)
        self.assertEqual(len(slabs), 4)
    
    def test_sections_builder(self):
        """Test SectionsBuilder functionality."""
        fixed_params = {
            'column_size': (0.40, 0.40),
            'beam_size': (0.25, 0.40),
            'slab_thickness': 0.10
        }
        
        sections = SectionsBuilder.create(fixed_params)
        
        # Check that sections were created
        self.assertEqual(len(sections.sections), 3)  # slab, column, beam
        self.assertEqual(len(sections.transformations), 2)  # column and beam transformations
        
        # Check specific sections
        slab_section = sections.get_section_by_tag(1)
        self.assertIsNotNone(slab_section)
        self.assertEqual(slab_section.element_type, 'slab')
        self.assertEqual(slab_section.thickness, 0.10)
        
        column_section = sections.get_section_by_tag(2)
        self.assertIsNotNone(column_section)
        self.assertEqual(column_section.element_type, 'column')
        self.assertEqual(column_section.size, (0.40, 0.40))
        
        beam_section = sections.get_section_by_tag(3)
        self.assertIsNotNone(beam_section)
        self.assertEqual(beam_section.element_type, 'beam')
        self.assertEqual(beam_section.size, (0.25, 0.40))
    
    def test_loads_builder(self):
        """Test LoadsBuilder functionality."""
        # Create a simple geometry
        geometry = GeometryBuilder.create(
            L_B_ratio=1.0,
            B=5.0,
            nx=1,
            ny=1,
            num_floors=1,
            floor_height=3.0
        )
        
        loads = LoadsBuilder.create(
            geometry=geometry,
            load_params={'distributed_load': 2.0}
        )
        
        # Check that loads were created
        self.assertGreater(len(loads.loads), 0)
        
        # All loads should be on the top floor
        for load in loads.loads.values():
            corresponding_node = geometry.nodes[load.node_tag]
            self.assertEqual(corresponding_node.floor, geometry.num_floors)
        
        # Check load properties
        first_load = next(iter(loads.loads.values()))
        self.assertEqual(first_load.load_type, 'distributed_load')
        self.assertEqual(first_load.value, -2.0)  # Negative for downward
        self.assertEqual(first_load.direction, 'Z')
    
    def test_analysis_config_builder(self):
        """Test AnalysisConfigBuilder functionality."""
        config = AnalysisConfigBuilder.create(
            enabled_analyses=['static', 'modal'],
            analysis_params={
                'static': {'steps': 15},
                'modal': {'num_modes': 8},
                'visualization': {'enabled': True}
            }
        )
        
        self.assertEqual(config.enabled_analyses, ['static', 'modal'])
        self.assertTrue(config.is_enabled('static'))
        self.assertTrue(config.is_enabled('modal'))
        self.assertFalse(config.is_enabled('dynamic'))
        
        # Check specific configurations
        self.assertIsNotNone(config.static_config)
        self.assertEqual(config.static_config.steps, 15)
        
        self.assertIsNotNone(config.modal_config)
        self.assertEqual(config.modal_config.num_modes, 8)
        
        self.assertIsNone(config.dynamic_config)  # Not enabled
        
        self.assertTrue(config.visualization_config.enabled)


class TestNewModelBuilder(unittest.TestCase):
    """Test the new ModelBuilder implementation."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.builder = ModelBuilder(output_dir=self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_basic_model_creation(self):
        """Test basic model creation."""
        model = self.builder.create_model(
            L_B_ratio=1.5,
            B=10.0,
            nx=3,
            ny=2
        )
        
        self.assertIsInstance(model, StructuralModel)
        self.assertEqual(model.geometry.L, 15.0)  # 1.5 * 10.0
        self.assertEqual(model.geometry.B, 10.0)
        self.assertEqual(model.analysis_config.enabled_analyses, ['static', 'modal'])  # Default
        
        # Check that file was created
        expected_file = os.path.join(self.temp_dir, f"{model.name}.json")
        self.assertTrue(os.path.exists(expected_file))
    
    def test_model_with_custom_analysis(self):
        """Test model creation with custom analysis parameters."""
        model = self.builder.create_model(
            L_B_ratio=2.0,
            B=8.0,
            nx=2,
            ny=2,
            enabled_analyses=['static', 'modal', 'dynamic'],
            analysis_params={
                'modal': {'num_modes': 12},
                'dynamic': {'dt': 0.005},
                'visualization': {'enabled': True}
            }
        )
        
        self.assertEqual(model.analysis_config.enabled_analyses, ['static', 'modal', 'dynamic'])
        self.assertEqual(model.analysis_config.modal_config.num_modes, 12)
        self.assertEqual(model.analysis_config.dynamic_config.dt, 0.005)
        self.assertTrue(model.analysis_config.visualization_config.enabled)
    
    def test_multiple_models_creation(self):
        """Test creating multiple models."""
        parameter_sets = [
            {'L_B_ratio': 1.0, 'B': 8.0, 'nx': 2, 'ny': 2},
            {'L_B_ratio': 1.5, 'B': 10.0, 'nx': 3, 'ny': 2},
            {'L_B_ratio': 2.0, 'B': 12.0, 'nx': 4, 'ny': 3}
        ]
        
        models = self.builder.create_multiple_models(parameter_sets)
        
        self.assertEqual(len(models), 3)
        for model in models:
            self.assertIsInstance(model, StructuralModel)
            
            # Check that files were created
            expected_file = os.path.join(self.temp_dir, f"{model.name}.json")
            self.assertTrue(os.path.exists(expected_file))
    
    def test_model_serialization(self):
        """Test model serialization to dictionary."""
        model = self.builder.create_model(
            L_B_ratio=1.5,
            B=10.0,
            nx=2,
            ny=2
        )
        
        model_dict = model.to_dict()
        
        # Check required keys
        required_keys = ['name', 'parameters', 'nodes', 'elements', 'sections', 'loads', 'analysis_config']
        for key in required_keys:
            self.assertIn(key, model_dict)
        
        # Check parameters
        params = model_dict['parameters']
        self.assertEqual(params['L_B_ratio'], 1.5)
        self.assertEqual(params['B'], 10.0)
        self.assertEqual(params['L'], 15.0)
        self.assertEqual(params['nx'], 2)
        self.assertEqual(params['ny'], 2)
        
        # Check that data structures are serializable
        import json
        json_str = json.dumps(model_dict)  # Should not raise an exception
        self.assertIsInstance(json_str, str)
    
    def test_model_summary(self):
        """Test model summary functionality."""
        model = self.builder.create_model(
            L_B_ratio=2.0,
            B=12.0,
            nx=4,
            ny=3
        )
        
        summary = model.get_model_summary()
        
        # Check required keys
        required_keys = ['name', 'dimensions', 'mesh', 'counts', 'analyses']
        for key in required_keys:
            self.assertIn(key, summary)
        
        # Check dimensions
        dims = summary['dimensions']
        self.assertEqual(dims['L'], 24.0)  # 2.0 * 12.0
        self.assertEqual(dims['B'], 12.0)
        self.assertEqual(dims['aspect_ratio'], 2.0)
        self.assertEqual(dims['footprint_area'], 288.0)  # 24.0 * 12.0
        
        # Check mesh
        mesh = summary['mesh']
        self.assertEqual(mesh['nx'], 4)
        self.assertEqual(mesh['ny'], 3)
        self.assertEqual(mesh['num_floors'], 2)
        
        # Check counts
        counts = summary['counts']
        self.assertGreater(counts['nodes'], 0)
        self.assertGreater(counts['elements'], 0)
        self.assertEqual(counts['sections'], 3)


class TestArchitectureIntegration(unittest.TestCase):
    """Integration tests for the complete architecture."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow."""
        builder = ModelBuilder(output_dir=self.temp_dir)
        
        # Create model
        model = builder.create_model(
            L_B_ratio=1.8,
            B=15.0,
            nx=5,
            ny=4,
            enabled_analyses=['static', 'modal', 'dynamic'],
            analysis_params={
                'modal': {'num_modes': 10},
                'dynamic': {'dt': 0.01, 'num_steps': 1000},
                'visualization': {
                    'enabled': True,
                    'modal_shapes': True,
                    'deform_scale': 100
                }
            }
        )
        
        # Verify model structure
        self.assertEqual(len(model.analysis_config.enabled_analyses), 3)
        self.assertGreater(len(model.geometry.nodes), 0)
        self.assertGreater(len(model.geometry.elements), 0)
        self.assertGreater(len(model.loads.loads), 0)
        
        # Test domain object methods
        boundary_nodes = model.geometry.get_boundary_nodes()
        self.assertGreater(len(boundary_nodes), 0)
        
        columns = model.geometry.get_elements_by_type('column')
        self.assertGreater(len(columns), 0)
        
        total_load = model.loads.get_total_vertical_load()
        self.assertGreater(total_load, 0)
        
        # Test analysis configuration
        self.assertTrue(model.analysis_config.is_enabled('static'))
        self.assertTrue(model.analysis_config.is_enabled('modal'))
        self.assertTrue(model.analysis_config.is_enabled('dynamic'))
        
        modal_config = model.analysis_config.get_solver_config('modal')
        self.assertIsNotNone(modal_config)
        self.assertEqual(modal_config['num_modes'], 10)
        
        # Test file operations
        model_file = os.path.join(self.temp_dir, f"{model.name}.json")
        self.assertTrue(os.path.exists(model_file))
        
        # Verify file content
        import json
        with open(model_file, 'r') as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data['name'], model.name)
        self.assertIn('nodes', saved_data)
        self.assertIn('elements', saved_data)
        self.assertIn('analysis_config', saved_data)


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestDomainObjects,
        TestBuilders,
        TestNewModelBuilder,
        TestArchitectureIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")
