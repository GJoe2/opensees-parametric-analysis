#!/bin/bash
"""
Script de instalación automática para opensees-parametric-analysis
Detecta el tipo de entorno Linux y instala las dependencias apropiadas
"""

set -e  # Exit on any error

echo "🚀 Instalador automático de opensees-parametric-analysis"
echo "=================================================="

# Detectar distribución Linux
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    echo "❌ No se pudo detectar la distribución Linux"
    exit 1
fi

echo "📋 Sistema detectado: $OS $VER"

# Detectar tipo de entorno (Desktop vs Server)
detect_environment() {
    if [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ]; then
        echo "🖥️  Entorno: Linux Desktop (con GUI)"
        return 0  # Desktop
    elif systemctl is-active --quiet graphical.target 2>/dev/null; then
        echo "🖥️  Entorno: Linux Desktop (con GUI disponible)"
        return 0  # Desktop
    elif [ "$XDG_SESSION_TYPE" = "x11" ] || [ "$XDG_SESSION_TYPE" = "wayland" ]; then
        echo "🖥️  Entorno: Linux Desktop (con GUI)"
        return 0  # Desktop
    else
        echo "🖧  Entorno: Linux Server (headless)"
        return 1  # Server
    fi
}

# Función para instalar en Ubuntu/Debian
install_ubuntu_debian() {
    local is_desktop=$1
    
    echo "📦 Actualizando repositorios..."
    sudo apt-get update
    
    echo "📦 Instalando dependencias básicas..."
    sudo apt-get install -y \
        libopenblas-dev \
        liblapack-dev \
        libblas-dev \
        gfortran \
        libffi-dev \
        libssl-dev \
        python3-pip
    
    if [ $is_desktop -eq 1 ]; then
        echo "📦 Instalando dependencias para servidor headless..."
        sudo apt-get install -y \
            libglu1-mesa-dev \
            freeglut3-dev \
            mesa-common-dev \
            libgl1-mesa-dev \
            libglu1-mesa \
            xvfb
    fi
}

# Función para instalar en Red Hat/CentOS/Fedora
install_redhat_fedora() {
    local is_desktop=$1
    
    if command -v dnf &> /dev/null; then
        PKG_MANAGER="dnf"
    elif command -v yum &> /dev/null; then
        PKG_MANAGER="yum"
    else
        echo "❌ No se encontró gestor de paquetes (dnf/yum)"
        exit 1
    fi
    
    echo "📦 Instalando dependencias básicas..."
    sudo $PKG_MANAGER install -y \
        openblas-devel \
        lapack-devel \
        blas-devel \
        gcc-gfortran \
        libffi-devel \
        openssl-devel \
        python3-pip
    
    if [ $is_desktop -eq 1 ]; then
        echo "📦 Instalando dependencias para servidor headless..."
        sudo $PKG_MANAGER install -y \
            mesa-libGLU-devel \
            freeglut-devel \
            mesa-libGL-devel \
            xorg-x11-server-Xvfb
    fi
}

# Detectar entorno
if detect_environment; then
    IS_DESKTOP=0  # Desktop
else
    IS_DESKTOP=1  # Server
fi

# Instalar según distribución
case "$OS" in
    "Ubuntu"|"Debian"*)
        install_ubuntu_debian $IS_DESKTOP
        ;;
    "CentOS"*|"Red Hat"*|"Rocky"*|"AlmaLinux"*)
        install_redhat_fedora $IS_DESKTOP
        ;;
    "Fedora"*)
        install_redhat_fedora $IS_DESKTOP
        ;;
    *)
        echo "⚠️  Distribución no soportada oficialmente: $OS"
        echo "   Intentando instalación para Ubuntu/Debian..."
        install_ubuntu_debian $IS_DESKTOP
        ;;
esac

echo ""
echo "🐍 Instalando opensees-parametric-analysis..."

# Verificar Python 3.12+
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
required_version="3.12"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "⚠️  Advertencia: Python $python_version detectado, se requiere 3.12+"
    echo "   El paquete podría no funcionar correctamente"
fi

# Instalar el paquete Python
if [ "$1" = "--dev" ] || [ "$1" = "--source" ]; then
    echo "📥 Instalando desde código fuente..."
    if [ ! -d "opensees-parametric-analysis" ]; then
        git clone https://github.com/GJoe2/opensees-parametric-analysis.git
    fi
    cd opensees-parametric-analysis
    pip3 install -r requirements.txt
    echo "✅ Instalación desde código fuente completada"
else
    echo "📥 Instalando desde PyPI..."
    pip3 install opensees-parametric-analysis
    echo "✅ Instalación desde PyPI completada"
fi

echo ""
echo "🧪 Verificando instalación..."

# Crear script de verificación temporal
cat > /tmp/verify_install.py << 'EOF'
import sys
try:
    # Test basic imports
    import openseespy.opensees as ops
    import opstool
    print("✅ Dependencias básicas OK")
    
    # Test package
    try:
        from opensees_parametric_analysis import ModelBuilder
        print("✅ Paquete PyPI OK")
    except ImportError:
        from src.model_builder import ModelBuilder
        print("✅ Código fuente OK")
    
    print("🎉 ¡Instalación exitosa!")
    sys.exit(0)
    
except ImportError as e:
    print(f"❌ Error: {e}")
    print("💡 Revisar logs de instalación arriba")
    sys.exit(1)
EOF

# Ejecutar verificación
if [ $IS_DESKTOP -eq 1 ]; then
    # Servidor: configurar display virtual
    echo "🔧 Configurando display virtual para servidor..."
    export DISPLAY=:99.0
    Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &
    XVFB_PID=$!
    sleep 3
    
    python3 /tmp/verify_install.py
    
    # Limpiar
    kill $XVFB_PID 2>/dev/null || true
else
    # Desktop: ejecución normal
    python3 /tmp/verify_install.py
fi

# Limpiar
rm -f /tmp/verify_install.py

echo ""
echo "🎯 Instalación completada!"
echo ""
if [ $IS_DESKTOP -eq 1 ]; then
    echo "📝 Para ejecutar en servidor headless:"
    echo "   export DISPLAY=:99.0"
    echo "   Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &"
    echo "   python3 tu_script.py"
    echo ""
fi
echo "📚 Documentación: https://github.com/GJoe2/opensees-parametric-analysis/tree/master/docs"
echo "🎯 Ejemplos: https://github.com/GJoe2/opensees-parametric-analysis/tree/master/examples"
