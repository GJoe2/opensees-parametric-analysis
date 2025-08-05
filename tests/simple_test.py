"""
Simple test script to verify the new architecture works correctly.
"""

import os
import sys
import tempfile
import shutil

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    from model_builder import ModelBuilder
    from domain import StructuralModel, Geometry, Node, Element
    from builders import GeometryBuilder, SectionsBuilder, LoadsBuilder, AnalysisConfigBuilder
    print("✓ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def test_basic_functionality():
    """Test basic functionality of the new architecture."""
    print("\n=== Testing Basic Functionality ===")
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"📁 Using temp directory: {temp_dir}")
    
    try:
        # Test 1: ModelBuilder creation
        builder = ModelBuilder(output_dir=temp_dir)
        print("✓ ModelBuilder created successfully")
        
        # Test 2: Basic model creation
        model = builder.create_model(
            L_B_ratio=1.5,
            B=10.0,
            nx=3,
            ny=2
        )
        print(f"✓ Basic model created: {model.name}")
        
        # Test 3: Verify model properties
        assert isinstance(model, StructuralModel)
        assert model.geometry.L == 15.0  # 1.5 * 10.0
        assert model.geometry.B == 10.0
        assert len(model.analysis_config.enabled_analyses) == 2  # default: static, modal
        print("✓ Model properties verified")
        
        # Test 4: Domain object methods
        boundary_nodes = model.geometry.get_boundary_nodes()
        total_load = model.loads.get_total_vertical_load()
        columns = model.geometry.get_elements_by_type('column')
        print(f"✓ Domain methods work: {len(boundary_nodes)} boundary nodes, {total_load} tonf load, {len(columns)} columns")
        
        # Test 5: Model with custom parameters
        custom_model = builder.create_model(
            L_B_ratio=2.0,
            B=8.0,
            nx=2,
            ny=2,
            enabled_analyses=['static', 'modal', 'dynamic'],
            analysis_params={
                'modal': {'num_modes': 8},
                'visualization': {'enabled': True}
            }
        )
        print(f"✓ Custom model created: {custom_model.name}")
        assert len(custom_model.analysis_config.enabled_analyses) == 3
        assert custom_model.analysis_config.modal_config.num_modes == 8
        print("✓ Custom parameters verified")
        
        # Test 6: Multiple models
        param_sets = [
            {'L_B_ratio': 1.0, 'B': 6.0, 'nx': 2, 'ny': 2},
            {'L_B_ratio': 1.5, 'B': 8.0, 'nx': 3, 'ny': 2}
        ]
        models = builder.create_multiple_models(param_sets)
        assert len(models) == 2
        print(f"✓ Multiple models created: {len(models)} models")
        
        # Test 7: File creation
        for model in [model, custom_model] + models:
            expected_file = os.path.join(temp_dir, f"{model.name}.json")
            assert os.path.exists(expected_file), f"File not found: {expected_file}"
        print("✓ All model files created")
        
        # Test 8: Model serialization
        model_dict = model.to_dict()
        required_keys = ['name', 'parameters', 'nodes', 'elements', 'sections', 'loads', 'analysis_config']
        for key in required_keys:
            assert key in model_dict, f"Missing key: {key}"
        print("✓ Model serialization works")
        
        # Test 9: Model summary
        summary = model.get_model_summary()
        assert 'dimensions' in summary
        assert 'counts' in summary
        assert 'analyses' in summary
        print("✓ Model summary works")
        
        print("\n🎉 All tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir)
        print(f"🧹 Cleaned up temp directory")


def test_builders_directly():
    """Test using builders directly."""
    print("\n=== Testing Builders Directly ===")
    
    try:
        # Test GeometryBuilder
        geometry = GeometryBuilder.create(
            L_B_ratio=1.5, B=10.0, nx=2, ny=2,
            num_floors=2, floor_height=3.0
        )
        assert geometry.L == 15.0
        assert len(geometry.nodes) > 0
        assert len(geometry.elements) > 0
        print(f"✓ GeometryBuilder: {len(geometry.nodes)} nodes, {len(geometry.elements)} elements")
        
        # Test SectionsBuilder
        sections = SectionsBuilder.create({
            'column_size': (0.40, 0.40),
            'beam_size': (0.25, 0.40),
            'slab_thickness': 0.10
        })
        assert len(sections.sections) == 3
        assert len(sections.transformations) == 2
        print(f"✓ SectionsBuilder: {len(sections.sections)} sections, {len(sections.transformations)} transformations")
        
        # Test LoadsBuilder
        loads = LoadsBuilder.create(
            geometry=geometry,
            load_params={'distributed_load': 1.5}
        )
        assert len(loads.loads) > 0
        print(f"✓ LoadsBuilder: {len(loads.loads)} loads")
        
        # Test AnalysisConfigBuilder
        analysis_config = AnalysisConfigBuilder.create(
            enabled_analyses=['static', 'modal'],
            analysis_params={'modal': {'num_modes': 6}}
        )
        assert len(analysis_config.enabled_analyses) == 2
        assert analysis_config.modal_config.num_modes == 6
        print("✓ AnalysisConfigBuilder: configuration created")
        
        print("🎉 All builder tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Builder test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("🔧 Testing New ModelBuilder Architecture")
    print("=" * 50)
    
    # Run tests
    test1_result = test_basic_functionality()
    test2_result = test_builders_directly()
    
    # Summary
    print("\n" + "=" * 50)
    if test1_result and test2_result:
        print("🎉 ALL TESTS PASSED! The new architecture is working correctly.")
        print("✅ Ready for production use!")
    else:
        print("❌ Some tests failed. Please check the implementation.")
        sys.exit(1)


if __name__ == "__main__":
    main()
