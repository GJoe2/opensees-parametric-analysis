"""
Verificación de cómo funcionan los métodos múltiples.
"""

from opsparametric import ModelBuilder
import os

builder = ModelBuilder()

# Crear múltiples modelos
param_combos = [
    {'L_B_ratio': 1.5, 'B': 14.0, 'nx': 4, 'ny': 3},
    {'L_B_ratio': 2.0, 'B': 18.0, 'nx': 5, 'ny': 4}
]

print("=== Creando múltiples modelos ===")
models = builder.create_multiple_models(param_combos)

print(f"Número de modelos creados: {len(models)}")
print(f"Tipo del primer elemento: {type(models[0])}")
print(f"Nombres de los modelos:")
for i, model in enumerate(models):
    print(f"  Modelo {i+1}: {model.name}")
    print(f"    L = {model.geometry.L}m, B = {model.geometry.B}m")

print("\n=== Exportando múltiples modelos ===")
exported_files = builder.export_multiple_models(models)

print(f"Archivos exportados: {len(exported_files)}")
for file_path in exported_files:
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path) / 1024  # KB
    print(f"  {file_name} ({file_size:.1f} KB)")

print(f"\n=== Verificando contenido del directorio ===")
output_dir = builder._get_default_output_dir()
if os.path.exists(output_dir):
    files = os.listdir(output_dir)
    print(f"Archivos en {output_dir}:")
    for file in files:
        print(f"  {file}")