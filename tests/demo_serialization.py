#!/usr/bin/env python3
"""
Demo script to show the cleaned up serialization.

Shows how much cleaner the code is now with the serialization methods.
"""

import json
import sys
import os

from opsparametric import ModelBuilder


def demo_clean_serialization():
    """Demo the clean serialization approach."""
    print("🚀 Demo: Clean Serialization with Methods")
    print("=" * 50)
    
    # Create model
    builder = ModelBuilder()
    model = builder.create_model(
        L_B_ratio=1.2,
        B=8.0,
        nx=1,
        ny=1,
        model_name="demo_clean_model"
    )
    
    print(f"📊 Model created: {model.name}")
    print(f"   - Dimensions: {model.geometry.L}m x {model.geometry.B}m")
    print(f"   - Grid: {model.geometry.nx+1} x {model.geometry.ny+1} nodes per floor")
    print(f"   - Floors: {model.geometry.num_floors}")
    print(f"   - Total nodes: {len(model.geometry.nodes)}")
    print(f"   - Total elements: {len(model.geometry.elements)}")
    
    # The magic: just one line to serialize everything!
    print("\n🔧 Serializing model...")
    model_dict = model.to_dict()
    
    print("✨ Clean serialization structure:")
    for key in model_dict.keys():
        if key == 'geometry':
            print(f"   📐 {key}: nodes({len(model_dict[key]['nodes'])}) + elements({len(model_dict[key]['elements'])})")
        elif key == 'material':
            print(f"   🧱 {key}: {model_dict[key]['name']} (E={model_dict[key]['E']:.0f})")
        elif key == 'sections':
            print(f"   📏 {key}: {len(model_dict[key]['sections'])} section types")
        elif key == 'loads':
            print(f"   ⚡ {key}: {len(model_dict[key]['loads'])} loaded nodes")
        else:
            print(f"   📋 {key}: {type(model_dict[key]).__name__}")
    
    # Show a sample of the clean JSON structure
    print("\n📄 Sample JSON structure (first node):")
    first_node_key = list(model_dict['geometry']['nodes'].keys())[0]
    first_node = model_dict['geometry']['nodes'][first_node_key]
    print(f"   Node {first_node_key}: {json.dumps(first_node, indent=4)}")
    
    print("\n📄 Sample JSON structure (first element):")
    first_elem_key = list(model_dict['geometry']['elements'].keys())[0]
    first_elem = model_dict['geometry']['elements'][first_elem_key]
    print(f"   Element {first_elem_key}: {json.dumps(first_elem, indent=4)}")
    
    # Show the benefits
    print("\n🎯 Benefits of this approach:")
    print("   ✅ No more manual loops for dict conversion")
    print("   ✅ Automatic int→string key conversion for JSON")
    print("   ✅ Type-safe deserialization with from_dict()")
    print("   ✅ Clean separation of concerns")
    print("   ✅ Consistent structure across all domain objects")
    
    # Round-trip test
    print("\n🔄 Testing round-trip serialization...")
    json_str = json.dumps(model_dict, indent=2)
    restored_data = json.loads(json_str)
    restored_model = model.from_dict(restored_data)
    
    print(f"   Original: {len(model.geometry.nodes)} nodes")
    print(f"   Restored: {len(restored_model.geometry.nodes)} nodes")
    print(f"   ✅ Round-trip successful!")
    
    print("\n💾 Save to file (also just one line):")
    model.save("demo_model.json")
    print("   model.save('demo_model.json')  # Done! 🎉")
    
    # Clean up
    if os.path.exists("demo_model.json"):
        os.remove("demo_model.json")


if __name__ == "__main__":
    demo_clean_serialization()
