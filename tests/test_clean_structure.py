#!/usr/bin/env python3
"""
Script de prueba simple para verificar los cambios en la estructura JSON.
"""

import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from opsparametric import ModelBuilder

def test_json_structure():
    """Prueba la nueva estructura JSON sin parámetros duplicados."""
    
    print("=== PROBANDO ESTRUCTURA JSON CORREGIDA ===\n")
    
    # Crear instancia del builder
    builder = ModelBuilder()
    
    # Actualizar material para que sea distintivo
    builder.update_material_params(
        E=30000,
        fc=300,
        name="concrete_c300"
    )
    
    # Crear modelo
    model = builder.create_model(
        L_B_ratio=2.0,
        B=10.0,
        nx=3,
        ny=2,
        model_name="structure_clean"
    )
    
    # Exportar modelo
    output_dir = "clean_structure_output"
    filepath = builder.export_model(model, output_dir=output_dir)
    print(f"Modelo exportado a: {filepath}")
    
    # Leer y verificar el JSON exportado
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("\n=== ESTRUCTURA JSON ===")
    print("Claves principales:", list(data.keys()))
    
    print("\n=== SECCIÓN 'parameters' ===")
    if 'parameters' in data:
        print("Parámetros geométricos solamente:")
        for key, value in data['parameters'].items():
            print(f"  {key}: {value}")
    
    print("\n=== SECCIÓN 'material' ===")
    if 'material' in data:
        print("Parámetros de material:")
        for key, value in data['material'].items():
            print(f"  {key}: {value}")
    
    print("\n=== VERIFICACIÓN DE SECCIONES ===")
    if 'sections' in data:
        print("Secciones con propiedades de material:")
        for tag, section in data['sections'].items():
            print(f"  Sección {tag} ({section.get('element_type', 'unknown')}):")
            if 'E' in section:
                print(f"    ✅ E: {section['E']}")
            if 'nu' in section:
                print(f"    ✅ nu: {section['nu']}")
            if 'material_name' in section:
                print(f"    ✅ material_name: {section['material_name']}")
    
    print(f"\n✅ Estructura JSON corregida exitosamente!")
    print(f"📁 Archivo: {filepath}")
    
    return data

if __name__ == "__main__":
    try:
        test_json_structure()
    except Exception as e:
        print(f"\n💥 Error: {e}")
        import traceback
        traceback.print_exc()
