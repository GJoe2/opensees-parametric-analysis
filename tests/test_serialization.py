#!/usr/bin/env python3
"""
Test script for serialization methods.

Tests the new serialization/deserialization functionality.
"""

import json
import sys
import os

from opsparametric import ModelBuilder


def test_serialization():
    """Test model creation, serialization, and deserialization."""
    print("🧪 Testing serialization functionality...")
    
    # Create model builder
    builder = ModelBuilder()
    
    # Create a simple model
    print("📊 Creating model...")
    model = builder.create_model(
        L_B_ratio=1.5,
        B=10.0,
        nx=2,
        ny=2,
        model_name="test_serialization_model"
    )
    
    print(f"✅ Model created: {model.name}")
    print(f"   - Nodes: {len(model.geometry.nodes)}")
    print(f"   - Elements: {len(model.geometry.elements)}")
    print(f"   - Sections: {len(model.sections.sections)}")
    print(f"   - Loads: {len(model.loads.loads)}")
    
    # Test serialization to dict
    print("\n🔄 Testing to_dict() serialization...")
    model_dict = model.to_dict()
    
    # Verify dict structure
    expected_keys = ['name', 'parameters', 'material', 'geometry', 'sections', 'loads', 'analysis_config']
    for key in expected_keys:
        if key not in model_dict:
            raise AssertionError(f"Missing key in serialized dict: {key}")
    
    print("✅ Serialization to dict successful")
    
    # Test JSON serialization
    print("\n📄 Testing JSON serialization...")
    json_str = json.dumps(model_dict, indent=2)
    print(f"✅ JSON serialization successful ({len(json_str)} characters)")
    
    # Test deserialization
    print("\n🔄 Testing deserialization...")
    data_from_json = json.loads(json_str)
    restored_model = model.from_dict(data_from_json)
    
    print(f"✅ Model restored: {restored_model.name}")
    print(f"   - Nodes: {len(restored_model.geometry.nodes)}")
    print(f"   - Elements: {len(restored_model.geometry.elements)}")
    print(f"   - Sections: {len(restored_model.sections.sections)}")
    print(f"   - Loads: {len(restored_model.loads.loads)}")
    
    # Verify integrity
    print("\n🔍 Verifying data integrity...")
    
    # Check nodes
    original_nodes = len(model.geometry.nodes)
    restored_nodes = len(restored_model.geometry.nodes)
    if original_nodes != restored_nodes:
        raise AssertionError(f"Node count mismatch: {original_nodes} vs {restored_nodes}")
    
    # Check elements
    original_elements = len(model.geometry.elements)
    restored_elements = len(restored_model.geometry.elements)
    if original_elements != restored_elements:
        raise AssertionError(f"Element count mismatch: {original_elements} vs {restored_elements}")
    
    # Check a specific node
    node_1_original = model.geometry.nodes[1]
    node_1_restored = restored_model.geometry.nodes[1]
    if node_1_original.coords != node_1_restored.coords:
        raise AssertionError(f"Node coords mismatch: {node_1_original.coords} vs {node_1_restored.coords}")
    
    print("✅ Data integrity verified")
    
    # Test file save/load
    print("\n💾 Testing file save/load...")
    test_file = "test_model.json"
    
    # Save
    model.save(test_file)
    print(f"✅ Model saved to {test_file}")
    
    # Load
    loaded_model = model.load(test_file)
    print(f"✅ Model loaded from {test_file}")
    print(f"   - Name: {loaded_model.name}")
    print(f"   - Nodes: {len(loaded_model.geometry.nodes)}")
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
        print("🧹 Test file cleaned up")
    
    print("\n🎉 All serialization tests passed!")


if __name__ == "__main__":
    try:
        test_serialization()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
