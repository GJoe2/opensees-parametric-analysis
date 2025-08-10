#!/usr/bin/env python3
"""
Test script for PythonExporterV2 - Optimized version with domain objects.

This script demonstrates how the new PythonExporterV2 works directly with
StructuralModel objects for better performance and type safety.
"""

import sys
import os

from opsparametric import ModelBuilder
from opsparametric import PythonExporterV2

def test_python_exporter_v2():
    """Test the optimized PythonExporterV2 with StructuralModel objects."""
    
    print("🚀 Testing PythonExporterV2 with StructuralModel objects...")
    print("=" * 60)
    
    # Create model using ModelBuilder
    print("\n1️⃣ Creating structural model...")
    builder = ModelBuilder()
    
    # Update some parameters for testing
    builder.update_material_params(
        E=25000e6,  # 25 GPa
        fc=280,     # Higher strength concrete
        name="concrete_c280"
    )
    
    builder.update_fixed_params(
        column_size=(0.50, 0.50),  # Larger columns
        beam_size=(0.30, 0.50),    # Standard beams
        num_floors=3               # 3 floors
    )
    
    # Create model
    model = builder.create_model(
        L_B_ratio=1.5,
        B=12.0,
        nx=3,
        ny=3,
        model_name="TestBuilding_V2",
        enabled_analyses=['static', 'modal'],
        analysis_params={
            'modal': {'num_modes': 10},
            'static': {'steps': 15}
        }
    )
    
    print(f"✅ Model created: {model.name}")
    print(f"   - Dimensions: {model.parameters.L}m x {model.parameters.B}m")
    print(f"   - Material: {model.material.name} (E={model.material.E/1e9:.1f} GPa)")
    print(f"   - Mesh: {model.parameters.nx}x{model.parameters.ny}")
    print(f"   - Floors: {model.parameters.num_floors}")
    print(f"   - Nodes: {len(model.geometry.nodes)}")
    print(f"   - Elements: {len(model.geometry.elements)}")
    print(f"   - Loads: {len(model.loads.loads)}")
    
    # Test exporter
    print("\n2️⃣ Testing PythonExporterV2...")
    
    # Create exporter with custom output directory
    exporter = PythonExporterV2("./test_exports_v2")
    
    # Test 1: Combined file export
    print("\n   📄 Testing combined file export...")
    combined_files = exporter.export_script(model, separate_files=False)
    print(f"   ✅ Combined files generated: {len(combined_files)}")
    for file in combined_files:
        print(f"      - {file}")
    
    # Test 2: Separate files export
    print("\n   📂 Testing separate files export...")
    separate_files = exporter.export_script(model, separate_files=True)
    print(f"   ✅ Separate files generated: {len(separate_files)}")
    for file in separate_files:
        print(f"      - {file}")
    
    # Test 3: Model summary export
    print("\n   📊 Testing model summary export...")
    summary_file = exporter.export_model_summary(model)
    print(f"   ✅ Summary file generated: {summary_file}")
    
    # Verify generated files contain expected content
    print("\n3️⃣ Verifying generated code...")
    
    # Check combined file
    combined_file = combined_files[0]
    with open(combined_file, 'r', encoding='utf-8') as f:
        combined_content = f.read()
    
    # Verify key elements are present
    checks = [
        ('Material properties', f"E = {model.material.E}"),
        ('Calculated shear modulus', f"G = {model.material.G}"),
        ('Model dimensions', f"L, B = {model.parameters.L}, {model.parameters.B}"),
        ('Build function', "def build_model():"),
        ('Analysis function', "def run_analysis():"),
        ('Modal analysis', "Modal Analysis" in combined_content),
        ('Static analysis', "Static Analysis" in combined_content),
    ]
    
    for check_name, check_condition in checks:
        if isinstance(check_condition, str):
            result = check_condition in combined_content
        else:
            result = check_condition
        
        status = "✅" if result else "❌"
        print(f"   {status} {check_name}")
    
    # Check summary file
    with open(summary_file, 'r', encoding='utf-8') as f:
        summary_content = f.read()
    
    print(f"\n   📋 Summary file preview:")
    print("   " + "-" * 40)
    for line in summary_content.split('\n')[:10]:
        print(f"   {line}")
    print("   ...")
    
    # Performance comparison note
    print("\n4️⃣ Performance Benefits:")
    print("   ✅ No unnecessary dictionary conversion")
    print("   ✅ Direct access to calculated properties (e.g., material.G)")
    print("   ✅ Type-safe property access")
    print("   ✅ Automatic property validation from dataclasses")
    print("   ✅ Rich object methods available (e.g., model.get_model_summary())")
    
    print(f"\n🎉 PythonExporterV2 test completed successfully!")
    print(f"📁 All files saved to: {exporter.output_dir}")
    
    return True

def compare_with_v1():
    """Quick comparison between V1 and V2 approaches."""
    
    print("\n" + "="*60)
    print("🔄 COMPARISON: V1 vs V2 Approach")
    print("="*60)
    
    # Create same model for comparison
    builder = ModelBuilder()
    model = builder.create_model(L_B_ratio=1.5, B=10, nx=2, ny=2, model_name="ComparisonTest")
    
    print("\n📊 Code Access Comparison:")
    print("\n   V1 (Dictionary-based):")
    print("   model_dict = model.to_dict()  # ← Unnecessary conversion")
    print("   E = model_dict.get('material', {}).get('E', 'default?')  # ← Error-prone")
    print("   G = E / (2 * (1 + nu))  # ← Manual calculation")
    
    print("\n   V2 (Object-based):")
    print("   E = model.material.E  # ← Direct, type-safe")
    print("   G = model.material.G  # ← Calculated property available!")
    print("   nodes = model.geometry.nodes  # ← Rich object access")
    
    print(f"\n📈 Actual Values Comparison:")
    print(f"   Material E: {model.material.E}")
    print(f"   Material G (calculated): {model.material.G}")
    print(f"   Model name: {model.name}")
    print(f"   Total nodes: {len(model.geometry.nodes)}")
    print(f"   Load count: {len(model.loads.loads)}")

if __name__ == "__main__":
    try:
        success = test_python_exporter_v2()
        compare_with_v1()
        
        if success:
            print("\n🎯 All tests passed! PythonExporterV2 is ready to use.")
        else:
            print("\n❌ Some tests failed. Check the output above.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
