# Ejemplos de Uso del Sistema OpenSees

Esta carpeta contiene ejemplos prácticos organizados por casos de uso específicos. Cada ejemplo es un archivo Python independiente que demuestra diferentes aspectos del sistema.

## 📁 Estructura de Ejemplos

| Archivo | Caso de Uso | Descripción | Nivel |
|---------|-------------|-------------|-------|
| [**01_analisis_individual_basico.py**](01_analisis_individual_basico.py) | Análisis individual | Crear y analizar un modelo básico | Principiante |
| [**02_control_visualizacion.py**](02_control_visualizacion.py) | Visualización | Control granular de outputs | Intermedio |
| [**03_tipos_analisis.py**](03_tipos_analisis.py) | Tipos de análisis | Estático, modal, dinámico, completo | Intermedio |
| [**04_estudio_parametrico.py**](04_estudio_parametrico.py) | Estudio paramétrico | Análisis de múltiples modelos | Avanzado |
| [**05_exportacion_scripts.py**](05_exportacion_scripts.py) | Exportación | Scripts Python independientes | Intermedio |
| [**06_generacion_reportes.py**](06_generacion_reportes.py) | Reportes | Documentación automática | Avanzado |

## 🚀 Cómo Ejecutar los Ejemplos

### Requisitos Previos
```bash
# Asegúrate de tener el entorno configurado
pip install -r requirements.txt

# Verifica que estás en el directorio raíz del proyecto
cd opensees-parametric-analysis
```

### Ejecución Individual
```bash
# Ejecutar un ejemplo específico
python examples/01_analisis_individual_basico.py

# O desde la carpeta examples
cd examples
python 01_analisis_individual_basico.py
```

### Ejecución Secuencial
```bash
# Ejecutar todos los ejemplos en orden
python examples/01_analisis_individual_basico.py
python examples/02_control_visualizacion.py
python examples/03_tipos_analisis.py
python examples/04_estudio_parametrico.py
python examples/05_exportacion_scripts.py
python examples/06_generacion_reportes.py
```

## 📚 Guía de Ejemplos

### 1️⃣ Análisis Individual Básico
**Objetivo**: Introducción al sistema con un modelo simple
```python
# Crear modelo básico
builder = ModelBuilder()
model = builder.create_model(1.5, 10, 4, 4)

# Analizar
engine = AnalysisEngine()
results = engine.analyze_model(model['file_path'])
```
- ✅ Perfecto para empezar
- ⏱️ Ejecuta en < 30 segundos
- 📊 Resultados numéricos básicos

### 2️⃣ Control de Visualización
**Objetivo**: Demostrar opciones de visualización
```python
# Sin visualización (rápido)
analysis_params={'visualization': {'enabled': False}}

# Visualización completa (detallado)
analysis_params={'visualization': {
    'enabled': True,
    'static_deformed': True,
    'modal_shapes': True
}}
```
- 🎛️ 4 casos diferentes de visualización
- 📈 Comparación de tiempos de ejecución
- 🎨 Archivos HTML interactivos

### 3️⃣ Tipos de Análisis
**Objetivo**: Diferentes tipos de análisis estructural
```python
# Solo estático
enabled_analyses=['static']

# Solo modal  
enabled_analyses=['modal']

# Análisis completo
enabled_analyses=['static', modal', 'dynamic']
```
- 🔬 4 tipos de análisis diferentes
- 📊 Comparación de resultados
- ⚙️ Configuración avanzada de parámetros

### 4️⃣ Estudio Paramétrico
**Objetivo**: Análisis de múltiples modelos
```python
# Estudio completo
runner = ParametricRunner(builder, engine)
results = runner.run_full_study(
    L_B_ratios=[1.0, 1.5, 2.0],
    B_values=[10.0, 15.0],
    nx_values=[3, 4, 5]
)
```
- 📈 4 estudios paramétricos diferentes
- 🔍 Análisis de sensibilidad
- 📊 Estadísticas agregadas
- ⏱️ Puede tomar varios minutos

### 5️⃣ Exportación de Scripts
**Objetivo**: Scripts Python independientes
```python
# Exportar como script unificado
exporter = PythonExporter()
script_path = exporter.export_script(
    model, 
    separate_files=False
)
```
- 📦 Exportación unificada y modular
- 🔄 Exportación en lote
- 📋 Scripts listos para distribución

### 6️⃣ Generación de Reportes
**Objetivo**: Documentación automática
```python
# Generar reporte completo
reporter = ReportGenerator()
report = reporter.generate_comprehensive_report(
    results,
    export_formats=['html', 'pdf']
)
```
- 📄 5 tipos de reportes diferentes
- 📊 Múltiples formatos de exportación
- 📈 Gráficas y análisis automático

## ⏱️ Tiempos Estimados de Ejecución

| Ejemplo | Tiempo Estimado | Modelos Creados | Archivos Generados |
|---------|-----------------|-----------------|-------------------|
| **01 - Básico** | 30 segundos | 1 | JSON + resultados |
| **02 - Visualización** | 2-5 minutos | 4 | JSON + HTML + resultados |
| **03 - Tipos Análisis** | 3-8 minutos | 4 | JSON + resultados |
| **04 - Paramétrico** | 5-15 minutos | 15-30 | JSON + resultados + reportes |
| **05 - Exportación** | 2-4 minutos | 6 | JSON + Scripts Python |
| **06 - Reportes** | 5-10 minutos | 10-20 | JSON + HTML + PDF + Excel |

## 📁 Archivos Generados

Los ejemplos crean archivos en las siguientes carpetas:

```
opensees-parametric-analysis/
├── models/                    # Modelos JSON generados
├── results/                   # Resultados de análisis  
├── reports/                   # Reportes HTML/PDF
├── exported_scripts/          # Scripts Python exportados
└── examples/                  # Esta carpeta
```

### Limpieza de Archivos
```bash
# Limpiar todos los archivos generados
rm -rf models/* results/* reports/* exported_scripts/*

# O mantener estructura
find models results reports exported_scripts -name "*ejemplo*" -delete
```

## 🎯 Recomendaciones de Uso

### Para Usuarios Nuevos
1. **Empezar con**: `01_analisis_individual_basico.py`
2. **Continuar con**: `02_control_visualizacion.py`
3. **Explorar**: `03_tipos_analisis.py`

### Para Usuarios Intermedios
1. **Revisar**: `04_estudio_parametrico.py`
2. **Practicar**: `05_exportacion_scripts.py`
3. **Dominar**: `06_generacion_reportes.py`

### Para Desarrollo e Investigación
- **Modificar** los ejemplos según necesidades específicas
- **Combinar** técnicas de múltiples ejemplos
- **Automatizar** workflows usando estos patrones

## 🔧 Personalización

### Modificar Parámetros
Cada ejemplo tiene una sección de parámetros fácil de modificar:
```python
# === PARÁMETROS MODIFICABLES ===
L_B_ratio = 1.5    # Cambiar relación L/B
B = 10.0           # Cambiar tamaño del edificio
nx = 4             # Cambiar número de ejes X
ny = 4             # Cambiar número de ejes Y
```

### Agregar Nuevos Casos
```python
# Copiar estructura de ejemplos existentes
# Modificar parámetros y configuración
# Documentar el nuevo caso de uso
```

## 🐛 Solución de Problemas

### Errores Comunes
1. **ModuleNotFoundError**: Ejecutar desde directorio raíz
2. **Permisos de escritura**: Verificar permisos en carpetas de salida
3. **OpenSees no encontrado**: Verificar instalación con `pip install openseespy`

### Debugging
```python
# Habilitar logs detallados
import logging
logging.basicConfig(level=logging.DEBUG)

# Ejecutar ejemplo con logs
python examples/01_analisis_individual_basico.py
```

## 📞 Soporte

- **Documentación completa**: [docs/](../docs/)
- **Tests del sistema**: [tests/](../tests/)
- **Issues**: GitHub Issues
- **Troubleshooting**: [docs/troubleshooting.md](../docs/troubleshooting.md)

---

💡 **Tip**: Ejecuta los ejemplos en orden numérico para una experiencia de aprendizaje progresiva.
