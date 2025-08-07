#!/usr/bin/env python3
"""
Test para verificar compatibilidad del PythonExporter con la nueva estructura JSON.
"""

import sys
import os
import json
import tempfile
import shutil

from opsparametric import ModelBuilder, PythonExporter

def test_python_exporter_compatibility():
    """Verifica que PythonExporter funcione con la nueva estructura JSON."""
    
    print("=== PROBANDO COMPATIBILIDAD DE PYTHON EXPORTER ===\n")
    
    # 1. Crear modelo con la nueva estructura
    print("1. Creando modelo con nueva estructura...")
    builder = ModelBuilder()
    
    # Actualizar material
    builder.update_material_params(
        E=25000,
        nu=0.25,
        rho=2500,
        name="test_concrete"
    )
    
    # Crear modelo
    model = builder.create_model(
        L_B_ratio=1.2,
        B=10.0,
        nx=3,
        ny=2,
        model_name="export_test_model"
    )
    
    # Exportar como JSON
    temp_dir = tempfile.mkdtemp()
    json_path = builder.export_model(model, output_dir=temp_dir)
    
    print(f"   Modelo JSON exportado: {json_path}")
    
    # 2. Cargar el JSON y verificar estructura
    print("\n2. Verificando estructura del JSON...")
    with open(json_path, 'r', encoding='utf-8') as f:
        model_data = json.load(f)
    
    print(f"   Claves principales: {list(model_data.keys())}")
    
    # Verificar que tiene la nueva sección 'material'
    if 'material' in model_data:
        print(f"   ✅ Sección 'material' presente: {model_data['material']}")
    else:
        print("   ❌ Falta sección 'material'")
        return False
    
    # 3. Probar PythonExporter con el JSON
    print("\n3. Probando PythonExporter...")
    
    try:
        exporter = PythonExporter(output_dir=temp_dir)
        
        # Exportar como script Python
        py_files = exporter.export_script(model_data, separate_files=False)
        print(f"   ✅ Archivos Python generados: {py_files}")
        
        # Verificar que el archivo se creó
        for py_file in py_files:
            if os.path.exists(py_file):
                print(f"   ✅ Archivo creado: {os.path.basename(py_file)}")
                
                # Leer parte del código generado para verificar que se ve correcto
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Verificar que tiene elementos esperados
                if 'def build_model():' in content:
                    print("   ✅ Función build_model() presente")
                else:
                    print("   ❌ Falta función build_model()")
                
                if 'ops.node(' in content:
                    print("   ✅ Creación de nodos presente")
                else:
                    print("   ❌ No se encontró creación de nodos")
                    
                if 'ops.element(' in content:
                    print("   ✅ Creación de elementos presente")
                else:
                    print("   ❌ No se encontró creación de elementos")
                    
                # Verificar que usa los parámetros del material correctamente
                material_data = model_data['material']
                E_value = material_data['E']
                if f"E = {E_value}" in content:
                    print(f"   ✅ Módulo E del material usado: {E_value}")
                else:
                    print(f"   ⚠️  Módulo E podría no estar siendo usado correctamente")
            else:
                print(f"   ❌ Archivo no creado: {py_file}")
                
    except Exception as e:
        print(f"   ❌ Error en PythonExporter: {e}")
        return False
    
    # 4. Probar con archivos separados
    print("\n4. Probando con archivos separados...")
    try:
        py_files_sep = exporter.export_script(model_data, separate_files=True)
        print(f"   ✅ Archivos separados generados: {[os.path.basename(f) for f in py_files_sep]}")
    except Exception as e:
        print(f"   ❌ Error con archivos separados: {e}")
        return False
    
    # Cleanup
    shutil.rmtree(temp_dir)
    
    print("\n=== COMPATIBILIDAD VERIFICADA ===")
    return True

if __name__ == "__main__":
    try:
        success = test_python_exporter_compatibility()
        if success:
            print("\n🎉 ¡PythonExporter es compatible con la nueva estructura!")
        else:
            print("\n❌ Se encontraron incompatibilidades")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
