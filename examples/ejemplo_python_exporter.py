"""
Ejemplo completo: ModelBuilder -> PythonExporter -> JSON
=======================================================

Este ejemplo demuestra el flujo completo:
1. Crear un modelo usando ModelBuilder
2. Exportar el modelo a script Python usando PythonExporter
3. Exportar el modelo a JSON para verificación

Autor: GitHub Copilot
Fecha: 2025
"""
import os
import json

from opsparametric import ModelBuilder
from opsparametric import PythonExporter

def main():
    print("=" * 60)
    print("Ejemplo: ModelBuilder -> PythonExporter -> JSON")
    print("=" * 60)
    
    # 1. CREAR MODELO CON MODELBUILDER
    print("\n1. Creando modelo con ModelBuilder...")
    builder = ModelBuilder()
    
    # Configurar material
    builder.update_material_params(
        name='Concreto_C25',
        E=2.8e10,  # 28 GPa (Concreto C25)
        nu=0.2,    # Coeficiente de Poisson
        rho=2500   # Densidad kg/m³
    )
    
    # Crear modelo de edificio de 3 pisos
    modelo = builder.create_model(
        L_B_ratio=12.0/9.0,  # Relación L/B
        B=9.0,               # 9 metros de ancho
        nx=3,                # 4 ejes en X (3 vanos)
        ny=2,                # 3 ejes en Y (2 vanos)
        model_name="Edificio_3P",
        enabled_analyses=['static', 'modal'],
        analysis_params={
            'static': {'steps': 20},
            'modal': {'num_modes': 10}
        }
    )
    
    # También necesitamos agregar parámetros de piso que probablemente sean fixed_params
    builder.update_fixed_params(
        num_floors=3,
        floor_height=3.5
    )
    
    # Recrear modelo con parámetros actualizados
    modelo = builder.create_model(
        L_B_ratio=12.0/9.0,
        B=9.0,
        nx=3,
        ny=2,
        model_name="Edificio_3P",
        enabled_analyses=['static', 'modal'],
        analysis_params={
            'static': {'steps': 20},
            'modal': {'num_modes': 10}
        }
    )
    
    print(f"✓ Modelo creado: {modelo.name}")
    
    # Convertir a diccionario para inspección
    modelo_dict = modelo.to_dict()
    print(f"  - Dimensiones: {modelo_dict['parameters']['L']}x{modelo_dict['parameters']['B']} m")
    print(f"  - Pisos: {modelo_dict['parameters']['num_floors']}")
    print(f"  - Elementos: {len(modelo_dict.get('elements', {}))} elementos")
    print(f"  - Material: {modelo_dict['material']['name']}")
    
    # 2. EXPORTAR A PYTHON USANDO PYTHONEXPORTER
    print("\n2. Exportando modelo a Python...")
    
    # Inicializar PythonExporter con ruta relativa
    # El PythonExporter se encargará de crear el directorio en la ubicación correcta
    exporter = PythonExporter(output_dir="python_exports")
    
    # Exportar en modo archivo único (modelo + análisis)
    print("   Exportando archivo combinado...")
    archivos_combinados = exporter.export_script(modelo_dict, separate_files=False)
    
    # Exportar en modo archivos separados
    print("   Exportando archivos separados...")
    archivos_separados = exporter.export_script(modelo_dict, separate_files=True)
    
    print(f"✓ Archivos Python generados:")
    print(f"  - Archivo combinado: {archivos_combinados[0]}")
    for archivo in archivos_separados:
        print(f"  - Archivo separado: {archivo}")
    
    # 3. EXPORTAR MODELO A JSON
    print("\n3. Exportando modelo a JSON...")
    
    # Usar la funcionalidad de exportación de ModelBuilder
    json_file = builder.export_model(modelo, output_dir="json_exports")
    
    print(f"✓ Archivo JSON generado: {json_file}")
    
    # 4. VERIFICAR CONTENIDO DEL JSON
    print("\n4. Verificando contenido del JSON...")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        modelo_json = json.load(f)
    
    print(f"✓ Estructura del JSON:")
    for clave in modelo_json.keys():
        if isinstance(modelo_json[clave], dict):
            print(f"  - {clave}: {len(modelo_json[clave])} elementos")
        elif isinstance(modelo_json[clave], list):
            print(f"  - {clave}: lista con {len(modelo_json[clave])} elementos")
        else:
            print(f"  - {clave}: {modelo_json[clave]}")
    
    # 5. MOSTRAR MUESTRA DEL CÓDIGO PYTHON GENERADO
    print("\n5. Muestra del código Python generado:")
    print("-" * 40)
    
    with open(archivos_combinados[0], 'r', encoding='utf-8-sig') as f:
        lineas = f.readlines()
    
    # Mostrar las primeras 20 líneas
    for i, linea in enumerate(lineas[:20], 1):
        print(f"{i:2d}: {linea.rstrip()}")
    
    if len(lineas) > 20:
        print(f"... (archivo completo tiene {len(lineas)} líneas)")
    
    print("\n6. Resumen:")
    print("-" * 40)
    print(f"✓ Modelo creado con {len(modelo_dict.get('elements', {}))} elementos")
    print(f"✓ Material: {modelo_dict['material']['name']} (E={modelo_dict['material']['E']:.1e} Pa)")
    print(f"✓ Análisis configurado: {', '.join(modelo_dict['analysis_config']['enabled_analyses'])}")
    print(f"✓ Archivos Python: {len(archivos_combinados + archivos_separados)} archivos")
    print(f"✓ Archivo JSON: {os.path.basename(json_file)}")
    
    print("\n" + "=" * 60)
    print("¡Ejemplo completado exitosamente!")
    print("Revisa las carpetas 'python_exports' y 'json_exports'")
    print("=" * 60)

if __name__ == "__main__":
    main()
