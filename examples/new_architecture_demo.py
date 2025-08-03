"""
Example script demonstrating the new improved ModelBuilder architecture.

This example shows how to use the new domain objects and specialized builders
to create structural models with better organization and features.
"""

import os
import sys

# Add src to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import with error handling
try:
    from model_builder_v2 import ModelBuilder
    from domain import StructuralModel
    from builders import GeometryBuilder, SectionsBuilder, LoadsBuilder, AnalysisConfigBuilder
    print("✓ Imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the correct directory")
    sys.exit(1)


def example_1_basic_usage():
    """Example 1: Basic usage of the new ModelBuilder."""
    
    print("=== Example 1: Basic Model Creation ===\n")
    
    # Create output directory relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "examples_output")
    
    # Create model builder
    builder = ModelBuilder(output_dir=output_dir)
    
    # Create a simple model
    model = builder.create_model(
        L_B_ratio=1.5,
        B=10.0,
        nx=3,
        ny=2
    )
    
    print(f"✓ Model created: {model.name}")
    print(f"  Dimensions: {model.geometry.L}m x {model.geometry.B}m")
    print(f"  Nodes: {len(model.geometry.nodes)}")
    print(f"  Elements: {len(model.geometry.elements)}")
    print(f"  Default analyses: {model.analysis_config.enabled_analyses}")
    
    return model


def example_2_custom_analysis():
    """Example 2: Model with custom analysis configuration."""
    
    print("\n=== Example 2: Custom Analysis Configuration ===\n")
    
    # Create output directory relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "examples_output")
    
    builder = ModelBuilder(output_dir=output_dir)
    
    # Create model with custom analysis parameters
    model = builder.create_model(
        L_B_ratio=2.0,
        B=12.0,
        nx=4,
        ny=3,
        enabled_analyses=['static', 'modal', 'dynamic'],
        analysis_params={
            'static': {
                'steps': 20,
                'algorithm': 'Newton'
            },
            'modal': {
                'num_modes': 12
            },
            'dynamic': {
                'dt': 0.005,
                'num_steps': 2000,
                'integrator': 'Newmark'
            },
            'visualization': {
                'enabled': True,
                'modal_shapes': True,
                'static_deformed': True,
                'deform_scale': 150
            }
        }
    )
    
    print(f"✓ Custom model created: {model.name}")
    print(f"  Enabled analyses: {model.analysis_config.enabled_analyses}")
    print(f"  Modal modes: {model.analysis_config.modal_config.num_modes}")
    print(f"  Dynamic dt: {model.analysis_config.dynamic_config.dt}")
    print(f"  Static steps: {model.analysis_config.static_config.steps}")
    print(f"  Visualization enabled: {model.analysis_config.visualization_config.enabled}")
    
    return model


def example_3_domain_object_usage():
    """Example 3: Using domain objects directly."""
    
    print("\n=== Example 3: Domain Object Features ===\n")
    
    # Create output directory relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "examples_output")
    
    builder = ModelBuilder(output_dir=output_dir)
    model = builder.create_model(L_B_ratio=1.8, B=15.0, nx=5, ny=4)
    
    print(f"Model: {model.name}")
    print(f"Total height: {model.geometry.get_total_height():.1f} m")
    print(f"Footprint area: {model.geometry.get_footprint_area():.1f} m²")
    print(f"Aspect ratio: {model.geometry.get_aspect_ratio():.2f}")
    
    # Analyze geometry
    print("\n📐 Geometry Analysis:")
    print(f"  Total nodes: {len(model.geometry.nodes)}")
    
    # Get nodes by floor
    for floor in range(model.geometry.num_floors + 1):
        floor_nodes = model.geometry.get_floor_nodes(floor)
        print(f"  Floor {floor}: {len(floor_nodes)} nodes")
    
    # Get boundary nodes
    boundary_nodes = model.geometry.get_boundary_nodes()
    print(f"  Boundary nodes: {len(boundary_nodes)}")
    
    # Analyze elements by type
    print("\n🏗️  Element Analysis:")
    columns = model.geometry.get_elements_by_type('column')
    beams_x = model.geometry.get_elements_by_type('beam_x')
    beams_y = model.geometry.get_elements_by_type('beam_y')
    slabs = model.geometry.get_elements_by_type('slab')
    
    print(f"  Columns: {len(columns)}")
    print(f"  Beams (X): {len(beams_x)}")
    print(f"  Beams (Y): {len(beams_y)}")
    print(f"  Slabs: {len(slabs)}")
    
    # Analyze loads
    print("\n⚖️  Load Analysis:")
    total_load = model.loads.get_total_vertical_load()
    loaded_nodes = model.loads.get_loaded_nodes()
    print(f"  Total vertical load: {total_load:.1f} tonf")
    print(f"  Loaded nodes: {len(loaded_nodes)}")
    
    return model


def example_4_multiple_models():
    """Example 4: Creating multiple models with different parameters."""
    
    print("\n=== Example 4: Multiple Model Creation ===\n")
    
    # Create output directory relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "examples_output")
    
    builder = ModelBuilder(output_dir=output_dir)
    
    # Define parameter combinations
    parameter_sets = [
        {
            'L_B_ratio': 1.0,
            'B': 8.0,
            'nx': 2,
            'ny': 2,
            'enabled_analyses': ['static']
        },
        {
            'L_B_ratio': 1.5,
            'B': 10.0,
            'nx': 3,
            'ny': 2,
            'enabled_analyses': ['static', 'modal']
        },
        {
            'L_B_ratio': 2.0,
            'B': 12.0,
            'nx': 4,
            'ny': 3,
            'enabled_analyses': ['static', 'modal', 'dynamic'],
            'analysis_params': {
                'modal': {'num_modes': 8},
                'visualization': {'enabled': True}
            }
        }
    ]
    
    models = builder.create_multiple_models(parameter_sets)
    
    print(f"✓ Created {len(models)} models:")
    for model in models:
        summary = model.get_model_summary()
        print(f"  {model.name}:")
        print(f"    Size: {summary['dimensions']['L']:.1f}x{summary['dimensions']['B']:.1f}m")
        print(f"    Elements: {summary['counts']['elements']}")
        print(f"    Analyses: {', '.join(summary['analyses']['enabled'])}")
    
    return models


def example_5_using_builders_directly():
    """Example 5: Using specialized builders directly for custom needs."""
    
    print("\n=== Example 5: Using Builders Directly ===\n")
    
    # Create geometry using GeometryBuilder
    geometry = GeometryBuilder.create(
        L_B_ratio=1.6,
        B=14.0,
        nx=4,
        ny=4,
        num_floors=3,  # Custom: 3 floors instead of default 2
        floor_height=3.5  # Custom: 3.5m floor height
    )
    
    print(f"✓ Custom geometry created:")
    print(f"  Size: {geometry.L:.1f}x{geometry.B:.1f}m")
    print(f"  Floors: {geometry.num_floors}")
    print(f"  Floor height: {geometry.floor_height:.1f}m")
    print(f"  Total height: {geometry.get_total_height():.1f}m")
    
    # Create custom sections
    custom_params = {
        'column_size': (0.50, 0.50),  # Larger columns
        'beam_size': (0.30, 0.50),    # Larger beams
        'slab_thickness': 0.15        # Thicker slab
    }
    sections = SectionsBuilder.create(custom_params)
    
    print(f"  Custom sections with larger elements")
    
    # Create custom loads
    custom_loads = LoadsBuilder.create(
        geometry=geometry,
        load_params={'distributed_load': 1.5}  # Higher load
    )
    
    print(f"  Higher distributed load: 1.5 tonf/m²")
    
    # Create analysis config
    analysis_config = AnalysisConfigBuilder.create(
        enabled_analyses=['static', 'modal'],
        analysis_params={
            'modal': {'num_modes': 15},
            'visualization': {'enabled': True, 'modal_shapes': True}
        }
    )
    
    # Create the complete model
    custom_model = StructuralModel(
        geometry=geometry,
        sections=sections,
        loads=custom_loads,
        analysis_config=analysis_config,
        name="CUSTOM_MODEL_160_14_0404"
    )
    
    # Save the custom model
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "examples_output")
    custom_model.save(os.path.join(output_dir, f"{custom_model.name}.json"))
    
    print(f"✓ Custom model saved: {custom_model.name}")
    
    return custom_model


def main():
    """Run all examples demonstrating the new architecture."""
    
    print("🏗️  New ModelBuilder Architecture - Examples\n")
    
    # Create output directory relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "examples_output")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📁 Output directory: {output_dir}")
    
    # Run examples
    try:
        model1 = example_1_basic_usage()
        model2 = example_2_custom_analysis()
        model3 = example_3_domain_object_usage()
        models4 = example_4_multiple_models()
        model5 = example_5_using_builders_directly()
        
        print("\n=== Summary ===")
        print(f"✓ All examples completed successfully")
        print(f"✓ Demonstrated: Basic usage, custom analysis, domain objects, multiple models, direct builders")
        print(f"✓ Check '{output_dir}' directory for generated model files")
        
    except Exception as e:
        print(f"❌ Error running examples: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
