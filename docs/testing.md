# 🧪 Testing del Sistema

## Suite de Tests Organizada

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

## Ejecutar Tests

### Opción 1: Runner Interactivo
```bash
python tests/run_all_tests.py
```

**Menú interactivo:**
```
=== Test Runner del Sistema OpenSees ===
1. Test ModelBuilder
2. Test AnalysisEngine  
3. Test VisualizationHelper
4. Test AnalysisTypes
5. Test Utils
6. Test ParametricRunner
7. Ejecutar TODOS los tests
0. Salir

Seleccione una opción:
```

### Opción 2: Pytest (Recomendado)
```bash
# Instalar pytest si no está instalado
pip install pytest

# Ejecutar todos los tests con información detallada
pytest tests/ -v

# Ejecutar tests específicos
pytest tests/test_model_builder.py -v

# Ejecutar con cobertura
pip install pytest-cov
pytest tests/ --cov=src --cov-report=html
```

### Opción 3: Tests Específicos con Runner
```bash
# Solo ModelBuilder
python tests/run_all_tests.py 1

# Solo AnalysisEngine  
python tests/run_all_tests.py 2

# Todos los tests
python tests/run_all_tests.py all
```

## Cobertura de Tests

### Funcionalidad Core ✅
- **Creación de modelos**: Parámetros válidos e inválidos
- **Ejecución de análisis**: Estático, modal y dinámico
- **Generación de visualizaciones**: Con y sin opstool
- **Manejo de archivos**: JSON de entrada y salida

### Manejo de Errores ✅
- **Archivos faltantes**: Modelos JSON no existentes
- **Parámetros inválidos**: Rangos fuera de límites
- **Fallas de convergencia**: Análisis que no convergen
- **Problemas de escritura**: Permisos de archivos

### Casos Límite ✅
- **Modelos vacíos**: JSON sin datos válidos
- **Parámetros extremos**: Valores en los límites
- **Análisis parciales**: Solo algunos tipos de análisis
- **Visualización deshabilitada**: Sin generación de archivos HTML

### Integración ✅
- **Flujo completo**: ModelBuilder → AnalysisEngine → Resultados
- **Estudios paramétricos**: Múltiples modelos en secuencia
- **Exportación**: Scripts Python independientes
- **Reportes**: Generación de documentos finales

## Categorías de Tests

| Categoría | Descripción | Archivos | Propósito |
|-----------|-------------|-----------|-----------|
| **Unit Tests** | Tests unitarios de cada clase | `test_*.py` | Validar funciones individuales |
| **Integration** | Tests de integración entre componentes | Incluidos en cada test | Validar flujos completos |
| **Mock Tests** | Tests con simulación de dependencias | Mayoría de tests | Aislar componentes |
| **API Tests** | Tests de la API unificada | `test_model_builder.py` | Validar interfaces públicas |

## Estructura de Tests

### Test ModelBuilder
```python
class TestModelBuilder:
    def test_create_basic_model(self):
        """Test creación de modelo básico"""
        
    def test_model_with_custom_params(self):
        """Test modelo con parámetros personalizados"""
        
    def test_invalid_parameters(self):
        """Test manejo de parámetros inválidos"""
        
    def test_convenience_methods(self):
        """Test métodos de conveniencia"""
```

### Test AnalysisEngine
```python
class TestAnalysisEngine:
    def test_static_analysis(self):
        """Test análisis estático"""
        
    def test_modal_analysis(self):
        """Test análisis modal"""
        
    def test_dynamic_analysis(self):
        """Test análisis dinámico"""
        
    def test_missing_model_file(self):
        """Test manejo de archivos faltantes"""
```

### Test VisualizationHelper
```python
class TestVisualizationHelper:
    def test_visualization_enabled(self):
        """Test visualización habilitada"""
        
    def test_visualization_disabled(self):
        """Test visualización deshabilitada"""
        
    def test_custom_viz_config(self):
        """Test configuración personalizada"""
```

## Mocks y Simulaciones

### Mock de OpenSees
```python
# Los tests no requieren OpenSees real instalado
@patch('openseespy.opensees')
def test_analysis_without_opensees(mock_ops):
    """Test que simula OpenSees para desarrollo sin instalación"""
    mock_ops.analyze.return_value = 0  # Simular análisis exitoso
    # ... resto del test
```

### Mock de opstool
```python
# Tests de visualización sin crear archivos reales
@patch('opstool.vis')
def test_visualization_without_files(mock_vis):
    """Test visualización sin crear archivos HTML"""
    mock_vis.plot_model.return_value = "mocked_html"
    # ... resto del test
```

## Configuración de Tests

### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
markers =
    slow: marca tests lentos
    integration: marca tests de integración
    unit: marca tests unitarios
```

### Configuración de Coverage
```bash
# Generar reporte de cobertura
pytest tests/ --cov=src --cov-report=html --cov-report=term

# Ver reporte en navegador
# El archivo htmlcov/index.html contiene el reporte detallado
```

## Tests de Performance

### Benchmark de Velocidad
```python
def test_model_creation_speed(self):
    """Test velocidad de creación de modelos"""
    import time
    
    start_time = time.time()
    for i in range(10):
        builder.create_model(1.5, 10, 4, 4)
    elapsed = time.time() - start_time
    
    assert elapsed < 5.0, f"Creación de 10 modelos tomó {elapsed:.2f}s (límite: 5s)"
```

### Tests de Memoria
```python
def test_memory_usage(self):
    """Test uso de memoria en estudios grandes"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Crear múltiples modelos
    for i in range(50):
        builder.create_model(1.5, 10, 4, 4)
    
    final_memory = process.memory_info().rss
    memory_increase = (final_memory - initial_memory) / 1024 / 1024  # MB
    
    assert memory_increase < 100, f"Aumento de memoria: {memory_increase:.1f}MB (límite: 100MB)"
```

## Ejecutar Tests en CI/CD

### GitHub Actions
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11"]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
```

## Debugging de Tests

### Ejecutar Test Individual con Debug
```bash
# Ejecutar un test específico con output detallado
pytest tests/test_model_builder.py::TestModelBuilder::test_create_basic_model -v -s

# Ejecutar con debugger (pdb)
pytest tests/test_model_builder.py::TestModelBuilder::test_create_basic_model --pdb
```

### Logs de Debug en Tests
```python
import logging
logging.basicConfig(level=logging.DEBUG)

def test_with_detailed_logs(self):
    """Test con logs detallados para debugging"""
    logger = logging.getLogger(__name__)
    logger.debug("Iniciando test de creación de modelo")
    
    # ... código del test con logs
```

## Mejores Prácticas

### 1. Tests Independientes
```python
def setUp(self):
    """Cada test debe ser independiente"""
    self.builder = ModelBuilder()
    self.temp_dir = tempfile.mkdtemp()

def tearDown(self):
    """Limpiar después de cada test"""
    shutil.rmtree(self.temp_dir, ignore_errors=True)
```

### 2. Assertions Descriptivas
```python
# Malo
assert result > 0

# Bueno
assert result > 0, f"El resultado debe ser positivo, obtuvo: {result}"
```

### 3. Tests Parametrizados
```python
@pytest.mark.parametrize("L_B_ratio,B,nx,ny", [
    (1.5, 10, 4, 4),
    (2.0, 15, 5, 3),
    (1.0, 20, 6, 4)
])
def test_model_creation_variants(self, L_B_ratio, B, nx, ny):
    """Test múltiples combinaciones de parámetros"""
    model = self.builder.create_model(L_B_ratio, B, nx, ny)
    assert model is not None
```

## Resolución de Problemas

### Tests Fallan por Dependencias
```bash
# Instalar dependencias de testing
pip install pytest pytest-mock pytest-cov

# Verificar que el entorno está correctamente configurado
python -c "import src.model_builder; print('OK')"
```

### Tests Lentos
```bash
# Ejecutar solo tests rápidos
pytest tests/ -m "not slow"

# Ejecutar tests en paralelo
pip install pytest-xdist
pytest tests/ -n auto
```

### Problemas de Paths
```python
# En conftest.py o al inicio de tests
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
```
