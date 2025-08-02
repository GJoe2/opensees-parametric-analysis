"""
Ejemplo 02: Control de Visualización
====================================

Este ejemplo demuestra las diferentes opciones de visualización:
- Sin visualización (análisis rápido)
- Solo deformada estática
- Solo formas modales  
- Visualización completa

Caso de uso: Control granular de outputs según necesidad
"""

from src.model_builder import ModelBuilder
from src.analysis_engine import AnalysisEngine

def main():
    """Ejemplo de control de visualización"""
    
    print("=== Ejemplo 02: Control de Visualización ===")
    
    # Configurar componentes
    builder = ModelBuilder(output_dir="models")
    engine = AnalysisEngine()
    
    # Parámetros del modelo base
    L_B_ratio = 1.5
    B = 10.0
    nx = 4
    ny = 3
    
    # === CASO 1: Sin visualización (máxima velocidad) ===
    print("\n1️⃣ Análisis SIN visualización (máxima velocidad)")
    
    model_fast = builder.create_model(
        L_B_ratio=L_B_ratio, B=B, nx=nx, ny=ny,
        model_name="ejemplo_02_sin_viz",
        analysis_params={
            'visualization': {'enabled': False}
        }
    )
    
    print(f"   Modelo creado: {model_fast['name']}")
    results_fast = engine.analyze_model(model_fast['file_path'])
    
    viz_files = results_fast.get('visualization_files', [])
    print(f"   ✅ Análisis completado - Archivos de viz: {len(viz_files)}")
    
    # === CASO 2: Solo deformada estática ===
    print("\n2️⃣ Solo DEFORMADA ESTÁTICA")
    
    model_static_viz = builder.create_model(
        L_B_ratio=L_B_ratio, B=B, nx=nx, ny=ny,
        model_name="ejemplo_02_deformada",
        analysis_params={
            'visualization': {
                'enabled': True,
                'static_deformed': True,
                'modal_shapes': False,
                'deform_scale': 100
            }
        }
    )
    
    print(f"   Modelo creado: {model_static_viz['name']}")
    results_static = engine.analyze_model(model_static_viz['file_path'])
    
    viz_files = results_static.get('visualization_files', [])
    print(f"   ✅ Análisis completado - Archivos de viz: {len(viz_files)}")
    for file in viz_files:
        print(f"      - {file}")
    
    # === CASO 3: Solo formas modales ===
    print("\n3️⃣ Solo FORMAS MODALES")
    
    model_modal_viz = builder.create_model(
        L_B_ratio=L_B_ratio, B=B, nx=nx, ny=ny,
        model_name="ejemplo_02_modal",
        analysis_params={
            'modal': {'num_modes': 6},
            'visualization': {
                'enabled': True,
                'static_deformed': False,
                'modal_shapes': True,
                'max_modes': 6,
                'deform_scale': 150
            }
        }
    )
    
    print(f"   Modelo creado: {model_modal_viz['name']}")
    results_modal = engine.analyze_model(model_modal_viz['file_path'])
    
    viz_files = results_modal.get('visualization_files', [])
    print(f"   ✅ Análisis completado - Archivos de viz: {len(viz_files)}")
    for file in viz_files:
        print(f"      - {file}")
    
    # === CASO 4: Visualización completa (presentación) ===
    print("\n4️⃣ VISUALIZACIÓN COMPLETA (para presentación)")
    
    model_complete_viz = builder.create_model(
        L_B_ratio=L_B_ratio, B=B, nx=nx, ny=ny,
        model_name="ejemplo_02_completo",
        analysis_params={
            'static': {'steps': 15},
            'modal': {'num_modes': 8},
            'visualization': {
                'enabled': True,
                'static_deformed': True,
                'modal_shapes': True,
                'max_modes': 8,
                'deform_scale': 200,
                'show_nodes': True,
                'line_width': 3
            }
        }
    )
    
    print(f"   Modelo creado: {model_complete_viz['name']}")
    results_complete = engine.analyze_model(model_complete_viz['file_path'])
    
    viz_files = results_complete.get('visualization_files', [])
    print(f"   ✅ Análisis completado - Archivos de viz: {len(viz_files)}")
    for file in viz_files:
        print(f"      - {file}")
    
    # === RESUMEN ===
    print("\n" + "="*50)
    print("📊 RESUMEN DE CASOS DE VISUALIZACIÓN")
    print("="*50)
    print("Caso 1 - Sin viz:       Archivos = 0 (máxima velocidad)")
    print("Caso 2 - Deformada:     Archivos = 1 (verificación rápida)")
    print("Caso 3 - Modal:         Archivos = 6 (análisis dinámico)")
    print("Caso 4 - Completo:      Archivos = 9 (presentación)")
    print()
    print("💡 RECOMENDACIONES DE USO:")
    print("- Estudios paramétricos grandes: Sin visualización")
    print("- Verificación de modelos: Solo deformada estática")
    print("- Análisis dinámico: Solo formas modales")
    print("- Reportes y presentaciones: Visualización completa")

if __name__ == "__main__":
    main()
