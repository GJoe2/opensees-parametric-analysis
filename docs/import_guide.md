# Guía de Importaciones - OpenSees Parametric Analysis

## Resumen
Este documento explica cómo importar y usar las clases del paquete tanto en desarrollo como en producción.

## 1. En Desarrollo Local

### Instalación en Modo Desarrollo
```bash
# Desde el directorio raíz del proyecto
pip install -e .
```

### Importaciones Principales
```python
# Clases principales
from opensees_parametric_analysis import ModelBuilder, AnalysisEngine

# Objetos de dominio
from opensees_parametric_analysis.domain import (
    StructuralModel, 
    Geometry, 
    Sections, 
    Loads, 
    AnalysisConfig
)

# Builders específicos
from opensees_parametric_analysis.builders import (
    GeometryBuilder,
    SectionsBuilder, 
    LoadsBuilder,
    AnalysisConfigBuilder
)

# Utilidades
from opensees_parametric_analysis.utils import (
    VisualizationHelper,
    ModelHelpers
)
```

## 2. En Producción (Paquete Publicado)

### Instalación
```bash
pip install opensees-parametric-analysis
```

### Importaciones (Idénticas a desarrollo)
```python
# ¡Las mismas importaciones que en desarrollo!
from opensees_parametric_analysis import ModelBuilder, AnalysisEngine
from opensees_parametric_analysis.domain import StructuralModel
```

## 3. Ejemplo de Uso Completo

### Caso Simple
```python
from opensees_parametric_analysis import ModelBuilder, AnalysisEngine

# Crear modelo
builder = ModelBuilder()
model = builder.create_concrete_frame_model(
    geometry_params={'stories': 3, 'bays': 2},
    section_params={'beam_width': 0.4, 'beam_height': 0.6},
    load_params={'dead_load': 10.0, 'live_load': 5.0}
)

# Analizar
engine = AnalysisEngine()
results = engine.analyze_model(model)

print(f"Análisis completado: {results.success}")
```

### Caso Avanzado
```python
from opensees_parametric_analysis import ModelBuilder
from opensees_parametric_analysis.builders import (
    GeometryBuilder, 
    SectionsBuilder, 
    LoadsBuilder, 
    AnalysisConfigBuilder
)

# Construcción paso a paso
geometry = GeometryBuilder().create_frame_geometry(stories=5, bays=3)
sections = SectionsBuilder().create_concrete_sections()
loads = LoadsBuilder().create_gravity_loads()
config = AnalysisConfigBuilder().create_static_analysis()

# Ensamblar modelo
builder = ModelBuilder()
model = builder.build_model(
    name="edificio_5_pisos",
    geometry=geometry,
    sections=sections, 
    loads=loads,
    analysis_config=config
)
```

## 4. Ventajas de Este Enfoque

✅ **Consistencia**: Las mismas importaciones en desarrollo y producción
✅ **Simplicidad**: No hay casos especiales ni fallbacks complicados  
✅ **IDE Support**: Mejor autocompletado y detección de errores
✅ **Testing**: Los tests usan las mismas importaciones que el código de producción
✅ **Distribución**: Funciona automáticamente cuando se publica el paquete

## 5. Estructura del Paquete Instalado

```
opensees_parametric_analysis/
├── __init__.py              # Exporta ModelBuilder, AnalysisEngine
├── model_builder.py
├── analysis_engine.py
├── domain/
│   ├── __init__.py         # Exporta clases de dominio
│   ├── structural_model.py
│   ├── geometry.py
│   └── ...
├── builders/
│   ├── __init__.py         # Exporta builders
│   └── ...
└── utils/
    ├── __init__.py         # Exporta utilidades
    └── ...
```

## 6. Scripts de Ejemplo

Ver los archivos en `examples/` para casos de uso completos.
