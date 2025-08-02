# 🏗️ Arquitectura del Sistema

## Estructura de Archivos
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

## Separación de Responsabilidades

### 🏗️ **ModelBuilder** (Constructor de Modelos)
- **Función**: Generador de modelos con API unificada
- **Entrada**: Parámetros geométricos (L_B_ratio, B, nx, ny)
- **Salida**: Archivos JSON con modelo + configuración de análisis embebida
- **Característica**: Control granular de análisis y visualización

### ⚙️ **AnalysisEngine** (Motor de Análisis Refactorizado)
- **Función**: Ejecutor puro de análisis con arquitectura modular
- **Entrada**: Archivos JSON de modelo
- **Salida**: Resultados de análisis
- **Mejoras**: Código 50% más corto, eliminación de condicionales complejas, gestión inteligente de recursos

### 🎯 **ParametricRunner** (Orquestador)
- **Función**: Orquestador de estudios paramétricos
- **Entrada**: Rangos de parámetros + estrategia de distribución
- **Salida**: Estudios completos con reportes
- **Configuración**: Define estrategias de asignación de análisis

### 📝 **PythonExporter** (Exportador)
- **Función**: Exportador de scripts Python ejecutables
- **Entrada**: JSONs de modelo (con análisis embebido)
- **Salida**: Scripts Python independientes

### 📊 **ReportGenerator** (Generador de Reportes)
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
