# 🔧 Instalación y Configuración

## Dependencias
```bash
pip install -r requirements.txt
```

## Principales Librerías
- `openseespy`: Motor de análisis estructural
- `opstool`: Visualización y post-procesamiento
- `numpy`: Cálculos numéricos
- `pandas`: Manejo de datos
- `plotly`: Gráficas interactivas
- `tqdm`: Barras de progreso

## Verificación de Instalación
```python
import openseespy.opensees as ops
import opstool as opst
print("OpenSees y opstool instalados correctamente")
```

## Configuración del Entorno

### Opción 1: Entorno Virtual (Recomendado)
```bash
# Crear entorno virtual
python -m venv opensees_env

# Activar entorno (Windows)
opensees_env\Scripts\activate

# Activar entorno (Linux/Mac)
source opensees_env/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Opción 2: Conda
```bash
# Crear entorno conda
conda create -n opensees python=3.9

# Activar entorno
conda activate opensees

# Instalar dependencias
pip install -r requirements.txt
```

## Requisitos del Sistema

### Mínimos
- Python 3.8+
- 4 GB RAM
- 1 GB espacio libre

### Recomendados
- Python 3.9+
- 8+ GB RAM
- 5 GB espacio libre
- SSD para mejor rendimiento

## Configuración Avanzada

### Variables de Entorno Opcionales
```bash
# Configurar directorio de resultados personalizado
export OPENSEES_RESULTS_DIR="/path/to/custom/results"

# Configurar nivel de logging
export OPENSEES_LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR
```

### Configuración de Jupyter (Para Notebooks)
```bash
# Instalar kernel del entorno
python -m ipykernel install --user --name opensees --display-name "OpenSees Analysis"

# Instalar extensiones útiles
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
```

## Resolución de Problemas Comunes

### Error de importación de OpenSees
```bash
# Reinstalar openseespy
pip uninstall openseespy
pip install openseespy
```

### Error de importación de opstool
```bash
# Actualizar opstool
pip install --upgrade opstool
```

### Problemas de visualización
```bash
# Instalar dependencias adicionales para visualización
pip install plotly kaleido
```

### Problemas de memoria en estudios grandes
```python
# En parametric_runner.py, ajustar configuración
runner = ParametricRunner(
    max_workers=2,  # Reducir workers paralelos
    chunk_size=5    # Procesar en lotes más pequeños
)
```
