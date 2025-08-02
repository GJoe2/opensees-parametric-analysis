"""
Ejemplo 03: Tipos de Análisis Específicos
=========================================

Este ejemplo muestra cómo ejecutar diferentes tipos de análisis:
- Solo análisis estático
- Solo análisis modal
- Análisis dinámico
- Análisis completo (todos los tipos)

Caso de uso: Selección de análisis según objetivos de investigación
"""

from src.model_builder import ModelBuilder
from src.analysis_engine import AnalysisEngine

def main():
    """Ejemplo de diferentes tipos de análisis"""
    
    print("=== Ejemplo 03: Tipos de Análisis Específicos ===")
    
    # Configurar componentes
    builder = ModelBuilder(output_dir="models")
    engine = AnalysisEngine()
    
    # Parámetros del modelo base
    L_B_ratio = 2.0
    B = 12.0
    nx = 5
    ny = 3
    
    print(f"Modelo base: L/B={L_B_ratio}, B={B}m, ejes={nx}x{ny}")
    
    # === ANÁLISIS 1: Solo Estático ===
    print("\n1️⃣ SOLO ANÁLISIS ESTÁTICO")
    print("   Objetivo: Evaluar desplazamientos bajo carga estática")
    
    model_static = builder.create_model(
        L_B_ratio=L_B_ratio, B=B, nx=nx, ny=ny,
        model_name="ejemplo_03_estatico",
        enabled_analyses=['static'],
        analysis_params={
            'static': {
                'steps': 20,           # Más pasos para mejor convergencia
                'algorithm': 'Newton', # Algoritmo más robusto
                'tolerance': 1e-8      # Mayor precisión
            },
            'visualization': {'enabled': False}  # Sin viz para velocidad
        }
    )
    
    print(f"   Modelo creado: {model_static['name']}")
    results_static = engine.analyze_model(model_static['file_path'])
    
    if results_static['static_analysis']['success']:
        static_data = results_static['static_analysis']
        print(f"   ✅ Desplazamiento máximo: {static_data['max_displacement']:.6f} m")
        print(f"   📍 Nodo crítico: {static_data['max_displacement_node']}")
    
    # === ANÁLISIS 2: Solo Modal ===
    print("\n2️⃣ SOLO ANÁLISIS MODAL")
    print("   Objetivo: Caracterizar propiedades dinámicas")
    
    model_modal = builder.create_model(
        L_B_ratio=L_B_ratio, B=B, nx=nx, ny=ny,
        model_name="ejemplo_03_modal",
        enabled_analyses=['modal'],
        analysis_params={
            'modal': {
                'num_modes': 12,                # Más modos para análisis completo
                'eigen_solver': 'fullGenLapack' # Solver más preciso
            },
            'visualization': {'enabled': False}
        }
    )
    
    print(f"   Modelo creado: {model_modal['name']}")
    results_modal = engine.analyze_model(model_modal['file_path'])
    
    if results_modal['modal_analysis']['success']:
        modal_data = results_modal['modal_analysis']
        print(f"   ✅ Periodo fundamental: {modal_data['fundamental_period']:.4f} s")
        print(f"   🌊 Frecuencia fundamental: {modal_data['fundamental_frequency']:.2f} Hz")
        print(f"   📊 Modos calculados: {len(modal_data['periods'])}")
        
        # Mostrar todos los periodos
        print("   📈 Periodos modales:")
        for i, period in enumerate(modal_data['periods'], 1):
            freq = 1.0 / period
            print(f"      Modo {i:2d}: T = {period:.4f} s, f = {freq:.2f} Hz")
    
    # === ANÁLISIS 3: Dinámico (Estático + Dinámico) ===
    print("\n3️⃣ ANÁLISIS DINÁMICO")
    print("   Objetivo: Respuesta en el tiempo")
    
    model_dynamic = builder.create_model(
        L_B_ratio=L_B_ratio, B=B, nx=nx, ny=ny,
        model_name="ejemplo_03_dinamico",
        enabled_analyses=['static', 'dynamic'],
        analysis_params={
            'static': {'steps': 15},
            'dynamic': {
                'dt': 0.01,           # Paso de tiempo
                'num_steps': 1000,    # Duración del análisis
                'damping_ratio': 0.05, # Amortiguamiento
                'integrator': 'Newmark',
                'gamma': 0.5,
                'beta': 0.25
            },
            'visualization': {'enabled': False}
        }
    )
    
    print(f"   Modelo creado: {model_dynamic['name']}")
    results_dynamic = engine.analyze_model(model_dynamic['file_path'])
    
    if results_dynamic['static_analysis']['success']:
        print(f"   ✅ Análisis estático: OK")
    if results_dynamic['dynamic_analysis']['success']:
        dynamic_data = results_dynamic['dynamic_analysis']
        print(f"   ✅ Análisis dinámico: {dynamic_data['num_steps']} pasos completados")
        print(f"   ⏱️  Duración simulada: {dynamic_data['total_time']:.2f} s")
    
    # === ANÁLISIS 4: Completo (Todos los tipos) ===
    print("\n4️⃣ ANÁLISIS COMPLETO (Static + Modal + Dynamic)")
    print("   Objetivo: Caracterización estructural completa")
    
    model_complete = builder.create_model(
        L_B_ratio=L_B_ratio, B=B, nx=nx, ny=ny,
        model_name="ejemplo_03_completo",
        enabled_analyses=['static', 'modal', 'dynamic'],
        analysis_params={
            'static': {
                'steps': 15,
                'algorithm': 'Newton'
            },
            'modal': {
                'num_modes': 10
            },
            'dynamic': {
                'dt': 0.005,
                'num_steps': 2000,
                'damping_ratio': 0.05
            },
            'visualization': {'enabled': False}  # Sin viz para este ejemplo
        }
    )
    
    print(f"   Modelo creado: {model_complete['name']}")
    results_complete = engine.analyze_model(model_complete['file_path'])
    
    # Resumen de resultados completos
    analysis_status = []
    if 'static_analysis' in results_complete:
        status = "✅" if results_complete['static_analysis']['success'] else "❌"
        analysis_status.append(f"   {status} Estático")
        
    if 'modal_analysis' in results_complete:
        status = "✅" if results_complete['modal_analysis']['success'] else "❌"
        analysis_status.append(f"   {status} Modal")
        
    if 'dynamic_analysis' in results_complete:
        status = "✅" if results_complete['dynamic_analysis']['success'] else "❌"
        analysis_status.append(f"   {status} Dinámico")
    
    print("\\n".join(analysis_status))
    
    # === RESUMEN COMPARATIVO ===
    print("\n" + "="*60)
    print("📊 RESUMEN COMPARATIVO DE ANÁLISIS")
    print("="*60)
    print("Tipo              | Tiempo | Información obtenida")
    print("-" * 60)
    print("Solo Estático     | Rápido | Desplazamientos, reacciones")
    print("Solo Modal        | Medio  | Periodos, frecuencias, formas modales")
    print("Dinámico          | Lento  | Respuesta temporal, historia")
    print("Completo          | Muy Lento | Caracterización total")
    print()
    print("💡 RECOMENDACIONES:")
    print("- Diseño preliminar: Solo estático")
    print("- Análisis sísmico: Modal + dinámico")
    print("- Investigación: Análisis completo")
    print("- Estudios paramétricos: Solo estático o modal")

if __name__ == "__main__":
    main()
