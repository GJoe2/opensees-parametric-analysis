#!/usr/bin/env python3
"""
Script para verificar los tipos de datos en StructuralModel.to_dict() vs JSON
"""

import json
import os
import sys

# Agregar src al path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'src'))

def main():
    print("=== VERIFICACIÓN DE TIPOS: StructuralModel.to_dict() vs JSON ===\n")
    
    # Cargar desde JSON (como viene del archivo)
    json_file = os.path.join(current_dir, "examples", "json_exports", "Edificio_3P.json")
    
    if not os.path.exists(json_file):
        print(f"Error: No se encontró {json_file}")
        return
        
    with open(json_file, 'r', encoding='utf-8') as f:
        modelo_from_json = json.load(f)
    
    print("1. TIPOS EN MODELO CARGADO DESDE JSON:")
    sections_json = modelo_from_json.get('sections', {})
    elements_json = modelo_from_json.get('elements', {})
    
    print("   Llaves en sections:")
    for key in list(sections_json.keys())[:3]:
        print(f"     '{key}' -> tipo: {type(key)}")
    
    print("   section_tag en elements:")
    for elem_id, elem in list(elements_json.items())[:3]:
        sec_tag = elem.get('section_tag')
        print(f"     Elemento {elem_id}: section_tag = {sec_tag} (tipo: {type(sec_tag)})")
    
    print("\n2. PROBLEMA DEL PYTHONEXPORTER:")
    # Simular lo que hace el PythonExporter
    elem_id = list(elements_json.keys())[0]
    elem = elements_json[elem_id]
    sec_tag = elem.get('section_tag')  # Esto es int
    
    print(f"   sec_tag obtenido: {sec_tag} (tipo: {type(sec_tag)})")
    print(f"   Buscar sections.get({sec_tag}): {sections_json.get(sec_tag)}")  # None!
    print(f"   Buscar sections.get(str({sec_tag})): {sections_json.get(str(sec_tag)) is not None}")  # Funciona!
    
    # Crear modelo desde ModelBuilder para comparar
    print("\n3. MODELO CREADO CON MODELBUILDER:")
    try:
        from model_builder import ModelBuilder
        
        builder = ModelBuilder()
        modelo_obj = builder.create_model(
            L_B_ratio=1.5,
            B=10.0,
            nx=2,
            ny=2,
            model_name="Test"
        )
        
        # Convertir a diccionario SIN pasar por JSON
        modelo_dict = modelo_obj.to_dict()
        
        sections_dict = modelo_dict.get('sections', {})
        elements_dict = modelo_dict.get('elements', {})
        
        print("   Llaves en sections (directo de to_dict()):")
        for key in list(sections_dict.keys())[:3]:
            print(f"     {key} -> tipo: {type(key)}")
        
        print("   section_tag en elements (directo de to_dict()):")
        for elem_id, elem in list(elements_dict.items())[:3]:
            sec_tag = elem.get('section_tag')
            print(f"     Elemento {elem_id}: section_tag = {sec_tag} (tipo: {type(sec_tag)})")
        
        # Probar acceso
        elem_id = list(elements_dict.keys())[0]
        elem = elements_dict[elem_id]
        sec_tag = elem.get('section_tag')
        
        print(f"\n   Prueba de acceso en modelo de ModelBuilder:")
        print(f"     sec_tag: {sec_tag} (tipo: {type(sec_tag)})")
        print(f"     sections.get({sec_tag}): {sections_dict.get(sec_tag) is not None}")
        print(f"     sections.get(str({sec_tag})): {sections_dict.get(str(sec_tag)) is not None}")
        
    except ImportError:
        print("   No se pudo importar ModelBuilder")
    
    print("\n4. CONCLUSIÓN:")
    print("   ✓ JSON siempre convierte llaves de objetos a strings")
    print("   ✓ StructuralModel.to_dict() mantiene tipos originales")
    print("   ✓ PythonExporter necesita manejar ambos casos")
    print("   ✓ La conversión str(sec_tag) es necesaria para compatibilidad con JSON")

if __name__ == "__main__":
    main()
