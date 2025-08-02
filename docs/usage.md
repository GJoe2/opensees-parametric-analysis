# 🚀 Guía de Uso

## Análisis Individual Rápido

### Análisis Básico sin Visualización
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

### Análisis con Visualización Completa
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

## Estudios Paramétricos

### Estudio Paramétrico Básico
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

### Estudio Paramétrico Avanzado
```python
# Configuración avanzada con control de performance
results = runner.run_full_study(
    L_B_ratios=[1.0, 1.5, 2.0, 2.5], 
    B_values=[5.0, 10.0, 15.0, 20.0],
    nx_values=[3, 4, 5, 6], 
    ny_values=[2, 3, 4],
    selection_method="all",  # Todas las combinaciones
    analysis_distribution={"static": 1.0},  # Solo análisis estático
    parallel_workers=4,
    chunk_size=10
)
```

## API Unificada de ModelBuilder

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
model = builder.create_static_only_model(1.5, 10, 4, 4)     # Solo análisis estático
model = builder.create_modal_only_model(1.5, 10, 4, 4)      # Solo análisis modal  
model = builder.create_dynamic_model(1.5, 10, 4, 4)         # Estático + dinámico
model = builder.create_complete_model(1.5, 10, 4, 4)        # Estático + modal + dinámico
```

### Configuración Avanzada
```python
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

## Control Granular de Visualización

### Casos de Uso Optimizados

#### 📈 Análisis Rápido (Solo Números)
```python
# Para estudios paramétricos grandes
model = builder.create_model(1.5, 10, 4, 4,
    analysis_params={'visualization': {'enabled': False}}
)
# Resultado: Solo números, sin archivos HTML, máxima velocidad
```

#### 🏗️ Verificación Estructural
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

#### 🌊 Análisis Modal
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

#### 🎨 Presentación Completa
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

## Generación de Reportes

### Reporte Básico
```python
from src.report_generator import ReportGenerator

# Generar reporte completo
reporter = ReportGenerator(results_dir="results", reports_dir="reports")
all_results = reporter.load_all_results()
comprehensive_report = reporter.generate_comprehensive_report(all_results)
```

### Reporte Personalizado
```python
# Reporte específico para un conjunto de resultados
filtered_results = reporter.filter_results(
    all_results, 
    L_B_ratio_range=(1.5, 2.0),
    B_range=(10.0, 15.0)
)

custom_report = reporter.generate_custom_report(
    filtered_results,
    include_plots=['displacement_vs_LB', 'period_vs_B'],
    export_formats=['html', 'pdf']
)
```

## Exportación de Scripts Python

### Exportar Modelo Individual
```python
from src.python_exporter import PythonExporter

exporter = PythonExporter()

# Exportar un modelo específico
model_path = "models/F01_15_10_0404.json"
script_path = exporter.export_model(model_path, output_dir="scripts")

# El script generado es independiente y ejecutable
print(f"Script generado: {script_path}")
```

### Exportar Múltiples Modelos
```python
# Exportar todos los modelos de un directorio
batch_scripts = exporter.batch_export(
    models_dir="models",
    output_dir="scripts",
    include_visualization=True
)

print(f"Scripts generados: {len(batch_scripts)}")
```
