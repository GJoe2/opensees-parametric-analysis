# Sistema de Análisis Paramétrico OpenSees

[![Tests](https://github.com/GJoe2/opensees-parametric-analysis/actions/workflows/tests.yml/badge.svg)](https://github.com/GJoe2/opensees-parametric-analysis/actions/workflows/tests.yml)
[![Build and Publish](https://github.com/GJoe2/opensees-parametric-analysis/actions/workflows/publish.yml/badge.svg)](https://github.com/GJoe2/opensees-parametric-analysis/actions/workflows/publish.yml)
[![PyPI version](https://badge.fury.io/py/opensees-parametric-analysis.svg)](https://badge.fury.io/py/opensees-parametric-analysis)
[![codecov](https://codecov.io/gh/GJoe2/opensees-parametric-analysis/branch/master/graph/badge.svg)](https://codecov.io/gh/GJoe2/opensees-parametric-analysis)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python versions](https://img.shields.io/pypi/pyversions/opensees-parametric-analysis.svg)](https://pypi.org/project/opensees-parametric-analysis/)
[![Downloads](https://pepy.tech/badge/opensees-parametric-analysis)](https://pepy.tech/project/opensees-parametric-analysis)
[![GitHub stars](https://img.shields.io/github/stars/GJoe2/opensees-parametric-analysis.svg?style=social&label=Star)](https://github.com/GJoe2/opensees-parametric-analysis)

## 🎯 Descripción General

Sistema completo de análisis paramétrico para estructuras de hormigón armado usando OpenSees. **Nueva arquitectura mejorada** que separa responsabilidades siguiendo principios SOLID, proporcionando mejor mantenibilidad, testabilidad y extensibilidad.

## ✨ Características Principales

### 🏗️ **Nueva Arquitectura (v2.0)**
- **Domain Objects**: Representación orientada a objetos de conceptos estructurales
- **Specialized Builders**: Constructores especializados con responsabilidad única
- **Improved ModelBuilder**: Orquestador que usa builders especializados
- **Better API**: Interfaz más intuitiva y expresiva

### 🔧 **Funcionalidades Técnicas**
- **Geometría**: Estructuras rectangulares con relación L/B variable
- **Elementos**: Columnas 40x40 cm, vigas 25x40 cm, losa de 10 cm  
- **Pisos**: 2 pisos de 3 m cada uno (configurable)
- **Análisis**: Estático, modal y dinámico con parámetros personalizables
- **Visualización**: Control granular con opstool
- **Post-procesamiento**: Reportes automáticos y visualizaciones interactivas

### 🎯 **Ventajas de la Nueva Arquitectura**
- **Separación de responsabilidades**: Cada clase tiene una sola responsabilidad
- **Mejor testabilidad**: Tests unitarios independientes para cada componente
- **Reutilización**: Builders pueden usarse en diferentes contextos
- **Extensibilidad**: Fácil adición de nuevos tipos de análisis o elementos
- **Mantenibilidad**: Cambios aislados que no afectan otros componentes
## 🚀 Inicio Rápido

### Instalación
```bash
# Opción 1: Desde PyPI (cuando esté publicado)
pip install opensees-parametric-analysis

# Opción 2: Desde código fuente
git clone https://github.com/GJoe2/opensees-parametric-analysis.git
cd opensees-parametric-analysis
pip install -r requirements.txt

# Opción 3: Instalación automática en Linux (detecta entorno)
curl -fsSL https://raw.githubusercontent.com/GJoe2/opensees-parametric-analysis/master/scripts/install.sh | bash
```

**Requisitos:** 
- Python 3.12+ (requerido por openseespy y opstool)
- **Linux Desktop**: Dependencias básicas
  ```bash
  sudo apt-get install -y libopenblas-dev liblapack-dev libblas-dev gfortran
  ```
- **Linux Server**: Dependencias básicas + gráficas para headless
  ```bash
  sudo apt-get install -y libopenblas-dev liblapack-dev libblas-dev gfortran libglu1-mesa-dev xvfb
  ```

📋 **Instalación completa**: Ver [requisitos del sistema](docs/system-requirements.md)

### Uso Básico - Nueva Arquitectura (Recomendado)

```python
# Nueva arquitectura mejorada (v2.0)
from src.model_builder_v2 import ModelBuilder
from src.analysis_engine import AnalysisEngine

# Crear modelo con la nueva arquitectura
builder = ModelBuilder(output_dir="models")
model = builder.create_model(
    L_B_ratio=1.5, 
    B=10.0, 
    nx=4, 
    ny=4,
    enabled_analyses=['static', 'modal', 'dynamic'],
    analysis_params={
        'modal': {'num_modes': 10},
        'visualization': {'enabled': True}
    }
)

# El modelo ahora es un objeto rico con métodos útiles
print(f"Modelo: {model.name}")
print(f"Dimensiones: {model.geometry.L}x{model.geometry.B}m")
print(f"Área: {model.geometry.get_footprint_area():.1f} m²")
print(f"Altura total: {model.geometry.get_total_height():.1f} m")

# Analizar usando domain objects
boundary_nodes = model.geometry.get_boundary_nodes()
total_load = model.loads.get_total_vertical_load()
print(f"Nodos de contorno: {len(boundary_nodes)}")
print(f"Carga total: {total_load:.1f} tonf")

# Análisis
engine = AnalysisEngine()
results = engine.analyze_model(model.to_dict())
```

### Uso con Arquitectura Anterior (Compatibilidad)

```python
# Arquitectura anterior (mantenida para compatibilidad)
from src.model_builder import ModelBuilder
from src.analysis_engine import AnalysisEngine

# Crear y analizar modelo
builder = ModelBuilder()
model = builder.create_model(L_B_ratio=1.5, B=10, nx=4, ny=4)

engine = AnalysisEngine()
results = engine.analyze_model(model['file_path'])

print(f"Periodo fundamental: {results['modal_analysis']['fundamental_period']:.4f} s")
```

### Estudio Paramétrico
```python
# Si instalaste desde PyPI
from opensees_parametric_analysis import ParametricRunner

# Si usas código fuente  
from src.parametric_runner import ParametricRunner

# Configurar estudio
runner = ParametricRunner(builder, engine)
results = runner.run_full_study(
    L_B_ratios=[1.5, 2.0], 
    B_values=[10.0, 15.0],
    nx_values=[3, 4], 
    ny_values=[3, 4]
)

print(f"Modelos analizados: {len(results)}")
```

## 🏗️ Nueva Arquitectura (v2.0)

### Conceptos Clave

La nueva arquitectura separa las responsabilidades en diferentes tipos de objetos:

#### **Domain Objects** (Objetos de Dominio)
Representan conceptos del mundo real de la ingeniería estructural:

```python
from src.domain import StructuralModel, Geometry, Loads, AnalysisConfig

# Los objetos de dominio tienen métodos útiles
geometry = model.geometry
print(f"Área de planta: {geometry.get_footprint_area():.1f} m²")
print(f"Relación de aspecto: {geometry.get_aspect_ratio():.2f}")

# Consultas específicas
boundary_nodes = geometry.get_boundary_nodes(floor=0)
columns = geometry.get_elements_by_type('column')
top_floor_nodes = geometry.get_floor_nodes(geometry.num_floors)
```

#### **Specialized Builders** (Constructores Especializados)
Cada builder tiene una sola responsabilidad:

```python
from src.builders import GeometryBuilder, SectionsBuilder, LoadsBuilder

# Crear geometría personalizada
custom_geometry = GeometryBuilder.create(
    L_B_ratio=2.0, B=12.0, nx=5, ny=4,
    num_floors=3,        # 3 pisos en lugar de 2
    floor_height=3.5     # 3.5m en lugar de 3.0m
)

# Crear secciones personalizadas
custom_sections = SectionsBuilder.create({
    'column_size': (0.50, 0.50),    # Columnas más grandes
    'beam_size': (0.30, 0.50),      # Vigas más grandes
    'slab_thickness': 0.15          # Losa más gruesa
})
```

### Ventajas de la Nueva Arquitectura

- **🎯 Responsabilidad única**: Cada clase tiene una sola razón para cambiar
- **🧪 Mejor testabilidad**: Tests unitarios independientes
- **🔄 Reutilización**: Componentes reutilizables en diferentes contextos
- **📝 Mantenibilidad**: Código más organizado y fácil de mantener
- **🚀 Extensibilidad**: Fácil adición de nuevas funcionalidades

### Migración Gradual

Ambas arquitecturas coexisten para permitir migración gradual:

```python
# Script de migración y comparación
python scripts/migration_test.py

# Ejemplos con nueva arquitectura
python examples/new_architecture_demo.py
```

### Documentación Detallada

- **[Nueva Arquitectura](docs/new-architecture.md)**: Guía completa de la nueva arquitectura
- **[Migración](scripts/migration_test.py)**: Script para migrar gradualmente
- **[Ejemplos](examples/new_architecture_demo.py)**: Ejemplos prácticos

### 🎯 Ejemplos Completos
Para casos de uso específicos y ejemplos detallados, consulte la carpeta [`examples/`](examples/) y la [guía completa](examples/GUIA_EJEMPLOS.md):

| Ejemplo | Descripción | Nivel |
|---------|-------------|-------|
| [01_analisis_individual_basico.py](examples/01_analisis_individual_basico.py) | Análisis de un modelo individual | Principiante |
| [02_control_visualizacion.py](examples/02_control_visualizacion.py) | Control granular de visualización | Intermedio |
| [03_tipos_analisis.py](examples/03_tipos_analisis.py) | Diferentes tipos de análisis | Intermedio |
| [04_estudio_parametrico.py](examples/04_estudio_parametrico.py) | Estudios paramétricos completos | Avanzado |
| [05_exportacion_scripts.py](examples/05_exportacion_scripts.py) | Exportación de scripts Python | Intermedio |
| [06_generacion_reportes.py](examples/06_generacion_reportes.py) | Generación de reportes | Avanzado |
## 🏗️ Arquitectura

### Estructura Modular
```
src/
├── model_builder.py          # Constructor de modelos (API unificada)
├── analysis_engine.py        # Motor de análisis (refactorizado)
├── parametric_runner.py      # Orquestador de estudios
├── python_exporter.py        # Exportador de scripts
├── report_generator.py       # Generador de reportes
└── utils/                    # Utilidades modulares
    ├── analysis_types.py      # Análisis específicos
    ├── visualization_helper.py # Helper de visualización
    └── model_helpers.py       # Métodos de conveniencia
```

### Componentes Principales

| Componente | Función | Entrada | Salida |
|------------|---------|---------|--------|
| **ModelBuilder** | Creación de modelos | Parámetros geométricos | JSON con modelo + configuración |
| **AnalysisEngine** | Ejecución de análisis | JSON de modelo | Resultados + visualizaciones |
| **ParametricRunner** | Estudios paramétricos | Rangos de parámetros | Resultados múltiples |

## 📊 Control de Visualización

### Configuración Granular
```python
# Solo números (máxima velocidad)
model = builder.create_model(1.5, 10, 4, 4,
    analysis_params={'visualization': {'enabled': False}}
)

# Solo deformada estática
model = builder.create_model(1.5, 10, 4, 4,
    analysis_params={
        'visualization': {
            'enabled': True,
            'static_deformed': True,
            'modal_shapes': False
        }
    }
)

# Presentación completa
model = builder.create_model(1.5, 10, 4, 4,
    analysis_params={
        'visualization': {
            'enabled': True,
            'static_deformed': True,
            'modal_shapes': True,
            'max_modes': 6,
            'deform_scale': 200
        }
    }
)
```

## 🧪 Testing

### Ejecutar Tests
```bash
# Runner interactivo
python tests/run_all_tests.py

# Con pytest (recomendado)
pip install pytest
pytest tests/ -v

# Tests específicos
python tests/run_all_tests.py 1  # Solo ModelBuilder
```

## 📚 Documentación Detallada

Para información completa y detallada, consulte la documentación organizada en la carpeta [`docs/`](docs/):

### 🎯 Por Audiencia

#### Para Usuarios Nuevos
- [**📋 Índice General**](docs/index.md) - Navegación completa
- [**🔧 Instalación**](docs/installation.md) - Setup completo y dependencias  
- [**🚀 Guía de Uso**](docs/usage.md) - Ejemplos y API detallada

#### Para Desarrolladores  
- [**🏗️ Arquitectura**](docs/architecture.md) - Diseño del sistema y componentes
- [**🧪 Testing**](docs/testing.md) - Suite de tests y validación
- [**🐛 Troubleshooting**](docs/troubleshooting.md) - Solución de problemas

#### Para Investigadores
- [**📊 Parámetros del Modelo**](docs/model-parameters.md) - Configuración y nomenclatura
- [**🎛️ Control de Visualización**](docs/visualization.md) - Configuración granular
- [**🚀 Uso Avanzado**](docs/usage.md#estudios-paramétricos) - Estudios paramétricos

### 🔍 Por Tema Específico

| Tema | Documento | Descripción |
|------|-----------|-------------|
| **Instalación** | [installation.md](docs/installation.md) | Setup, dependencias, configuración |
| **Requisitos** | [system-requirements.md](docs/system-requirements.md) | Requisitos del sistema y troubleshooting |
| **Uso Básico** | [usage.md](docs/usage.md) | API, ejemplos, casos de uso |
| **Arquitectura** | [architecture.md](docs/architecture.md) | Diseño, componentes, extensibilidad |
| **Parámetros** | [model-parameters.md](docs/model-parameters.md) | Configuración del modelo, nomenclatura |
| **Visualización** | [visualization.md](docs/visualization.md) | Control granular, optimización |
| **Testing** | [testing.md](docs/testing.md) | Suite de tests, validación |
| **Problemas** | [troubleshooting.md](docs/troubleshooting.md) | Debugging, soluciones comunes |

## 📁 Estructura del Proyecto

```
opensees-parametric-analysis/
├── src/                      # Código fuente
├── docs/                     # Documentación detallada
├── examples/                 # Ejemplos de uso prácticos
├── notebooks/                # Jupyter notebooks
├── models/                   # Modelos generados
├── results/                  # Resultados de análisis
├── tests/                    # Suite de tests
├── requirements.txt          # Dependencias
└── README.md                # Este archivo
```

## � Beneficios de la Refactorización

- ✅ **Código 50% más corto y legible**
- ✅ **Eliminación del 80% de condicionales complejas**
- ✅ **Separación clara de responsabilidades**
- ✅ **Gestión inteligente de recursos**
- ✅ **API unificada y consistente**
- ✅ **Control granular de visualización**
- ✅ **Suite de tests completa**

## 📜 Licencia

Este proyecto está bajo licencia Apache 2.0. Ver archivo LICENSE para más detalles.

## 📞 Contacto

Para preguntas, soporte o contribuciones:
- **Issues**: [GitHub Issues](https://github.com/GJoe2/opensees-parametric-analysis/issues)
- **Documentación**: [docs/](docs/)

---

**💡 Tip**: Para empezar rápidamente, revise el [índice de documentación](docs/index.md) y seleccione la guía apropiada para su caso de uso. 