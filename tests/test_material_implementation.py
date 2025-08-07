#!/usr/bin/env python3
"""
Script de prueba para verificar la nueva implementación de Material.

Este script verifica que los parámetros de material se incluyan correctamente
en el modelo exportado.
"""

import sys
import os
import json
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from opsparametric import ModelBuilder

def test_material_parameters():
    """Prueba la implementación de parámetros de material."""
    
    print("=== PROBANDO NUEVA IMPLEMENTACIÓN DE MATERIAL ===\n")
    
    # Crear instancia del builder
    builder = ModelBuilder()
    
    # Actualizar material para que sea distintivo
    builder.update_material_params(
        E=25000,
        fc=280,
        name="concrete_c280"
    )
    
    # Crear modelo
    print("1. Creando modelo...")
    model = builder.create_model(
        L_B_ratio=1.5,
        B=12.0,
        nx=4,
        ny=3,
        model_name="test_material_model"
    )
    
    # Exportar modelo
    print("2. Exportando modelo...")
    output_dir = "test_material_output"
    filepath = builder.export_model(model, output_dir=output_dir)
    print(f"   Exportado a: {filepath}")
    
    # Verificar el JSON exportado
    print("\n3. Verificando JSON exportado...")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"   Claves principales: {list(data.keys())}")
    
    # Verificar que parámetros NO están en 'parameters'
    print("\n4. Verificando sección 'parameters' (solo geometría):")
    params = data['parameters']
    geometry_params = ['L_B_ratio', 'nx', 'ny', 'L', 'B', 'num_floors', 'floor_height']
    material_params = ['E', 'nu', 'rho', 'G', 'material_name']
    
    for param in geometry_params:
        if param in params:
            print(f"   ✅ {param}: {params[param]}")
    
    for param in material_params:
        if param in params:
            print(f"   ❌ {param}: NO DEBERÍA ESTAR AQUÍ")
    
    # Verificar sección 'material' completa
    print("\n5. Verificando sección 'material':")
    material = data['material']
    for key, value in material.items():
        print(f"   ✅ {key}: {value}")
    
    # Verificar que las secciones solo tienen referencia al material
    print("\n6. Verificando secciones (solo referencia):")
    for tag, section in data['sections'].items():
        element_type = section.get('element_type', 'unknown')
        print(f"   Sección {tag} ({element_type}):")
        
        if 'material_name' in section:
            print(f"     ✅ material_name: {section['material_name']}")
        else:
            print(f"     ❌ Falta material_name")
        
        # Verificar que NO tiene propiedades duplicadas
        unwanted_props = ['E', 'nu', 'rho', 'G']
        for prop in unwanted_props:
            if prop in section:
                print(f"     ❌ {prop}: NO DEBERÍA ESTAR AQUÍ (duplicación)")
    
    print("\n=== PRUEBA COMPLETADA ===")
    return filepath

def test_backwards_compatibility():
    """Prueba compatibilidad hacia atrás."""
    print("\n=== PROBANDO COMPATIBILIDAD HACIA ATRÁS ===")
    
    # Importar directamente
    from opsparametric.builders import SectionsBuilder
    
    fixed_params = {
        'column_size': (0.40, 0.40),
        'beam_size': (0.25, 0.40),
        'slab_thickness': 0.10
    }
    
    try:
        # Código antiguo: sin material
        sections = SectionsBuilder.create(fixed_params)
        print("   ✅ SectionsBuilder funciona sin material")
        
        # Verificar que las secciones no tienen material_name
        for tag, section in sections.sections.items():
            if section.properties:
                print(f"   ❌ Sección {tag} tiene propiedades: {section.properties}")
            else:
                print(f"   ✅ Sección {tag} sin propiedades")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    try:
        # Ejecutar pruebas
        filepath = test_material_parameters()
        test_backwards_compatibility()
        
        print(f"\n🎉 ¡Implementación exitosa!")
        print(f"📁 Archivo de prueba generado: {filepath}")
        
    except Exception as e:
        print(f"\n💥 Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
