# 📊 Parámetros del Modelo

## Parámetros Fijos

### Geometría Estructural
- **Columnas**: 40×40 cm
- **Vigas**: 25×40 cm  
- **Losa**: 10 cm de espesor
- **Altura de piso**: 3.0 m
- **Número de pisos**: 2

### Propiedades del Material
- **Módulo de elasticidad**: E = 15000√210 × 0.001/0.01² tonf/m²
- **Coeficiente de Poisson**: ν = 0.2
- **Densidad**: ρ = 2.4/9.81 tonf·s²/m⁴

### Cargas
- **Carga distribuida**: 1 tonf/m² en el último piso
- **Tipo de carga**: Distribuida uniformemente
- **Aplicación**: Solo en losa del piso superior

## Parámetros Variables

### Geometría del Edificio

| Parámetro | Símbolo | Valores | Unidad | Descripción |
|-----------|---------|---------|--------|-------------|
| **Relación L/B** | L_B_ratio | 1.0, 1.5, 2.0, 2.5 | - | Relación longitud/ancho |
| **Ancho** | B | 5.0, 10.0, 15.0, 20.0 | m | Ancho de la estructura |
| **Ejes en X** | nx | 3, 4, 5, 6 | - | Número de ejes estructurales en X |
| **Ejes en Y** | ny | 2, 3, 4 | - | Número de ejes estructurales en Y |

### Relaciones Derivadas
- **Longitud**: L = L_B_ratio × B
- **Separación en X**: sx = L / (nx - 1)
- **Separación en Y**: sy = B / (ny - 1)

## Convención de Nombres

### Formato de Nomenclatura
Los modelos se nombran siguiendo el patrón: `F01_XX_BB_YYYY`

#### Desglose del Código
- **F01**: Identificador del proyecto (Fijo)
- **XX**: Relación L/B × 10
  - 10 = L/B = 1.0
  - 15 = L/B = 1.5
  - 20 = L/B = 2.0
  - 25 = L/B = 2.5
- **BB**: Ancho B en metros
  - 05 = B = 5m
  - 10 = B = 10m
  - 15 = B = 15m
  - 20 = B = 20m
- **YYYY**: Combinación nx×100 + ny
  - 0302 = nx=3, ny=2
  - 0403 = nx=4, ny=3
  - 0504 = nx=5, ny=4
  - 0604 = nx=6, ny=4

### Ejemplos de Nomenclatura

| Modelo | L/B | B(m) | nx | ny | L(m) | Descripción |
|--------|-----|------|----|----|------|-------------|
| F01_10_10_0302 | 1.0 | 10 | 3 | 2 | 10 | Edificio cuadrado 10×10m, 3×2 ejes |
| F01_15_10_0403 | 1.5 | 10 | 4 | 3 | 15 | Edificio rectangular 15×10m, 4×3 ejes |
| F01_20_15_0504 | 2.0 | 15 | 5 | 4 | 30 | Edificio rectangular 30×15m, 5×4 ejes |
| F01_25_20_0604 | 2.5 | 20 | 6 | 4 | 50 | Edificio rectangular 50×20m, 6×4 ejes |

## Configuración de Análisis

### Análisis Estático
```python
'static': {
    'steps': 10,                    # Número de pasos de carga
    'algorithm': 'Linear',          # Algoritmo de solución
    'integrator': 'LoadControl',    # Tipo de integrador
    'tolerance': 1e-6,              # Tolerancia de convergencia
    'max_iterations': 25            # Iteraciones máximas por paso
}
```

### Análisis Modal
```python
'modal': {
    'num_modes': 6,                 # Número de modos a calcular
    'eigen_solver': 'fullGenLapack' # Solver de valores propios
}
```

### Análisis Dinámico
```python
'dynamic': {
    'dt': 0.01,                     # Paso de tiempo (s)
    'num_steps': 1000,              # Número de pasos temporales
    'damping_ratio': 0.05,          # Razón de amortiguamiento
    'integrator': 'Newmark',        # Integrador temporal
    'gamma': 0.5,                   # Parámetro gamma de Newmark
    'beta': 0.25                    # Parámetro beta de Newmark
}
```

## Rangos de Validez

### Limitaciones Geométricas

| Parámetro | Mínimo | Máximo | Observaciones |
|-----------|--------|--------|---------------|
| **L/B ratio** | 1.0 | 2.5 | Relaciones extremas pueden causar inestabilidad |
| **B (m)** | 5.0 | 20.0 | Edificios muy grandes requieren más elementos |
| **nx** | 3 | 6 | Mínimo 3 para estabilidad estructural |
| **ny** | 2 | 4 | Mínimo 2 para formar pórtico |

### Consideraciones Estructurales
- **Separación mínima entre ejes**: 2.5 m
- **Separación máxima entre ejes**: 10.0 m
- **Relación altura/ancho**: Máximo 1:5 para estabilidad lateral

## Combinaciones Recomendadas

### Para Estudios Paramétricos Completos
```python
# Combinaciones equilibradas para análisis exhaustivo
L_B_ratios = [1.0, 1.5, 2.0, 2.5]
B_values = [10.0, 15.0]
nx_values = [3, 4, 5]
ny_values = [3, 4]
# Total: 4 × 2 × 3 × 2 = 48 modelos
```

### Para Estudios de Sensibilidad
```python
# Variación de un parámetro manteniendo otros fijos
# Sensibilidad a L/B ratio
L_B_ratios = [1.0, 1.5, 2.0, 2.5]
B_values = [10.0]  # Fijo
nx_values = [4]    # Fijo
ny_values = [3]    # Fijo
# Total: 4 modelos
```

### Para Validación Rápida
```python
# Pocos modelos representativos
L_B_ratios = [1.5, 2.0]
B_values = [10.0, 15.0]
nx_values = [4]
ny_values = [3]
# Total: 2 × 2 × 1 × 1 = 4 modelos
```

## Modificación de Parámetros

### Cambiar Parámetros Fijos
```python
# En model_builder.py
class ModelBuilder:
    def __init__(self):
        self.fixed_params = {
            'column_size': (0.40, 0.40),     # Modificar tamaño de columnas
            'beam_size': (0.25, 0.40),       # Modificar tamaño de vigas
            'slab_thickness': 0.10,          # Modificar espesor de losa
            'story_height': 3.0,             # Modificar altura de piso
            'num_stories': 2,                # Modificar número de pisos
            'load_intensity': 1.0            # Modificar intensidad de carga
        }
```

### Agregar Nuevos Parámetros Variables
```python
# Para agregar un nuevo parámetro (ej: número de pisos)
def create_model_with_stories(self, L_B_ratio, B, nx, ny, num_stories):
    # Modificar método para incluir num_stories como parámetro variable
    # Actualizar nomenclatura: F01_XX_BB_YYYY_SS (SS = num_stories)
    pass
```

## Validación de Parámetros

### Reglas de Validación
```python
def validate_parameters(L_B_ratio, B, nx, ny):
    """Validar que los parámetros estén en rangos aceptables"""
    
    # Validar rangos básicos
    assert 1.0 <= L_B_ratio <= 2.5, "L/B ratio debe estar entre 1.0 y 2.5"
    assert 5.0 <= B <= 20.0, "B debe estar entre 5.0 y 20.0 m"
    assert 3 <= nx <= 6, "nx debe estar entre 3 y 6"
    assert 2 <= ny <= 4, "ny debe estar entre 2 y 4"
    
    # Validar separaciones
    L = L_B_ratio * B
    sx = L / (nx - 1)
    sy = B / (ny - 1)
    
    assert 2.5 <= sx <= 10.0, f"Separación en X ({sx:.1f}m) fuera de rango 2.5-10.0m"
    assert 2.5 <= sy <= 10.0, f"Separación en Y ({sy:.1f}m) fuera de rango 2.5-10.0m"
    
    return True
```
