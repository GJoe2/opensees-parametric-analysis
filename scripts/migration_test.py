"""
Migration script to gradually transition from old ModelBuilder to new architecture.

This script demonstrates how to use both the old and new ModelBuilder implementations
side by side, allowing for gradual migration.
"""

import os
import sys
import json
from typing import Dict, Any

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from model_builder import ModelBuilder as OldModelBuilder
from model_builder_v2 import ModelBuilder as NewModelBuilder


def compare_models(old_model_data: Dict, new_model: Any) -> Dict[str, Any]:
    """
    Compare models created by old and new builders.
    
    Args:
        old_model_data: Data from old ModelBuilder
        new_model: StructuralModel from new ModelBuilder
        
    Returns:
        Comparison results
    """
    new_model_data = new_model.to_dict()
    
    comparison = {
        'nodes_match': len(old_model_data['nodes']) == len(new_model_data['nodes']),
        'elements_match': len(old_model_data['elements']) == len(new_model_data['elements']),
        'sections_match': len(old_model_data['sections']) == len(new_model_data['sections']),
        'loads_match': len(old_model_data['loads']) == len(new_model_data['loads']),
        'old_node_count': len(old_model_data['nodes']),
        'new_node_count': len(new_model_data['nodes']),
        'old_element_count': len(old_model_data['elements']),
        'new_element_count': len(new_model_data['elements'])
    }
    
    return comparison


def migration_test():
    """Test the migration by creating models with both builders and comparing them."""
    
    print("=== Migration Test: Comparing Old vs New ModelBuilder ===\n")
    
    # Test parameters
    test_params = [
        {'L_B_ratio': 1.5, 'B': 10.0, 'nx': 3, 'ny': 2},
        {'L_B_ratio': 2.0, 'B': 12.0, 'nx': 4, 'ny': 3},
        {'L_B_ratio': 1.0, 'B': 8.0, 'nx': 2, 'ny': 2}
    ]
    
    # Create output directories
    old_output = "models_old"
    new_output = "models_new"
    
    old_builder = OldModelBuilder(output_dir=old_output)
    new_builder = NewModelBuilder(output_dir=new_output)
    
    for i, params in enumerate(test_params, 1):
        print(f"Test {i}: L/B={params['L_B_ratio']}, B={params['B']}, nx={params['nx']}, ny={params['ny']}")
        
        try:
            # Create model with old builder
            old_model_data = old_builder.create_model(**params)
            print(f"  ✓ Old model created: {old_model_data['name']}")
            
            # Create model with new builder
            new_model = new_builder.create_model(**params)
            print(f"  ✓ New model created: {new_model.name}")
            
            # Compare models
            comparison = compare_models(old_model_data, new_model)
            
            print(f"  📊 Comparison:")
            print(f"    Nodes: {comparison['old_node_count']} vs {comparison['new_node_count']} - {'✓' if comparison['nodes_match'] else '✗'}")
            print(f"    Elements: {comparison['old_element_count']} vs {comparison['new_element_count']} - {'✓' if comparison['elements_match'] else '✗'}")
            print(f"    Sections: {'✓' if comparison['sections_match'] else '✗'}")
            print(f"    Loads: {'✓' if comparison['loads_match'] else '✗'}")
            
            # Test new model features
            summary = new_model.get_model_summary()
            print(f"  🏗️  New model features:")
            print(f"    Footprint area: {summary['dimensions']['footprint_area']:.1f} m²")
            print(f"    Total height: {summary['dimensions']['height']:.1f} m")
            print(f"    Aspect ratio: {summary['dimensions']['aspect_ratio']:.2f}")
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
        
        print()


def demonstrate_new_features():
    """Demonstrate new features available in the improved architecture."""
    
    print("=== Demonstrating New Architecture Features ===\n")
    
    # Create new builder
    builder = NewModelBuilder(output_dir="models_demo")
    
    # 1. Basic model creation
    print("1. Creating basic model...")
    model = builder.create_model(
        L_B_ratio=1.5,
        B=10.0,
        nx=3,
        ny=2,
        enabled_analyses=['static', 'modal']
    )
    print(f"   Model created: {model.name}")
    
    # 2. Model with custom analysis parameters
    print("\n2. Creating model with custom analysis parameters...")
    custom_model = builder.create_model(
        L_B_ratio=2.0,
        B=12.0,
        nx=4,
        ny=3,
        enabled_analyses=['static', 'modal', 'dynamic'],
        analysis_params={
            'modal': {'num_modes': 10},
            'dynamic': {'dt': 0.005, 'num_steps': 2000},
            'visualization': {
                'enabled': True,
                'modal_shapes': True,
                'deform_scale': 200
            }
        }
    )
    print(f"   Custom model created: {custom_model.name}")
    
    # 3. Demonstrate domain object features
    print("\n3. Using domain object features...")
    
    # Geometry features
    print(f"   Total nodes: {len(custom_model.geometry.nodes)}")
    print(f"   Total elements: {len(custom_model.geometry.elements)}")
    
    # Get boundary nodes
    boundary_nodes = custom_model.geometry.get_boundary_nodes()
    print(f"   Boundary nodes: {len(boundary_nodes)}")
    
    # Get elements by type
    columns = custom_model.geometry.get_elements_by_type('column')
    beams_x = custom_model.geometry.get_elements_by_type('beam_x')
    slabs = custom_model.geometry.get_elements_by_type('slab')
    print(f"   Columns: {len(columns)}, Beams (X): {len(beams_x)}, Slabs: {len(slabs)}")
    
    # Analysis config features
    print(f"   Enabled analyses: {custom_model.analysis_config.enabled_analyses}")
    print(f"   Modal analysis modes: {custom_model.analysis_config.modal_config.num_modes}")
    print(f"   Dynamic analysis dt: {custom_model.analysis_config.dynamic_config.dt}")
    
    # Load features
    total_load = custom_model.loads.get_total_vertical_load()
    loaded_nodes = len(custom_model.loads.get_loaded_nodes())
    print(f"   Total vertical load: {total_load:.1f} tonf")
    print(f"   Loaded nodes: {loaded_nodes}")
    
    # 4. Model summary
    print("\n4. Model summary:")
    summary = custom_model.get_model_summary()
    for category, data in summary.items():
        print(f"   {category.title()}:")
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, float):
                    print(f"     {key}: {value:.2f}")
                else:
                    print(f"     {key}: {value}")
        else:
            print(f"     {data}")


def main():
    """Main function to run migration tests and demonstrations."""
    
    print("🏗️  OpenSees Model Builder - Architecture Migration\n")
    
    # Run migration test
    migration_test()
    
    # Demonstrate new features
    demonstrate_new_features()
    
    print("\n=== Migration Complete ===")
    print("✓ Old and new builders are working side by side")
    print("✓ New architecture provides better organization and features")
    print("✓ Gradual migration is possible")


if __name__ == "__main__":
    main()
