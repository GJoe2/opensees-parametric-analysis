#!/usr/bin/env python3
"""
Test script to verify that the JSON export no longer has double nesting.
"""

import sys
import os
import json


from opsparametric import ModelBuilder

def test_json_structure():
    """Test that JSON structure doesn't have double nesting."""
    
    print("Creating model...")
    builder = ModelBuilder()
    
    # Create a simple model
    model = builder.create_model(
        L_B_ratio=1.5,
        B=10.0,
        nx=2,
        ny=2
    )
    
    print("Converting to dictionary...")
    model_dict = model.to_dict()
    
    # Check sections structure
    print("\n=== SECTIONS STRUCTURE ===")
    if 'sections' in model_dict:
        sections = model_dict['sections']
        print(f"Type of sections: {type(sections)}")
        
        if isinstance(sections, dict):
            # Check if it has nested 'sections' key (BAD)
            if 'sections' in sections:
                print("❌ ERROR: Double nesting detected in sections!")
                print(f"Nested structure: {list(sections.keys())}")
                return False
            else:
                print("✅ GOOD: No double nesting in sections")
                print(f"Section tags: {list(sections.keys())}")
        else:
            print(f"❌ ERROR: sections is not a dict, it's {type(sections)}")
            return False
    
    # Check loads structure  
    print("\n=== LOADS STRUCTURE ===")
    if 'loads' in model_dict:
        loads = model_dict['loads']
        print(f"Type of loads: {type(loads)}")
        
        if isinstance(loads, dict):
            # Check if it has nested 'loads' key (BAD)
            if 'loads' in loads:
                print("❌ ERROR: Double nesting detected in loads!")
                print(f"Nested structure: {list(loads.keys())}")
                return False
            else:
                print("✅ GOOD: No double nesting in loads")
                print(f"Load keys: {list(loads.keys())}")
        else:
            print(f"❌ ERROR: loads is not a dict, it's {type(loads)}")
            return False
    
    # Show overall structure
    print("\n=== OVERALL JSON STRUCTURE ===")
    print(f"Top-level keys: {list(model_dict.keys())}")
    
    # Save to file for inspection
    output_file = "test_structure.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(model_dict, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ JSON exported to: {output_file}")
    print("✅ Structure verification completed successfully!")
    return True

if __name__ == "__main__":
    success = test_json_structure()
    if not success:
        sys.exit(1)
