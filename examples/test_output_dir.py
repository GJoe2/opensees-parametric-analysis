#!/usr/bin/env python3
"""
Script para probar el comportamiento del directorio de salida del PythonExporter.
"""

import sys
import os

# Agregar el directorio src al path para importar el módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from python_exporter import PythonExporter

def test_output_directories():
    """Prueba diferentes configuraciones de directorio de salida."""
    
    print("=== Test de Directorios de Salida ===")
    print(f"Directorio de trabajo actual: {os.getcwd()}")
    print(f"Ubicación de este script: {os.path.dirname(os.path.abspath(__file__))}")
    print()
    
    # Test 1: Sin especificar directorio (por defecto)
    print("1. Sin especificar directorio (por defecto):")
    exporter1 = PythonExporter()
    print(f"   Directorio de salida: {exporter1.output_dir}")
    expected1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "python_exports")
    print(f"   Esperado: {expected1}")
    print(f"   ✓ Correcto: {exporter1.output_dir == expected1}")
    print()
    
    # Test 2: Ruta relativa
    print("2. Con ruta relativa 'mi_output':")
    exporter2 = PythonExporter(output_dir="mi_output")
    print(f"   Directorio de salida: {exporter2.output_dir}")
    expected2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mi_output")
    print(f"   Esperado: {expected2}")
    print(f"   ¿Es ruta absoluta? {os.path.isabs(exporter2.output_dir)}")
    print(f"   ✓ Correcto: {exporter2.output_dir == expected2}")
    print()
    
    # Test 3: Ruta relativa con subdirectorios
    print("3. Con ruta relativa 'outputs/modelos':")
    exporter3 = PythonExporter(output_dir="outputs/modelos")
    print(f"   Directorio de salida: {exporter3.output_dir}")
    expected3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "modelos")
    print(f"   Esperado: {expected3}")
    print(f"   ¿Es ruta absoluta? {os.path.isabs(exporter3.output_dir)}")
    print(f"   ✓ Correcto: {exporter3.output_dir == expected3}")
    print()
    
    # Test 4: Ruta absoluta (no debe cambiar)
    print("4. Con ruta absoluta:")
    abs_path = os.path.join(os.path.dirname(__file__), "test_absolute")
    exporter4 = PythonExporter(output_dir=abs_path)
    print(f"   Directorio de salida: {exporter4.output_dir}")
    print(f"   Esperado: {abs_path}")
    print(f"   ¿Es ruta absoluta? {os.path.isabs(exporter4.output_dir)}")
    print(f"   ✓ Correcto: {exporter4.output_dir == abs_path}")
    print()
    
    # Test 5: Verificar que funciona desde diferentes ubicaciones
    print("5. Test desde directorio diferente:")
    original_cwd = os.getcwd()
    try:
        # Cambiar al directorio padre temporalmente
        parent_dir = os.path.dirname(os.getcwd())
        os.chdir(parent_dir)
        print(f"   Cambiado a: {os.getcwd()}")
        
        # El directorio de salida aún debe ser relativo al script, no al cwd actual
        exporter5 = PythonExporter(output_dir="test_from_parent")
        expected5 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_from_parent")
        print(f"   Directorio de salida: {exporter5.output_dir}")
        print(f"   Esperado: {expected5}")
        print(f"   ✓ Correcto: {exporter5.output_dir == expected5}")
        
    finally:
        os.chdir(original_cwd)
    
    print("\n=== Resumen ===")
    print("La corrección asegura que:")
    print("- Las rutas relativas se interpretan desde la ubicación del archivo Python que llama")
    print("- No desde el directorio de trabajo actual (cwd)")
    print("- Las rutas absolutas se mantienen sin cambios")

if __name__ == "__main__":
    test_output_directories()
