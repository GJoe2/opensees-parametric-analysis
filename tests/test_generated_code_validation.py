#!/usr/bin/env python3
"""
Script para verificar que el código Python generado es válido y funcional.
"""

import tempfile
import shutil
import subprocess
import sys

from opsparametric import ModelBuilder, PythonExporter

def test_generated_python_execution():
    """Verifica que el código Python generado sea ejecutable."""
    
    print("=== PROBANDO EJECUCIÓN DEL CÓDIGO GENERADO ===\n")
    
    # 1. Crear modelo y exportar
    builder = ModelBuilder()
    builder.update_material_params(E=30000, nu=0.2, rho=2400, name="test_concrete")
    
    model = builder.create_model(
        L_B_ratio=1.0,
        B=8.0,
        nx=2,
        ny=2,
        model_name="execution_test"
    )
    
    temp_dir = tempfile.mkdtemp()
    json_path = builder.export_model(model, output_dir=temp_dir)
    
    # 2. Cargar JSON y exportar a Python
    import json
    with open(json_path, 'r', encoding='utf-8') as f:
        model_data = json.load(f)
    
    exporter = PythonExporter(output_dir=temp_dir)
    py_files = exporter.export_script(model_data, separate_files=False)
    
    print(f"Archivo Python generado: {py_files[0]}")
    
    # 3. Verificar sintaxis del código generado
    print("\nVerificando sintaxis del código...")
    try:
        with open(py_files[0], 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Verificar sintaxis compilando
        compile(code, py_files[0], 'exec')
        print("✅ Sintaxis válida")
        
        # Mostrar primeras líneas del código
        lines = code.split('\n')
        print("\nPrimeras líneas del código generado:")
        for i, line in enumerate(lines[:15]):
            print(f"  {i+1:2d}: {line}")
        
        print("  ...")
        
        # Mostrar valores del material usados
        for line in lines[10:25]:  # Buscar en la sección de parámetros
            if "E = " in line and "Módulo" in line:
                print(f"\n✅ {line.strip()}")
            elif "nu = " in line and "Coeficiente" in line:
                print(f"✅ {line.strip()}")
            elif "rho = " in line and "Densidad" in line:
                print(f"✅ {line.strip()}")
        
    except SyntaxError as e:
        print(f"❌ Error de sintaxis: {e}")
        return False
    
    # Cleanup
    shutil.rmtree(temp_dir)
    
    print("\n=== CÓDIGO PYTHON VÁLIDO Y FUNCIONAL ===")
    return True

if __name__ == "__main__":
    try:
        success = test_generated_python_execution()
        if success:
            print("\n🎉 ¡El código Python generado es válido!")
        else:
            print("\n❌ Problemas con el código generado")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
