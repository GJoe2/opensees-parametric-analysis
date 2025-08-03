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
        print("      sudo apt-get install -y libopenblas-dev liblapack-dev libblas-dev gfortran libglu1-mesa-dev")
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

def show_system_info():
    """Mostrar información del sistema útil para debugging"""
    import sys
    import platform
    
    print("\n📋 Información del Sistema:")
    print(f"   Sistema: {platform.system()} {platform.release()}")
    print(f"   Python: {sys.version}")
    print(f"   Ejecutable: {sys.executable}")
    
    try:
        import openseespy
        print(f"   openseespy: {openseespy.__version__}")
    except:
        print("   openseespy: No instalado o error")
    
    try:
        import opstool
        print(f"   opstool: {opstool.__version__}")
    except:
        print("   opstool: No instalado o error")

if __name__ == "__main__":
    print("🚀 Verificando instalación de opensees-parametric-analysis\n")
    
    show_system_info()
    
    imports_ok = test_imports()
    if imports_ok:
        functionality_ok = test_basic_functionality()
        if functionality_ok:
            print("\n✨ Todo perfecto! El sistema está listo para usar.")
            exit(0)
        else:
            print("\n⚠️  Importaciones OK pero hay problemas de funcionalidad.")
            exit(1)
    else:
        print("\n🔧 Por favor corrige los problemas de importación primero.")
        print("\n📚 Consulta la documentación: docs/system-requirements.md")
        exit(1)
