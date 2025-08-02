"""
Ejemplo de uso del AnalysisEngine refactorizado.
Demuestra cómo el nuevo código es más limpio y fácil de usar.
"""

import os
import sys

# Configurar path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def ejemplo_uso_basico():
    """Ejemplo básico de uso del motor refactorizado."""
    
    from model_builder import ModelBuilder
    from analysis_engine_refactored import AnalysisEngine
    
    print("🎯 EJEMPLO: Uso Básico del Motor Refactorizado")
    print("=" * 50)
    
    # 1. Crear modelo
    builder = ModelBuilder()
    engine = AnalysisEngine()
    
    # Modelo simple sin visualización (máxima velocidad)
    model_info = builder.create_model(
        L_B_ratio=1.5,
        B=10.0,
        nx=4,
        ny=4,
        enabled_analyses=['static', 'modal'],
        analysis_params={
            'visualization': {'enabled': False}  # Solo números
        }
    )
    
    # 2. Ejecutar análisis
    results = engine.analyze_model(model_info['file_path'])
    
    # 3. Extraer resultados principales
    static = results['static_analysis']
    modal = results['modal_analysis']
    
    print(f"📊 Resultados para {results['model_name']}:")
    print(f"   • Desplazamiento máximo: {static['max_displacement']:.6f} m")
    print(f"   • Periodo fundamental: {modal['fundamental_period']:.4f} s")
    print(f"   • Tiempo de análisis: Optimizado (sin visualización)")


def ejemplo_con_visualizacion():
    """Ejemplo con visualización selectiva."""
    
    from model_builder import ModelBuilder
    from analysis_engine_refactored import AnalysisEngine
    
    print("\n🎨 EJEMPLO: Con Visualización Selectiva")
    print("=" * 50)
    
    builder = ModelBuilder()
    engine = AnalysisEngine()
    
    # Modelo con visualización específica
    model_info = builder.create_model(
        L_B_ratio=1.2,
        B=8.0,
        nx=3,
        ny=3,
        enabled_analyses=['static', 'modal'],
        analysis_params={
            'visualization': {
                'enabled': True,
                'static_deformed': True,    # Sí - deformada estática
                'modal_shapes': True,       # Sí - formas modales  
                'max_modes': 4              # Solo primeros 4 modos
            }
        }
    )
    
    results = engine.analyze_model(model_info['file_path'])
    
    # Archivos generados
    viz_files = results.get('visualization_files', [])
    print(f"📁 Archivos de visualización generados ({len(viz_files)}):")
    for file in viz_files:
        print(f"   • {os.path.basename(file)}")


def ejemplo_estudio_parametrico():
    """Ejemplo de estudio paramétrico eficiente."""
    
    from model_builder import ModelBuilder
    from analysis_engine_refactored import AnalysisEngine
    
    print("\n📈 EJEMPLO: Estudio Paramétrico Eficiente")
    print("=" * 50)
    
    builder = ModelBuilder()
    engine = AnalysisEngine()
    
    # Parámetros a estudiar
    L_B_ratios = [1.0, 1.5, 2.0]
    B_values = [8.0, 10.0, 12.0]
    
    resultados_parametricos = []
    
    for L_B in L_B_ratios:
        for B in B_values:
            # Crear modelo SIN visualización para máxima velocidad
            model_info = builder.create_model(
                L_B_ratio=L_B,
                B=B,
                nx=3,
                ny=3,
                model_name=f"param_LB{L_B:.1f}_B{B:.0f}",
                enabled_analyses=['static', 'modal'],
                analysis_params={
                    'visualization': {'enabled': False}  # Sin visualización
                }
            )
            
            # Analizar
            results = engine.analyze_model(model_info['file_path'])
            
            # Extraer datos clave
            resultados_parametricos.append({
                'L_B_ratio': L_B,
                'B': B,
                'max_displacement': results['static_analysis']['max_displacement'],
                'fundamental_period': results['modal_analysis']['fundamental_period']
            })
    
    # Mostrar resumen
    print("📊 Resumen del estudio paramétrico:")
    print("L/B  | B(m) | Despl.Max(m) | T1(s)")
    print("-" * 35)
    for r in resultados_parametricos:
        print(f"{r['L_B_ratio']:.1f}  | {r['B']:4.0f} | {r['max_displacement']:.6f} | {r['fundamental_period']:.4f}")


def ejemplo_configuracion_avanzada():
    """Ejemplo de configuración avanzada personalizada."""
    
    from model_builder import ModelBuilder
    from analysis_engine_refactored import AnalysisEngine
    
    print("\n🔧 EJEMPLO: Configuración Avanzada")
    print("=" * 50)
    
    builder = ModelBuilder()
    engine = AnalysisEngine()
    
    # Configuración personalizada detallada
    model_info = builder.create_model(
        L_B_ratio=1.5,
        B=10.0,
        nx=4,
        ny=4,
        enabled_analyses=['static', 'modal', 'dynamic'],
        analysis_params={
            # Configuración específica de análisis estático
            'static': {
                'system': 'BandGeneral',
                'algorithm': 'Newton',  # Algoritmo no lineal
                'steps': 20
            },
            # Configuración específica de análisis modal
            'modal': {
                'num_modes': 12  # Más modos
            },
            # Configuración específica de análisis dinámico
            'dynamic': {
                'dt': 0.001,      # Paso de tiempo más fino
                'num_steps': 1000
            },
            # Visualización granular
            'visualization': {
                'enabled': True,
                'static_deformed': True,
                'modal_shapes': True,
                'max_modes': 6,
                'deform_scale': 150  # Factor de escala personalizado
            }
        }
    )
    
    results = engine.analyze_model(model_info['file_path'])
    
    # Mostrar resultados de todos los análisis
    print(f"📊 Resultados completos:")
    for analysis_type in ['static_analysis', 'modal_analysis', 'dynamic_analysis']:
        result = results.get(analysis_type, {})
        status = "✅ Exitoso" if result.get('success') else "❌ Falló"
        print(f"   • {analysis_type.replace('_', ' ').title()}: {status}")


if __name__ == '__main__':
    print("🚀 EJEMPLOS DE USO - ANALYSIS ENGINE REFACTORIZADO")
    print("=" * 60)
    
    try:
        ejemplo_uso_basico()
        ejemplo_con_visualizacion()
        ejemplo_estudio_parametrico()
        ejemplo_configuracion_avanzada()
        
        print("\n" + "=" * 60)
        print("✅ TODOS LOS EJEMPLOS EJECUTADOS EXITOSAMENTE")
        print("📚 El nuevo código es más limpio, flexible y eficiente.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error en los ejemplos: {e}")
        import traceback
        traceback.print_exc()
