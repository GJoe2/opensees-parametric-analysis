# Requisitos del Sistema y Instalación

## 🖥️ Requisitos del Sistema

### Python
- **Versión mínima**: Python 3.12+
- **Motivo**: Requerido por openseespy y opstool

### Sistemas Operativos Soportados
- ✅ **Windows 10/11** - Completamente soportado
- ✅ **Ubuntu 20.04+** - Soportado con dependencias del sistema
- ❓ **macOS** - No testeado (debería funcionar pero sin garantías)

## 📦 Instalación por Sistema Operativo

### 🚀 Instalación Automática (Recomendada)

```bash
# Descargar e ejecutar instalador automático
curl -fsSL https://raw.githubusercontent.com/GJoe2/opensees-parametric-analysis/master/scripts/install.sh | bash

# O desde código fuente
curl -fsSL https://raw.githubusercontent.com/GJoe2/opensees-parametric-analysis/master/scripts/install.sh | bash -s -- --source
```

El instalador automático:
- ✅ Detecta tu distribución Linux (Ubuntu, Debian, CentOS, Fedora)
- ✅ Detecta si es Desktop o Server (headless)
- ✅ Instala solo las dependencias necesarias
- ✅ Configura el entorno apropiado
- ✅ Verifica la instalación

### 📋 Instalación Manual

### Windows

```powershell
# Opción 1: Desde PyPI (recomendado)
pip install opensees-parametric-analysis

# Opción 2: Desde código fuente
git clone https://github.com/GJoe2/opensees-parametric-analysis.git
cd opensees-parametric-analysis
pip install -r requirements.txt
```

### Ubuntu/Debian

#### Linux Desktop (con interfaz gráfica)
```bash
# 1. Dependencias básicas (REQUERIDO)
sudo apt-get update
sudo apt-get install -y \
    libopenblas-dev \
    liblapack-dev \
    libblas-dev \
    gfortran \
    libffi-dev \
    libssl-dev

# 2. Instalar el paquete Python
# Opción 1: Desde PyPI (recomendado)
pip install opensees-parametric-analysis

# Opción 2: Desde código fuente
git clone https://github.com/GJoe2/opensees-parametric-analysis.git
cd opensees-parametric-analysis
pip install -r requirements.txt
```

#### Linux Server (sin interfaz gráfica)
```bash
# 1. Dependencias básicas + gráficas para headless (REQUERIDO)
sudo apt-get update
sudo apt-get install -y \
    libopenblas-dev \
    liblapack-dev \
    libblas-dev \
    gfortran \
    libffi-dev \
    libssl-dev \
    libglu1-mesa-dev \
    freeglut3-dev \
    mesa-common-dev \
    libgl1-mesa-dev \
    libglu1-mesa \
    xvfb

# 2. Instalar el paquete Python
pip install opensees-parametric-analysis

# 3. Para ejecutar (configurar display virtual)
export DISPLAY=:99.0
Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &
sleep 3
# Ahora puedes ejecutar tu código Python
```

### Red Hat/CentOS/Fedora

#### Desktop
```bash
# Para RHEL/CentOS:
sudo yum install -y openblas-devel lapack-devel blas-devel gcc-gfortran libffi-devel openssl-devel

# Para Fedora:
sudo dnf install -y openblas-devel lapack-devel blas-devel gcc-gfortran libffi-devel openssl-devel

pip install opensees-parametric-analysis
```

#### Server (headless)
```bash
# Para RHEL/CentOS:
sudo yum install -y openblas-devel lapack-devel blas-devel gcc-gfortran libffi-devel openssl-devel mesa-libGLU-devel freeglut-devel mesa-libGL-devel xorg-x11-server-Xvfb

# Para Fedora:
sudo dnf install -y openblas-devel lapack-devel blas-devel gcc-gfortran libffi-devel openssl-devel mesa-libGLU-devel freeglut-devel mesa-libGL-devel xorg-x11-server-Xvfb

pip install opensees-parametric-analysis
```

### macOS (No testeado)

```bash
# Instalar Homebrew si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependencias (puede funcionar)
brew install openblas lapack

# Instalar el paquete
pip install opensees-parametric-analysis
```

## ⚠️ Problemas Comunes

### Error: `libGLU.so.1: cannot open shared object file`

**Síntoma**: Error de importación de opstool en Linux
```
OSError: libGLU.so.1: cannot open shared object file: No such file or directory
```

**Causa**: Faltan bibliotecas gráficas OpenGL/GLU necesarias para opstool

**Solución**: Instalar dependencias gráficas del sistema
```bash
sudo apt-get install -y libglu1-mesa-dev freeglut3-dev mesa-common-dev libgl1-mesa-dev libglu1-mesa
```

### Error: `libblas.so.3: cannot open shared object file`

**Síntoma**: Error de importación de openseespy en Linux
```
ImportError: libblas.so.3: cannot open shared object file: No such file or directory
RuntimeError: Failed to import openseespy on Linux.
```

**Solución**: Instalar dependencias del sistema (ver sección Ubuntu arriba)

### Error: `Failed to import openseespy`

**Causas posibles**:
1. **Linux**: Faltan bibliotecas del sistema → Instalar dependencias
2. **Todas las plataformas**: Python < 3.12 → Actualizar Python
3. **Todas las plataformas**: Instalación corrupta → Reinstalar openseespy

**Soluciones**:
```bash
# Verificar versión de Python
python --version  # Debe ser >= 3.12

# Reinstalar openseespy
pip uninstall openseespy
pip install openseespy>=3.4.0

# En Linux, asegurar dependencias del sistema (álgebra lineal)
sudo apt-get install -y libopenblas-dev liblapack-dev libblas-dev

# En Linux, asegurar dependencias gráficas (para opstool)
sudo apt-get install -y libglu1-mesa-dev freeglut3-dev mesa-common-dev
```

### Error: Display/Graphics en servidores sin GUI

**Síntoma**: Errores relacionados con display o gráficos en servidores Linux
```
Cannot connect to X server
No display available
```

**Causa**: opstool requiere capacidades gráficas que no están disponibles en servidores headless

**Solución**: Usar display virtual (Xvfb)
```bash
# Instalar Xvfb
sudo apt-get install -y xvfb

# Ejecutar con display virtual
export DISPLAY=:99.0
Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &
python tu_script.py
```

## 🧪 Testing en Diferentes Entornos

### Entorno Local (con GUI)
```bash
python verify_installation.py
pytest tests/ -v
```

### Servidor/CI (headless)
```bash
# Setup display virtual
export DISPLAY=:99.0
Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &
sleep 3

# Ejecutar tests
python verify_installation.py
pytest tests/ -v
```

## 🧪 Verificar Instalación

### Script de Verificación

```python
#!/usr/bin/env python3
"""
Script para verificar que opensees-parametric-analysis esté correctamente instalado
"""

def test_imports():
    """Verificar que todas las importaciones funcionen"""
    try:
        print("🔍 Verificando importaciones...")
        
        # Test Python version
        import sys
        version = sys.version_info
        if version < (3, 12):
            print(f"❌ Python {version.major}.{version.minor} es muy antiguo. Se requiere 3.12+")
            return False
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        
        # Test openseespy
        import openseespy.opensees as ops
        print("✅ openseespy importado correctamente")
        
        # Test opstool  
        import opstool
        print("✅ opstool importado correctamente")
        
        # Test package components
        try:
            from opensees_parametric_analysis import ModelBuilder, AnalysisEngine
            print("✅ Paquete instalado desde PyPI")
        except ImportError:
            from src.model_builder import ModelBuilder
            from src.analysis_engine import AnalysisEngine
            print("✅ Usando código fuente")
        
        print("\n🎉 ¡Instalación exitosa! Todos los componentes funcionan correctamente.")
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("\n💡 Posibles soluciones:")
        print("   1. Verificar que Python >= 3.12")
        print("   2. En Linux: instalar dependencias del sistema")
        print("   3. Reinstalar: pip install --force-reinstall opensees-parametric-analysis")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_basic_functionality():
    """Test básico de funcionalidad"""
    try:
        print("\n🔧 Probando funcionalidad básica...")
        
        # Import based on installation method
        try:
            from opensees_parametric_analysis import ModelBuilder
        except ImportError:
            from src.model_builder import ModelBuilder
        
        # Create a simple model
        builder = ModelBuilder()
        print("✅ ModelBuilder creado")
        
        # This would normally create a model, but we'll just verify the builder works
        print("✅ Funcionalidad básica verificada")
        return True
        
    except Exception as e:
        print(f"❌ Error en test de funcionalidad: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Verificando instalación de opensees-parametric-analysis\n")
    
    imports_ok = test_imports()
    if imports_ok:
        functionality_ok = test_basic_functionality()
        if functionality_ok:
            print("\n✨ Todo perfecto! El sistema está listo para usar.")
        else:
            print("\n⚠️  Importaciones OK pero hay problemas de funcionalidad.")
    else:
        print("\n🔧 Por favor corrige los problemas de importación primero.")
```

Guardar como `verify_installation.py` y ejecutar:

```bash
python verify_installation.py
```

## 📋 Dependencias Detalladas

### Dependencias Python (automáticas)
- openseespy >= 3.4.0
- opstool >= 0.0.1  
- numpy >= 1.21.0
- pandas >= 1.3.0
- matplotlib >= 3.5.0
- plotly >= 5.0.0
- seaborn >= 0.11.0
- jupyter >= 1.0.0
- ipywidgets >= 7.6.0
- tqdm >= 4.62.0

### Dependencias del Sistema (Linux)
- **Álgebra lineal** (siempre requeridas):
  - libopenblas-dev - Álgebra lineal optimizada
  - liblapack-dev - Rutinas de álgebra lineal
  - libblas-dev - Operaciones básicas de álgebra lineal
- **Compilación** (siempre requeridas):
  - gfortran - Compilador Fortran (para extensiones)
  - libffi-dev - Interface de funciones foráneas
  - libssl-dev - Biblioteca SSL/TLS
- **Gráficos/OpenGL** (solo para servidores headless):
  - libglu1-mesa-dev - OpenGL Utility Library
  - freeglut3-dev - GLUT (OpenGL Utility Toolkit)
  - mesa-common-dev - Mesa 3D graphics library
  - libgl1-mesa-dev - Mesa OpenGL development
  - libglu1-mesa - GLU runtime library
  - xvfb - Virtual framebuffer X server

## 🆘 Obtener Ayuda

Si los problemas persisten:

1. **Crear issue**: [GitHub Issues](https://github.com/GJoe2/opensees-parametric-analysis/issues)
2. **Incluir**:
   - Salida del script de verificación
   - Sistema operativo y versión
   - Versión de Python
   - Log completo del error

3. **Información útil**:
   ```bash
   python --version
   pip list | grep -E "(opensees|opstool)"
   cat /etc/os-release  # Linux
   ```
