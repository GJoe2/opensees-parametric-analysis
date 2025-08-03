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

Sistema completo de análisis paramétrico para estructuras de hormigón armado usando OpenSees. Arquitectura modular refactorizada que permite análisis estático, modal y dinámico con control granular de visualización.

## ✨ Características Principales

- **Geometría**: Estructuras rectangulares con relación L/B variable
- **Elementos**: Columnas 40x40 cm, vigas 25x40 cm, losa de 10 cm  
- **Pisos**: 2 pisos de 3 m cada uno
- **Análisis**: Estático, modal y dinámico
- **Visualización**: Control granular con opstool
- **Post-procesamiento**: Reportes automáticos y visualizaciones interactivas
## 🚀 Inicio Rápido

### Instalación
```bash
# Opción 1: Desde PyPI (cuando esté publicado)
pip install opensees-parametric-analysis

# Opción 2: Desde código fuente
git clone https://github.com/GJoe2/opensees-parametric-analysis.git
cd opensees-parametric-analysis
pip install -r requirements.txt
```

**Requisitos:** 
- Python 3.12+ (requerido por openseespy y opstool)
- **Linux únicamente**: Dependencias del sistema requeridas
  ```bash
  sudo apt-get install -y libopenblas-dev liblapack-dev libblas-dev gfortran
  ```

📋 **Instalación completa**: Ver [requisitos del sistema](docs/system-requirements.md)

### Uso Básico
```python
# Si instalaste desde PyPI
from opensees_parametric_analysis import ModelBuilder, AnalysisEngine

# Si usas código fuente
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