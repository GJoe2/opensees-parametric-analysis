"""
Debug: Análisis del comportamiento de transf_tag en PythonExporter
===============================================================

Este script verifica paso a paso cómo el PythonExporter maneja los transf_tag
y por qué todos los elementos están usando el valor por defecto de 1000.

Autor: GitHub Copilot
Fecha: 2025
"""

import sys
import os
import json

from opsparametric import ModelBuilder
from opsparametric import PythonExporter

def debug_transf_tag():
    print("=" * 70)
    print("DEBUG: Análisis del comportamiento de transf_tag")
    print("=" * 70)
    
    # 1. CREAR MODELO
    print("\n1. CREANDO MODELO...")
    builder = ModelBuilder()
    
    # Configurar material
    builder.update_material_params(
        name='Concreto_Debug',
        E=2.5e10,
        nu=0.2,
        rho=2400
    )
    
    # Crear modelo simple
    model = builder.create_model(
        L_B_ratio=2.0,
        B=8.0,
        nx=2,
        ny=1,
        model_name="debug_transf"
    )
    
    print(f"✓ Modelo creado: {model.name}")
    
    # 2. CONVERTIR A DICCIONARIO
    print("\n2. CONVIRTIENDO A DICCIONARIO...")
    model_dict = model.to_dict()
    
    # 3. ANALIZAR SECCIONES DEL JSON
    print("\n3. ANÁLISIS DE SECCIONES EN EL JSON:")
    sections = model_dict.get('sections', {})
    
    for sec_id, sec_info in sections.items():
        print(f"\nSección {sec_id}:")
        print(f"  - Tipo: {sec_info.get('type', 'N/A')}")
        print(f"  - Element_type: {sec_info.get('element_type', 'N/A')}")
        print(f"  - Material: {sec_info.get('material_name', 'N/A')}")
        print(f"  - Transf_tag: {sec_info.get('transf_tag', 'NO_ENCONTRADO')}")
        print(f"  - Datos completos: {sec_info}")
    
    # 4. ANALIZAR ELEMENTOS DEL JSON
    print("\n4. ANÁLISIS DE ELEMENTOS EN EL JSON (primeros 10):")
    elements = model_dict.get('elements', {})
    
    count = 0
    for elem_id, elem_info in elements.items():
        if count >= 10:
            break
        
        elem_type = elem_info.get('type', elem_info.get('element_type', 'N/A'))
        sec_tag = elem_info.get('section_tag', 'N/A')
        
        print(f"\nElemento {elem_id}:")
        print(f"  - Tipo: {elem_type}")
        print(f"  - Section_tag: {sec_tag}")
        print(f"  - Nodos: {elem_info.get('nodes', 'N/A')}")
        
        # Simular lógica del PythonExporter
        if elem_type in ['column', 'beam_x', 'beam_y']:
            section_info = sections.get(str(sec_tag), {})
            transf_tag = section_info.get('transf_tag', 1000)
            print(f"  - Sección encontrada: {section_info}")
            print(f"  - Transf_tag obtenido: {transf_tag}")
        
        count += 1
    
    # 5. SIMULAR LÓGICA EXACTA DEL PYTHONEXPORTER
    print("\n5. SIMULANDO LÓGICA EXACTA DEL PYTHONEXPORTER:")
    
    # Código exacto del PythonExporter
    for elem_id, elem in elements.items():
        elem_type = elem.get('element_type', elem.get('type'))
        if elem_type in ['column', 'beam_x', 'beam_y']:
            nodes = elem['nodes']
            sec_tag = elem['section_tag']
            
            # Esta es la línea exacta del PythonExporter
            transf_tag = sections.get(str(sec_tag), {}).get('transf_tag', 1000)
            
            print(f"\nElemento {elem_id} ({elem_type}):")
            print(f"  - section_tag: {sec_tag} (tipo: {type(sec_tag)})")
            print(f"  - str(sec_tag): '{str(sec_tag)}'")
            print(f"  - sections.get(str(sec_tag)): {sections.get(str(sec_tag))}")
            print(f"  - transf_tag final: {transf_tag}")
            
            # Solo mostrar los primeros 3 elementos
            if int(elem_id) > 20:
                break
    
    # 6. EXPORTAR CON PYTHONEXPORTER
    print("\n6. EXPORTANDO CON PYTHONEXPORTER:")
    
    exporter = PythonExporter("debug_python_exports")
    files = exporter.export_script(model_dict)
    
    print(f"✓ Archivo generado: {files[0]}")
    
    # 7. VERIFICAR ARCHIVO GENERADO
    print("\n7. VERIFICANDO ARCHIVO GENERADO:")
    
    with open(files[0], 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    
    print("\nLíneas con elementos elasticBeamColumn:")
    for i, line in enumerate(lines):
        if 'ops.element(\'elasticBeamColumn\'' in line:
            print(f"  Línea {i+1}: {line.strip()}")
            # Solo mostrar los primeros 5
            if line.count('elasticBeamColumn') >= 5:
                break
    
    # 8. GUARDAR JSON PARA INSPECCIÓN MANUAL
    print("\n8. GUARDANDO JSON PARA INSPECCIÓN MANUAL:")
    
    debug_json_path = "debug_python_exports/debug_model.json"
    os.makedirs(os.path.dirname(debug_json_path), exist_ok=True)
    
    with open(debug_json_path, 'w', encoding='utf-8') as f:
        json.dump(model_dict, f, ensure_ascii=False, indent=2)
    
    print(f"✓ JSON guardado en: {debug_json_path}")
    
    # 9. RESUMEN DEL DIAGNÓSTICO
    print("\n" + "=" * 70)
    print("RESUMEN DEL DIAGNÓSTICO:")
    print("=" * 70)
    
    total_sections = len(sections)
    sections_with_transf = sum(1 for s in sections.values() if 'transf_tag' in s)
    total_elements = len(elements)
    beam_column_elements = sum(1 for e in elements.values() 
                              if e.get('type', e.get('element_type')) in ['column', 'beam_x', 'beam_y'])
    
    print(f"📊 ESTADÍSTICAS:")
    print(f"  - Total secciones: {total_sections}")
    print(f"  - Secciones con transf_tag: {sections_with_transf}")
    print(f"  - Total elementos: {total_elements}")
    print(f"  - Elementos viga/columna: {beam_column_elements}")
    
    print(f"\n🔍 DIAGNÓSTICO:")
    if sections_with_transf == 0:
        print("  ❌ PROBLEMA: Ninguna sección tiene transf_tag en el JSON")
        print("  📋 CAUSA: El problema está en la generación del JSON, no en PythonExporter")
    elif sections_with_transf > 0:
        print("  ✅ Las secciones SÍ tienen transf_tag en el JSON")
        print("  📋 CAUSA: El problema está en la lógica del PythonExporter")
    
    print(f"\n📁 ARCHIVOS GENERADOS:")
    print(f"  - Python: {files[0]}")
    print(f"  - JSON: {debug_json_path}")
    
    print(f"\n💡 SIGUIENTE PASO:")
    print(f"  - Revisar manualmente los archivos generados")
    print(f"  - Identificar si el problema está en ModelBuilder o PythonExporter")

if __name__ == "__main__":
    try:
        debug_transf_tag()
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        import traceback
        traceback.print_exc()
