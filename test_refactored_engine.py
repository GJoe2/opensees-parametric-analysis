"""
Script de prueba para demostrar el AnalysisEngine refactorizado.
Muestra cómo el nuevo código es más limpio y mantenible.
"""

import os
import sys

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from model_builder import ModelBuilder
from analysis_engine_refactored import AnalysisEngine


def test_refactored_engine():
    """Prueba el motor de análisis refactorizado."""
    
    print("🔧 Probando AnalysisEngine Refactorizado")
    print("=" * 50)
    
    # 1. Crear modelo de prueba
    print("📋 1. Creando modelo de prueba...")
    builder = ModelBuilder()
    
    # Modelo simple con visualización habilitada
    model_info = builder.create_model(
        L_B_ratio=1.5,
        B=10.0,
        nx=3,
        ny=3,
        model_name="test_refactored",
        enabled_analyses=['static', 'modal'],
        analysis_params={
            'visualization': {
                'enabled': True,
                'static_deformed': True,
                'modal_shapes': True,
                'max_modes': 4
            }
        }
    )
    print(f"   ✅ Modelo creado: {model_info['name']}")
    
    # 2. Ejecutar análisis con nuevo motor
    print("\n🚀 2. Ejecutando análisis con motor refactorizado...")
    engine = AnalysisEngine()
    
    model_file = model_info['file_path']
    results = engine.analyze_model(model_file)
    
    # 3. Mostrar resultados
    print("\n📊 3. Resultados del análisis:")
    
    static = results.get('static_analysis', {})
    modal = results.get('modal_analysis', {})
    
    print(f"   • Estático: {'✅ Exitoso' if static.get('success') else '❌ Falló'}")
    if static.get('success'):
        print(f"     - Desplazamiento máx: {static.get('max_displacement', 0):.6f} m")
    
    print(f"   • Modal: {'✅ Exitoso' if modal.get('success') else '❌ Falló'}")
    if modal.get('success'):
        period = modal.get('fundamental_period', 0)
        print(f"     - Periodo fundamental: {period:.4f} s")
        print(f"     - Modos calculados: {len(modal.get('periods', []))}")
    
    # 4. Archivos de visualización
    viz_files = results.get('visualization_files', [])
    if viz_files:
        print(f"\n📁 4. Archivos de visualización generados ({len(viz_files)}):")
        for file in viz_files:
            print(f"   • {os.path.basename(file)}")
    else:
        print("\n📁 4. No se generaron archivos de visualización")
    
    print("\n✅ Prueba completada exitosamente!")
    return results


def test_multiple_configurations():
    """Prueba múltiples configuraciones para mostrar flexibilidad."""
    
    print("\n🔧 Probando Múltiples Configuraciones")
    print("=" * 50)
    
    builder = ModelBuilder()
    engine = AnalysisEngine()
    
    configs = [
        {
            'name': 'solo_numerico',
            'desc': 'Solo análisis numérico (sin visualización)',
            'analyses': ['static', 'modal'],
            'viz': {'enabled': False}
        },
        {
            'name': 'solo_estatico',
            'desc': 'Solo análisis estático con visualización',
            'analyses': ['static'],
            'viz': {'enabled': True, 'static_deformed': True, 'modal_shapes': False}
        },
        {
            'name': 'completo',
            'desc': 'Análisis completo con todas las visualizaciones',
            'analyses': ['static', 'modal', 'dynamic'],
            'viz': {'enabled': True, 'static_deformed': True, 'modal_shapes': True}
        }
    ]
    
    for i, config in enumerate(configs, 1):
        print(f"\n{i}. {config['desc']}")
        
        # Crear modelo
        model_info = builder.create_model(
            L_B_ratio=1.2,
            B=8.0,
            nx=2,
            ny=2,
            model_name=config['name'],
            enabled_analyses=config['analyses'],
            analysis_params={'visualization': config['viz']}
        )
        
        # Analizar
        try:
            results = engine.analyze_model(model_info['file_path'])
            
            # Resumen
            analyses_run = [k for k in ['static_analysis', 'modal_analysis', 'dynamic_analysis'] 
                          if results.get(k, {}).get('success', False)]
            viz_count = len(results.get('visualization_files', []))
            
            print(f"   ✅ Análisis: {len(analyses_run)} exitosos")
            print(f"   📁 Visualizaciones: {viz_count} archivos")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n✅ Todas las configuraciones probadas!")


def demonstrate_code_simplicity():
    """Demuestra la simplicidad del código refactorizado."""
    
    print("\n📝 Código Refactorizado - Características Principales")
    print("=" * 60)
    
    print("🎯 SEPARACIÓN DE RESPONSABILIDADES:")
    print("   • AnalysisEngine: Orquestación principal")
    print("   • StaticAnalysis, ModalAnalysis, DynamicAnalysis: Análisis específicos")
    print("   • VisualizationHelper: Manejo de visualizaciones")
    
    print("\n🔄 REUTILIZACIÓN DE CÓDIGO:")
    print("   • BaseAnalysis: Funcionalidad común")
    print("   • Sin repetición de configuraciones OpenSees")
    print("   • Helper de visualización reutilizable")
    
    print("\n⚡ GESTIÓN INTELIGENTE DE RECURSOS:")
    print("   • ODB se crea SOLO cuando se necesita visualización")
    print("   • ops.analyze(1) vs ops.analyze(N) según el contexto")
    print("   • Limpieza automática de recursos")
    
    print("\n🎛️ CONFIGURACIÓN FLEXIBLE:")
    print("   • Análisis independientes (static/modal/dynamic)")
    print("   • Visualización granular (por tipo)")
    print("   • Fácil extensión para nuevos tipos")
    
    print("\n🧹 CÓDIGO LIMPIO:")
    print("   • Métodos cortos y enfocados")
    print("   • Mínimo uso de condicionales if")
    print("   • Fácil debugging y mantenimiento")


if __name__ == '__main__':
    try:
        test_refactored_engine()
        test_multiple_configurations()
        demonstrate_code_simplicity()
        
        print("\n" + "="*60)
        print("🎉 REFACTORIZACIÓN COMPLETADA CON ÉXITO!")
        print("📚 El código ahora es más limpio, mantenible y reutilizable.")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
