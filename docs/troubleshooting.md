# 🐛 Troubleshooting

## Problemas Comunes y Soluciones

### 1. Problemas de Instalación

#### Error de importación de OpenSees
```bash
ImportError: No module named 'openseespy'
```

**Solución:**
```bash
pip uninstall openseespy
pip install openseespy
```

**Si persiste el problema:**
```bash
# En Windows
pip install openseespy --user

# En Linux/Mac con problemas de permisos
sudo pip install openseespy

# Con conda
conda install -c conda-forge openseespy
```

#### Error de importación de opstool
```bash
ImportError: No module named 'opstool'
```

**Solución:**
```bash
pip install --upgrade opstool

# Si hay conflictos de dependencias
pip install opstool --force-reinstall
```

#### Problemas con dependencias de visualización
```bash
# Error con plotly o matplotlib
pip install plotly matplotlib kaleido

# Error con pandas o numpy
pip install pandas numpy --upgrade
```

### 2. Problemas de Análisis

#### Análisis falla por convergencia
```
AnalysisError: Static analysis failed to converge
```

**Diagnóstico:**
```python
# Verificar parámetros del modelo
print(f"L/B ratio: {L_B_ratio}, B: {B}, nx: {nx}, ny: {ny}")

# Calcular separaciones
L = L_B_ratio * B
sx = L / (nx - 1)
sy = B / (ny - 1)
print(f"Separaciones - X: {sx:.2f}m, Y: {sy:.2f}m")
```

**Soluciones:**
```python
# 1. Reducir el tamaño de paso en análisis estático
analysis_params = {
    'static': {
        'steps': 20,  # Aumentar de 10 a 20
        'tolerance': 1e-8  # Hacer más estricta la tolerancia
    }
}

# 2. Cambiar algoritmo para problemas no lineales
analysis_params = {
    'static': {
        'algorithm': 'Newton',  # En lugar de 'Linear'
        'max_iterations': 50
    }
}

# 3. Verificar condiciones de frontera
# Revisar que el modelo tenga restricciones adecuadas
```

#### Análisis modal falla
```
ModalError: Failed to compute eigenvalues
```

**Soluciones:**
```python
# 1. Reducir número de modos
analysis_params = {
    'modal': {
        'num_modes': 3  # En lugar de 6 o más
    }
}

# 2. Cambiar solver de eigenvalores
analysis_params = {
    'modal': {
        'eigen_solver': 'genBandArpack'  # En lugar de 'fullGenLapack'
    }
}
```

### 3. Problemas de Visualización

#### Visualización no se genera
```
Warning: No visualization files were created
```

**Verificaciones:**
```python
# 1. Confirmar que está habilitada
viz_config = {
    'enabled': True,  # Debe ser True
    'static_deformed': True
}

# 2. Verificar que el análisis fue exitoso
if results['static_analysis']['success']:
    print("Análisis OK, problema en visualización")
else:
    print("Análisis falló, no se puede visualizar")

# 3. Revisar permisos de escritura
import os
results_dir = "results"
if os.access(results_dir, os.W_OK):
    print("Permisos de escritura OK")
else:
    print("Sin permisos de escritura en results/")
```

**Soluciones:**
```bash
# 1. Crear directorio de resultados
mkdir results

# 2. Cambiar permisos (Linux/Mac)
chmod 755 results/

# 3. Ejecutar como administrador (Windows)
# Ejecutar terminal como administrador
```

#### Archivos HTML vacíos o corruptos
```
Warning: Generated HTML files are empty or corrupted
```

**Soluciones:**
```bash
# 1. Actualizar opstool
pip install --upgrade opstool

# 2. Verificar versión compatible
pip install opstool==0.6.0  # Usar versión específica estable

# 3. Reinstalar con dependencias
pip uninstall opstool
pip install opstool --no-cache-dir
```

### 4. Problemas de Performance

#### Sistema muy lento en estudios grandes
```
Warning: Parametric study is taking too long
```

**Optimizaciones:**
```python
# 1. Deshabilitar visualización
analysis_params = {
    'visualization': {'enabled': False}
}

# 2. Usar solo análisis necesarios
enabled_analyses = ['static']  # Solo estático, sin modal

# 3. Reducir número de modos modales
analysis_params = {
    'modal': {'num_modes': 3}  # En lugar de 6-12
}

# 4. Usar procesamiento en paralelo
runner = ParametricRunner(
    max_workers=4,  # Ajustar según CPU
    chunk_size=5
)
```

#### Uso excesivo de memoria
```
MemoryError: Unable to allocate memory
```

**Soluciones:**
```python
# 1. Procesar en lotes más pequeños
runner.run_full_study(
    ...,
    chunk_size=3  # Reducir de 10 a 3
)

# 2. Limpiar memoria entre análisis
import gc
gc.collect()  # Forzar limpieza de memoria

# 3. Usar menos workers paralelos
max_workers = 2  # En lugar de 4 o más
```

### 5. Problemas de Archivos

#### Error al leer archivos JSON
```
JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Verificación y solución:**
```python
import json
import os

def verify_json_file(file_path):
    """Verificar integridad de archivo JSON"""
    if not os.path.exists(file_path):
        print(f"Archivo no existe: {file_path}")
        return False
    
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        print(f"JSON válido: {file_path}")
        return True
    except json.JSONDecodeError as e:
        print(f"JSON inválido: {file_path}, Error: {e}")
        return False

# Usar para verificar archivos
verify_json_file("models/mi_modelo.json")
```

#### Archivos no se encuentran
```
FileNotFoundError: [Errno 2] No such file or directory: 'models/F01_15_10_0404.json'
```

**Soluciones:**
```python
# 1. Verificar rutas relativas vs absolutas
import os
current_dir = os.getcwd()
print(f"Directorio actual: {current_dir}")

# 2. Usar rutas absolutas
models_dir = os.path.abspath("models")
model_path = os.path.join(models_dir, "F01_15_10_0404.json")

# 3. Crear directorios faltantes
os.makedirs("models", exist_ok=True)
os.makedirs("results", exist_ok=True)
```

### 6. Problemas Específicos por Plataforma

#### Windows: Problemas con paths largos
```
OSError: [Errno 36] File name too long
```

**Soluciones:**
```python
# 1. Usar nombres más cortos
model_name = "F01_15_10_04"  # En lugar de nombres muy largos

# 2. Cambiar directorio de trabajo
os.chdir("C:/")  # Usar ruta más corta

# 3. Habilitar paths largos en Windows 10+
# Ejecutar como administrador:
# New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

#### Linux/Mac: Problemas de permisos
```bash
PermissionError: [Errno 13] Permission denied
```

**Soluciones:**
```bash
# 1. Cambiar permisos
chmod 755 models/ results/ reports/

# 2. Cambiar propietario
sudo chown -R $USER:$USER models/ results/ reports/

# 3. Ejecutar con permisos adecuados
sudo python run_parametric_study.py
```

### 7. Debugging Avanzado

#### Habilitar logging detallado
```python
import logging

# Configurar logging detallado
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('opensees_debug.log'),
        logging.StreamHandler()
    ]
)

# En el código
logger = logging.getLogger(__name__)
logger.debug("Iniciando análisis de modelo")
logger.info(f"Parámetros: L/B={L_B_ratio}, B={B}")
```

#### Verificar estado del sistema
```python
def system_diagnostics():
    """Diagnóstico completo del sistema"""
    import sys
    import psutil
    import openseespy
    import opstool
    
    print("=== Diagnóstico del Sistema ===")
    print(f"Python: {sys.version}")
    print(f"OpenSees: {openseespy.__version__}")
    print(f"opstool: {opstool.__version__}")
    print(f"RAM disponible: {psutil.virtual_memory().available / 1024**3:.1f} GB")
    print(f"Espacio en disco: {psutil.disk_usage('.').free / 1024**3:.1f} GB")
    
    # Verificar directorios
    dirs = ['models', 'results', 'reports']
    for dir_name in dirs:
        exists = os.path.exists(dir_name)
        writable = os.access(dir_name, os.W_OK) if exists else False
        print(f"Directorio {dir_name}: {'Existe' if exists else 'No existe'}, {'Escribible' if writable else 'No escribible'}")

# Ejecutar diagnóstico
system_diagnostics()
```

### 8. Recursos de Ayuda

#### Documentación Oficial
- **OpenSees**: https://opensees.berkeley.edu/
- **opstool**: https://opstool.readthedocs.io/
- **Python**: https://docs.python.org/

#### Foros y Comunidad
- **OpenSees Community**: https://opensees.berkeley.edu/community/
- **Stack Overflow**: Buscar "opensees python"
- **GitHub Issues**: Reportar bugs específicos del proyecto

#### Contacto de Soporte
Para problemas específicos del proyecto:
1. Revisar esta documentación de troubleshooting
2. Ejecutar diagnósticos del sistema
3. Revisar logs de error detallados
4. Contactar al desarrollador con información específica del error
