"""
Ejemplo de uso de ModelBuilder con sus principales características.
"""

from opsparametric import ModelBuilder

builder = ModelBuilder(output_dir="models_output")

# Actualizar parámetros fijos (opcional)
builder.update_fixed_params(num_floors=3, floor_height=3.5)

# Crear un modelo estructural con parámetros personalizados
model = builder.create_model(
    L_B_ratio=1.5,
    B=12.0,
    nx=4,
    ny=3,
    enabled_analyses=['static', 'modal', 'dynamic'],
    analysis_params={'modal': {'num_modes': 8}, 'dynamic': {'dt': 0.01}}
)

# Exportar el modelo a archivo JSON
builder.export_model(model)

# Obtener resumen del modelo
summary = builder.get_model_summary(model)
print("Resumen del modelo:")
for k, v in summary.items():
    print(f"{k}: {v}")

# Crear múltiples modelos con diferentes combinaciones de parámetros
param_combos = [
    {'L_B_ratio': 1.2, 'B': 10.0, 'nx': 3, 'ny': 2},
    {'L_B_ratio': 2.0, 'B': 15.0, 'nx': 5, 'ny': 4, 'enabled_analyses': ['static']}
]
models = builder.create_multiple_models(param_combos)
for m in models:
    builder.export_model(m)
    print("Modelo exportado:", m.name)
