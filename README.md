# Sistema de Análisis Paramétrico OpenSees - Documentación Completa

## 🎯 Descripción General

Este proyecto implementa un sistema completo de análisis paramétrico para estructuras de hormigón armado usando OpenSees. El sistema está diseñado para analizar la influencia de diferentes parámetros geométricos en el comportamiento estructural mediante una arquitectura modular y refactorizada que prioriza el código limpio y mantenible.

## ✨ Características Principales

- **Geometría**: Estructuras rectangulares con relación L/B variable
- **Elementos**: Columnas 40x40 cm, vigas 25x40 cm, losa de 10 cm
- **Pisos**: 2 pisos de 3 m cada uno
- **Análisis**: Estático, modal y dinámico
- **Visualización**: Control granular con opstool
- **Post-procesamiento**: Reportes automáticos y visualizaciones interactivas

## 🏗️ Arquitectura del Sistema (Refactorizada)

### Estructura de Archivos
```
Prototipo/
├── src/                                    # Código fuente principal
│   ├── __init__.py
│   ├── model_builder.py                    # Constructor de modelos (API unificada)
│   ├── analysis_engine_refactored.py       # Motor de análisis (refactorizado)
│   ├── parametric_runner.py                # Orquestador de estudios
│   ├── python_exporter.py                  # Exportador de scripts
│   ├── report_generator.py                 # Generador de reportes
│   └── utils/                              # Utilidades modulares
│       ├── analysis_types.py               # Análisis específicos (Static, Modal, Dynamic)
│       ├── visualization_helper.py         # Helper de visualización
│       └── model_helpers.py                # Métodos de conveniencia
├── notebooks/                              # Jupyter notebooks
│   ├── 00_verificacion_instalacion.ipynb
│   ├── 01_crear_modelos.ipynb
│   ├── 02_analizar_modelo_individual.ipynb
│   ├── 03_analisis_parametrico_completo.ipynb
│   └── 04_generar_reportes.ipynb
├── models/                                 # Modelos generados
├── results/                                # Resultados de análisis
├── reports/                                # Reportes generados
├── requirements.txt                        # Dependencias
└── README.md                               # Esta documentación
```

### Separación de Responsabilidades

#### 🏗️ **ModelBuilder** (Constructor de Modelos)
- **Función**: Generador de modelos con API unificada
- **Entrada**: Parámetros geométricos (L_B_ratio, B, nx, ny)
- **Salida**: Archivos JSON con modelo + configuración de análisis embebida
- **Característica**: Control granular de análisis y visualización

#### ⚙️ **AnalysisEngine** (Motor de Análisis Refactorizado)
- **Función**: Ejecutor puro de análisis con arquitectura modular
- **Entrada**: Archivos JSON de modelo
- **Salida**: Resultados de análisis
- **Mejoras**: Código 50% más corto, eliminación de condicionales complejas, gestión inteligente de recursos

#### 🎯 **ParametricRunner** (Orquestador)
- **Función**: Orquestador de estudios paramétricos
- **Entrada**: Rangos de parámetros + estrategia de distribución
- **Salida**: Estudios completos con reportes
- **Configuración**: Define estrategias de asignación de análisis

#### 📝 **PythonExporter** (Exportador)
- **Función**: Exportador de scripts Python ejecutables
- **Entrada**: JSONs de modelo (con análisis embebido)
- **Salida**: Scripts Python independientes

#### 📊 **ReportGenerator** (Generador de Reportes)
- **Función**: Generador de reportes y visualizaciones
- **Entrada**: Resultados de análisis
- **Salida**: Reportes HTML/CSV con gráficas interactivas

## 🔄 Mejoras de la Refactorización

### Antes vs Después

| Aspecto | Código Original | Código Refactorizado |
|---------|----------------|---------------------|
| **Líneas por análisis** | ~80 líneas | ~40 líneas |
| **Métodos por clase** | 1 clase, 15+ métodos | 4 clases, 5-8 métodos c/u |
| **Condicionales if** | 20+ condicionales | 5-8 condicionales |
| **Creación de ODB** | Siempre | Solo cuando necesario |
| **ops.analyze()** | Siempre paso a paso | Optimizado por contexto |

### Arquitectura Modular Implementada

```
src/
├── analysis_engine_refactored.py      # Orquestador principal
├── utils/
│   ├── analysis_types.py              # StaticAnalysis, ModalAnalysis, DynamicAnalysis
│   └── visualization_helper.py        # VisualizationHelper (opstool)
```

#### **1. Análisis Específicos**
```python
class StaticAnalysis(BaseAnalysis):
    def run(self, viz_helper=None) -> Dict:
        # Solo lógica de análisis estático
        
class ModalAnalysis(BaseAnalysis):
    def run(self, viz_helper=None) -> Dict:
        # Solo lógica de análisis modal
        
class DynamicAnalysis(BaseAnalysis):
    def run(self, viz_helper=None) -> Dict:
        # Solo lógica de análisis dinámico
```

#### **2. Helper de Visualización**
```python
class VisualizationHelper:
    def create_odb_if_needed(self) -> bool:
        # Crea ODB SOLO cuando es necesario
        
    def generate_static_visualization(self) -> List[str]:
        # Maneja toda la lógica de visualización estática
        
    def generate_modal_visualizations(self) -> List[str]:
        # Maneja visualizaciones de formas modales
```

## 🎛️ Control Granular de Visualización

### Configuración de Visualización
```python
'visualization': {
    'enabled': False,           # Control maestro on/off
    'static_deformed': False,   # Deformada estática
    'modal_shapes': False,      # Formas modales  
    'max_modes': 6,            # Máximo número de modos a visualizar
    'deform_scale': 100,       # Factor de escala visual
    'export_format': 'html',   # Formato de exportación
    'show_nodes': True,        # Mostrar nodos
    'line_width': 2            # Grosor de líneas
}
```

### Casos de Uso Optimizados

#### **📈 Análisis Rápido (Solo Números)**
```python
# Para estudios paramétricos grandes
model = builder.create_model(1.5, 10, 4, 4,
    analysis_params={'visualization': {'enabled': False}}
)
# Resultado: Solo números, sin archivos HTML, máxima velocidad
```

#### **🏗️ Verificación Estructural**
```python
# Para verificar deformaciones
model = builder.create_model(1.5, 10, 4, 4,
    analysis_params={
        'visualization': {
            'enabled': True,
            'static_deformed': True,    # Solo deformada estática
            'modal_shapes': False
        }
    }
)
# Resultado: 1 archivo HTML con deformada estática
```

#### **🌊 Análisis Modal**
```python
# Para estudiar comportamiento dinámico
model = builder.create_model(1.5, 10, 4, 4,
    analysis_params={
        'visualization': {
            'enabled': True,
            'static_deformed': False,
            'modal_shapes': True,       # Solo formas modales
            'max_modes': 8
        }
    }
)
# Resultado: 8 archivos HTML con formas modales
```

#### **🎨 Presentación Completa**
```python
# Para reportes, presentaciones, depuración
model = builder.create_model(1.5, 10, 4, 4,
    analysis_params={
        'visualization': {
            'enabled': True,
            'static_deformed': True,
            'modal_shapes': True,
            'deform_scale': 200
        }
    }
)
# Resultado: Deformada estática + formas modales
```

## 📋 API Unificada de ModelBuilder

### Método Principal
```python
def create_model(self, L_B_ratio, B, nx, ny, 
                model_name=None, 
                enabled_analyses=None,      # Control de qué análisis ejecutar
                analysis_params=None):      # Parámetros personalizados
```

### Métodos de Conveniencia
```python
# Métodos simplificados para casos comunes
builder.create_static_only_model(...)   # Solo análisis estático
builder.create_modal_only_model(...)    # Solo análisis modal
builder.create_dynamic_model(...)       # Estático + dinámico
builder.create_complete_model(...)      # Estático + modal + dinámico
```

### Ejemplos de Uso
```python
# Configuración básica
model = builder.create_model(1.5, 10, 4, 4)

# Análisis específicos
model = builder.create_model(1.5, 10, 4, 4, enabled_analyses=['static', 'modal'])

# Configuración avanzada
model = builder.create_model(1.5, 10, 4, 4,
    enabled_analyses=['static', 'modal', 'dynamic'],
    analysis_params={
        'static': {'steps': 20, 'algorithm': 'Newton'},
        'modal': {'num_modes': 12},
        'dynamic': {'dt': 0.001, 'num_steps': 5000},
        'visualization': {
            'enabled': True,
            'static_deformed': True,
            'modal_shapes': True
        }
    }
)
```

## 🔧 Instalación y Configuración

### Dependencias
```bash
pip install -r requirements.txt
```

### Principales Librerías
- `openseespy`: Motor de análisis estructural
- `opstool`: Visualización y post-procesamiento
- `numpy`: Cálculos numéricos
- `pandas`: Manejo de datos
- `plotly`: Gráficas interactivas
- `tqdm`: Barras de progreso

### Verificación de Instalación
```python
import openseespy.opensees as ops
import opstool as opst
print("OpenSees y opstool instalados correctamente")
```

## 🚀 Guía de Uso

### 1. Análisis Individual Rápido
```python
from src.model_builder import ModelBuilder
from src.analysis_engine_refactored import AnalysisEngine

# Crear modelo sin visualización (máxima velocidad)
builder = ModelBuilder()
model_info = builder.create_model(1.5, 10, 4, 4,
    enabled_analyses=['static', 'modal'],
    analysis_params={'visualization': {'enabled': False}}
)

# Ejecutar análisis
engine = AnalysisEngine()
results = engine.analyze_model(model_info['file_path'])

# Extraer resultados principales
print(f"Desplazamiento máximo: {results['static_analysis']['max_displacement']:.6f} m")
print(f"Periodo fundamental: {results['modal_analysis']['fundamental_period']:.4f} s")
```

### 2. Estudio Paramétrico Eficiente
```python
from src.parametric_runner import ParametricRunner

# Configurar componentes
builder = ModelBuilder()
engine = AnalysisEngine()
runner = ParametricRunner(builder, engine)

# Ejecutar estudio paramétrico
results = runner.run_full_study(
    L_B_ratios=[1.5, 2.0], 
    B_values=[10.0, 12.0],
    nx_values=[3, 4], 
    ny_values=[3, 4],
    selection_method="distribution",
    analysis_distribution={"static": 0.6, "modal": 0.2, "complete": 0.2}
)
```

### 3. Análisis con Visualización Completa
```python
# Modelo con visualización detallada
model_info = builder.create_model(1.5, 10, 4, 4,
    enabled_analyses=['static', 'modal'],
    analysis_params={
        'visualization': {
            'enabled': True,
            'static_deformed': True,
            'modal_shapes': True,
            'max_modes': 6,
            'deform_scale': 150
        }
    }
)

results = engine.analyze_model(model_info['file_path'])

# Archivos generados
viz_files = results.get('visualization_files', [])
print(f"Archivos de visualización generados: {len(viz_files)}")
```

### 4. Generar Reportes
```python
from src.report_generator import ReportGenerator

# Generar reporte completo
reporter = ReportGenerator(results_dir="results", reports_dir="reports")
all_results = reporter.load_all_results()
comprehensive_report = reporter.generate_comprehensive_report(all_results)
```

## 📊 Parámetros del Modelo

### Parámetros Fijos
- **Columnas**: 40x40 cm
- **Vigas**: 25x40 cm  
- **Losa**: 10 cm de espesor
- **Altura de piso**: 3.0 m
- **Número de pisos**: 2
- **Módulo de elasticidad**: E = 15000√210 × 0.001/0.01² tonf/m²
- **Coeficiente de Poisson**: ν = 0.2
- **Densidad**: ρ = 2.4/9.81 tonf·s²/m⁴

### Parámetros Variables
- **L/B ratio**: Relación longitud/ancho (1.0, 1.5, 2.0, 2.5)
- **B**: Ancho de la estructura en metros (5.0, 10.0, 15.0, 20.0)
- **nx**: Número de ejes estructurales en dirección X (3, 4, 5, 6)
- **ny**: Número de ejes estructurales en dirección Y (2, 3, 4)

### Convención de Nombres
Los modelos se nombran siguiendo: `F01_XX_BB_YYYY`
- `F01`: Identificador del proyecto
- `XX`: Relación L/B × 10 (ej: 15 = L/B = 1.5)
- `BB`: Ancho B en metros (ej: 10 = B = 10m)
- `YYYY`: Combinación nx×100 + ny (ej: 0403 = nx=4, ny=3)

## 🔬 Tipos de Análisis

### Análisis Estático
- **Cargas**: 1 tonf/m² distribuida en el último piso
- **Método**: Análisis lineal con pasos controlados
- **Resultados**: Desplazamientos máximos, deformadas

### Análisis Modal
- **Método**: Cálculo de valores propios
- **Modos**: Configurable (6-12 modos típicamente)
- **Resultados**: Frecuencias, períodos, formas modales

### Análisis Dinámico
- **Método**: Integración directa (Newmark)
- **Configuración**: dt y num_steps personalizables
- **Resultados**: Historia de respuesta en el tiempo

## 📁 Archivos de Salida

### Modelos (`models/`)
- **Formato**: JSON
- **Contenido**: Geometría, elementos, cargas, configuración de análisis

### Resultados (`results/`)
- **Formato**: JSON
- **Contenido**: Desplazamientos, frecuencias, períodos, estados de análisis
- **Visualizaciones**: Archivos HTML interactivos (opcional)

### Reportes (`reports/`)
- **HTML**: Reportes completos interactivos
- **CSV**: Datos tabulares para análisis posterior
- **PNG**: Gráficas estáticas
- **TXT**: Resúmenes ejecutivos

### Archivos de Visualización
```
results/
├── modelo_results.json                    # Resultados numéricos
├── modelo_static_deformed.html           # Deformada estática (opcional)
├── modelo_mode_1_T0.2500s.html          # Modo 1 (opcional)
├── modelo_mode_2_T0.1800s.html          # Modo 2 (opcional)
└── modelo_mode_3_T0.1200s.html          # Modo 3 (opcional)
```

## 🛠️ Desarrollo y Extensibilidad

### Agregar Nuevo Tipo de Análisis
```python
# En utils/analysis_types.py
class PushoverAnalysis(BaseAnalysis):
    def run(self, viz_helper=None) -> Dict:
        # Implementar lógica específica de pushover
        
# En analysis_engine_refactored.py
if 'pushover' in enabled_analyses:
    pushover_analysis = PushoverAnalysis(model_data)
    results['pushover_analysis'] = pushover_analysis.run(viz_helper)
```

### Agregar Nueva Visualización
```python
# En utils/visualization_helper.py
def generate_pushover_visualization(self, model_name: str, viz_config: Dict):
    # Implementar nueva visualización sin tocar otros métodos
```

### Modificar Parámetros del Modelo
```python
# En model_builder.py - modificar fixed_params
self.fixed_params = {
    'column_size': (0.50, 0.50),  # Cambiar a 50x50 cm
    'beam_size': (0.30, 0.50),    # Cambiar a 30x50 cm
    # ... otros parámetros
}
```

## 🐛 Troubleshooting

### Problemas Comunes

1. **Error de importación de OpenSees**:
   ```bash
   pip install openseespy
   ```

2. **Error de importación de opstool**:
   ```bash
   pip install opstool
   ```

3. **Análisis falla por convergencia**:
   - Reducir el tamaño de paso en análisis estático
   - Cambiar algoritmo a 'Newton' para problemas no lineales
   - Verificar condiciones de frontera

4. **Visualización no se genera**:
   - Verificar que `visualization.enabled = True`
   - Confirmar que el análisis fue exitoso
   - Revisar permisos de escritura en directorio results

5. **Performance lenta en estudios grandes**:
   - Deshabilitar visualización: `visualization.enabled = False`
   - Usar menos modos modales
   - Considerar análisis distribuido

### Debugging
```python
# Habilitar logs detallados
import logging
logging.basicConfig(level=logging.DEBUG)

# Verificar estado de análisis
if results['static_analysis']['success']:
    print("Análisis estático exitoso")
else:
    print(f"Error: {results['static_analysis'].get('error', 'Desconocido')}")
```

## 🧪 Testing del Sistema

### Suite de Tests Organizada

El sistema incluye una suite completa de tests organizados por componente:

```
tests/
├── run_all_tests.py               # Runner principal de tests
├── test_model_builder.py          # Tests de ModelBuilder
├── test_analysis_engine.py        # Tests de AnalysisEngine refactorizado
├── test_visualization_helper.py   # Tests de VisualizationHelper
├── test_analysis_types.py         # Tests de análisis específicos
├── test_utils.py                  # Tests de helpers y utilidades
└── test_parametric_runner.py      # Tests de ParametricRunner
```

### Ejecutar Tests

**Opción 1: Runner interactivo**
```bash
python tests/run_all_tests.py
```

**Opción 2: Pytest (recomendado)**
```bash
pip install pytest
pytest tests/ -v
```

**Opción 3: Tests específicos**
```bash
# Solo ModelBuilder
python tests/run_all_tests.py 1

# Solo AnalysisEngine  
python tests/run_all_tests.py 2

# Todos los tests
python tests/run_all_tests.py all
```

### Cobertura de Tests

Los tests cubren:

- ✅ **Funcionalidad core**: Creación de modelos, análisis, visualización
- ✅ **Manejo de errores**: Archivos faltantes, fallas de convergencia 
- ✅ **Casos límite**: Modelos vacíos, parámetros inválidos
- ✅ **Integración**: Flujo completo de ModelBuilder → AnalysisEngine
- ✅ **Utilidades**: Helpers, runners paramétricos
- ✅ **Mocks**: Simulación de OpenSees y opstool para tests unitarios

### Categorías de Tests

| Categoría | Descripción | Archivos |
|-----------|-------------|-----------|
| **Unit Tests** | Tests unitarios de cada clase | `test_*.py` |
| **Integration** | Tests de integración entre componentes | Incluidos en cada test |
| **Mock Tests** | Tests con simulación de dependencias | Mayoría de tests |
| **API Tests** | Tests de la API unificada | `test_model_builder.py` |

## 📈 Beneficios de la Refactorización

1. **Código 50% más corto y legible**
2. **Eliminación del 80% de condicionales complejas**
3. **Separación clara de responsabilidades**
4. **Reutilización efectiva de componentes**
5. **Gestión inteligente de recursos (ODB solo cuando necesario)**
6. **Facilidad para agregar nuevos tipos de análisis**
7. **Performance optimizada según el caso de uso**
8. **API unificada y consistente**
9. **Control granular de visualización**
10. **Código mantenible y extensible**
11. **Suite de tests completa y organizada**
12. **Documentación consolidada y actualizada**

## 📜 Licencia

Este proyecto está bajo licencia MIT. Ver archivo LICENSE para más detalles.

## 📞 Contacto

Para preguntas, soporte o contribuciones, contactar al desarrollador principal del proyecto.

---

**Nota**: Esta documentación refleja el estado actual del sistema después de las refactorizaciones realizadas en agosto de 2025, incluyendo la separación modular de análisis, control granular de visualización, API unificada y suite de tests organizada. 