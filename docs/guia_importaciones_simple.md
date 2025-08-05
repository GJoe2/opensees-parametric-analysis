# 📋 Guía Simple de Importaciones - OpenSees Parametric Analysis

## ✅ Solución Final Simplificada

### Para Scripts Fuera de `src/` (Ejemplos, Tests, Notebooks)

```python
import sys
import os

# ⭐ LÍNEA MÁGICA - Agregar src al path
sys.path.insert(0, 'src')  # o la ruta relativa a src/

# 🎯 Importar normalmente
from model_builder import ModelBuilder
from analysis_engine import AnalysisEngine
from domain.structural_model import StructuralModel
from builders.geometry_builder import GeometryBuilder
```

### Para Código Dentro de `src/`
✅ **Las importaciones relativas funcionan perfectamente como están:**
```python
from .domain.structural_model import StructuralModel
from ..utils.analysis_types import StaticAnalysis
```

### Para Paquete Publicado (Futuro)
```bash
pip install opensees-parametric-analysis
```
```python
from opensees_parametric_analysis import ModelBuilder, AnalysisEngine
from opensees_parametric_analysis.domain import StructuralModel
```

## 📁 Estructura de Archivos con Fallbacks

Los archivos principales ahora tienen **fallbacks automáticos**:

- `analysis_engine.py` ✅
- `model_builder.py` ✅  
- `utils/analysis_types.py` ✅

Esto significa que funcionan tanto:
- Como parte del paquete (importaciones relativas)
- Importados directamente (importaciones absolutas con fallback)

## 🔧 Ejemplo Completo Funcionando

```python
# examples/mi_script.py
import sys
sys.path.insert(0, 'src')

from model_builder import ModelBuilder
from analysis_engine import AnalysisEngine

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

print(f"✅ Análisis completado: {results.success}")
```

## 🏆 Ventajas de Esta Solución

✅ **Simple**: Una línea para habilitar importaciones  
✅ **Consistente**: Mismo patrón en todos los scripts  
✅ **Robusto**: Fallbacks automáticos en los módulos principales  
✅ **Futuro-compatible**: Preparado para publicación como paquete  
✅ **IDE-friendly**: Funciona con autocompletado una vez ejecutado  

## 📝 Template para Copiar y Pegar

```python
"""
Mi script usando opensees-parametric-analysis
"""
import sys
sys.path.insert(0, 'src')  # 🔥 Línea obligatoria

# Tus importaciones aquí
from model_builder import ModelBuilder
from analysis_engine import AnalysisEngine

# Tu código aquí
def main():
    builder = ModelBuilder()
    engine = AnalysisEngine()
    # ... resto de tu código

if __name__ == "__main__":
    main()
```

## 🚀 ¡Listo para usar!

Con esta configuración, puedes:
- Crear scripts en `examples/`
- Escribir tests en `tests/`
- Trabajar en notebooks en `notebooks/`
- Todo con las mismas importaciones simples

**Solo recuerda agregar `sys.path.insert(0, 'src')` al inicio de cada script.**
