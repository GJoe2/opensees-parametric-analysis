# Nueva Arquitectura del ModelBuilder

## Resumen

Se ha implementado una arquitectura mejorada para el `ModelBuilder` que sigue los principios de diseño SOLID, especialmente el **Single Responsibility Principle**. La nueva arquitectura separa claramente las responsabilidades entre objetos de dominio y builders especializados.

## Arquitectura

### 1. Domain Objects (Objetos de Dominio)

Los objetos de dominio representan conceptos del mundo real de la ingeniería estructural:

#### `StructuralModel`
- **Propósito**: Representa un modelo estructural completo
- **Responsabilidades**: 
  - Contener todos los componentes del modelo
  - Serialización a JSON
  - Guardado/carga de archivos
  - Resumen del modelo

#### `Geometry`
- **Propósito**: Representa la geometría del modelo
- **Responsabilidades**:
  - Contener nodos y elementos
  - Consultas geométricas (nodos de contorno, por piso, etc.)
  - Cálculos de dimensiones

#### `Sections`
- **Propósito**: Representa las secciones estructurales
- **Responsabilidades**:
  - Contener secciones y transformaciones geométricas
  - Consultas por tipo de elemento

#### `Loads`
- **Propósito**: Representa las cargas del modelo
- **Responsabilidades**:
  - Contener cargas por nodo
  - Consultas por tipo de carga
  - Cálculos totales de carga

#### `AnalysisConfig`
- **Propósito**: Representa la configuración de análisis
- **Responsabilidades**:
  - Configuraciones de análisis estático, modal y dinámico
  - Configuración de visualización
  - Verificación de análisis habilitados

### 2. Specialized Builders (Builders Especializados)

Cada builder tiene una sola responsabilidad y crea un tipo específico de objeto de dominio:

#### `GeometryBuilder`
- **Responsabilidad única**: Crear geometría (nodos y elementos)
- **Métodos**: `create()`, `_create_nodes()`, `_create_elements()`

#### `SectionsBuilder`
- **Responsabilidad única**: Crear secciones y transformaciones
- **Métodos**: `create()`, `_create_sections()`, `_create_transformations()`

#### `LoadsBuilder`
- **Responsabilidad única**: Crear cargas
- **Métodos**: `create()`, `_create_distributed_loads()`, métodos para otros tipos de carga

#### `AnalysisConfigBuilder`
- **Responsabilidad única**: Crear configuraciones de análisis
- **Métodos**: `create()`, métodos para cada tipo de análisis

### 3. ModelBuilder Refactorizado

El `ModelBuilder` ahora actúa como un orquestador que usa los builders especializados:

```python
class ModelBuilder:
    def create_model(self, ...):
        # Orquesta la creación usando builders especializados
        geometry = GeometryBuilder.create(...)
        sections = SectionsBuilder.create(...)
        loads = LoadsBuilder.create(geometry, ...)
        analysis_config = AnalysisConfigBuilder.create(...)
        
        return StructuralModel(geometry, sections, loads, analysis_config, name)
```

## Ventajas de la Nueva Arquitectura

### 1. **Single Responsibility Principle**
- Cada clase tiene una sola razón para cambiar
- Separación clara de responsabilidades

### 2. **Mejor Testabilidad**
- Cada builder se puede testear independientemente
- Domain objects son fáciles de crear para tests
- Mocking es más simple

### 3. **Reutilización**
- Builders pueden reutilizarse en diferentes contextos
- Domain objects pueden extenderse fácilmente

### 4. **Mantenibilidad**
- Cambios en geometría solo afectan `GeometryBuilder`
- Cambios en análisis solo afectan `AnalysisConfigBuilder`
- Código más organizado y legible

### 5. **Expresividad**
- El código es autodocumentado
- Las relaciones entre objetos son claras
- Mejor API para el usuario

## Uso de la Nueva Arquitectura

### Uso Básico

```python
from model_builder_v2 import ModelBuilder

builder = ModelBuilder(output_dir="models")
model = builder.create_model(
    L_B_ratio=1.5,
    B=10.0,
    nx=3,
    ny=2
)
```

### Uso Avanzado con Parámetros Personalizados

```python
model = builder.create_model(
    L_B_ratio=2.0,
    B=12.0,
    nx=4,
    ny=3,
    enabled_analyses=['static', 'modal', 'dynamic'],
    analysis_params={
        'modal': {'num_modes': 10},
        'dynamic': {'dt': 0.005},
        'visualization': {'enabled': True}
    }
)
```

### Uso de Builders Directamente

```python
from builders import GeometryBuilder, SectionsBuilder

# Crear geometría personalizada
geometry = GeometryBuilder.create(
    L_B_ratio=1.5, B=10.0, nx=3, ny=2,
    num_floors=3, floor_height=3.5
)

# Crear secciones personalizadas
sections = SectionsBuilder.create({
    'column_size': (0.50, 0.50),
    'beam_size': (0.30, 0.50)
})
```

### Funciones de los Domain Objects

```python
# Consultas geométricas
boundary_nodes = model.geometry.get_boundary_nodes()
floor_nodes = model.geometry.get_floor_nodes(floor=1)
columns = model.geometry.get_elements_by_type('column')

# Análisis de cargas
total_load = model.loads.get_total_vertical_load()
loaded_nodes = model.loads.get_loaded_nodes()

# Configuración de análisis
is_modal_enabled = model.analysis_config.is_enabled('modal')
modal_config = model.analysis_config.get_solver_config('modal')

# Resumen del modelo
summary = model.get_model_summary()
```

## Migración Gradual

La nueva arquitectura permite migración gradual:

1. **Paso 1**: Usar ambos builders lado a lado
2. **Paso 2**: Migrar componentes específicos
3. **Paso 3**: Actualizar tests gradualmente
4. **Paso 4**: Deprecar builder antiguo

### Script de Migración

Se proporciona un script `migration_test.py` que:
- Compara salidas de ambos builders
- Verifica compatibilidad
- Demuestra nuevas funcionalidades

## Archivos de la Nueva Arquitectura

```
src/
├── domain/                    # Objetos de dominio
│   ├── __init__.py
│   ├── structural_model.py
│   ├── geometry.py
│   ├── sections.py
│   ├── loads.py
│   └── analysis_config.py
├── builders/                  # Builders especializados
│   ├── __init__.py
│   ├── geometry_builder.py
│   ├── sections_builder.py
│   ├── loads_builder.py
│   └── analysis_config_builder.py
├── model_builder.py          # Builder original (mantenido)
└── model_builder_v2.py       # Builder refactorizado
```

## Próximos Pasos

1. **Validación**: Ejecutar tests de migración
2. **Extensión**: Añadir nuevos tipos de análisis
3. **Optimización**: Mejorar performance si es necesario
4. **Documentación**: Expandir ejemplos y guías de uso

## Conclusión

La nueva arquitectura proporciona una base sólida y extensible para el desarrollo futuro del sistema de análisis paramétrico, manteniendo la compatibilidad con el código existente mientras mejora significativamente la organización y mantenibilidad del código.
