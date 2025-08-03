"""
Ejemplo 01: Análisis Individual Básico
======================================

Este ejemplo muestra cómo crear y analizar un modelo individual
con configuración básica (estático + modal).

Caso de uso: Análisis rápido de un edificio específico
"""

from src.model_builder import ModelBuilder
from src.analysis_engine import AnalysisEngine

def main():
    """Ejemplo básico de análisis individual"""
    
    print("=== Ejemplo 01: Análisis Individual Básico ===")
    
    # 1. Configurar componentes
    builder = ModelBuilder(output_dir="models")
    engine = AnalysisEngine()
    
    # 2. Parámetros del modelo
    L_B_ratio = 1.5   # Relación largo/ancho
    B = 10.0          # Ancho en metros  
    nx = 4            # Ejes en X
    ny = 4            # Ejes en Y
    
    print(f"Creando modelo: L/B={L_B_ratio}, B={B}m, ejes={nx}x{ny}")
    
    # 3. Crear modelo con configuración por defecto
    model_info = builder.create_model(
        L_B_ratio=L_B_ratio, 
        B=B, 
        nx=nx, 
        ny=ny,
        model_name="ejemplo_01"
    )
    
    print(f"Modelo creado: {model_info['name']}")
    print(f"Archivo: {model_info['file_path']}")
    
    # 4. Ejecutar análisis
    print("\nEjecutando análisis...")
    results = engine.analyze_model(model_info['file_path'])
    
    # 5. Mostrar resultados principales
    print("\n=== RESULTADOS ===")
    
    if 'static_analysis' in results and results['static_analysis']['success']:
        static_results = results['static_analysis']
        print(f"✅ Análisis Estático:")
        print(f"   Desplazamiento máximo: {static_results['max_displacement']:.6f} m")
        print(f"   Nodo con máx. desplazamiento: {static_results['max_displacement_node']}")
    
    if 'modal_analysis' in results and results['modal_analysis']['success']:
        modal_results = results['modal_analysis']
        print(f"✅ Análisis Modal:")
        print(f"   Periodo fundamental: {modal_results['fundamental_period']:.4f} s")
        print(f"   Frecuencia fundamental: {modal_results['fundamental_frequency']:.2f} Hz")
        print(f"   Número de modos calculados: {len(modal_results['periods'])}")
        
        # Mostrar primeros 3 periodos
        print("   Primeros 3 periodos:")
        for i, period in enumerate(modal_results['periods'][:3], 1):
            print(f"     Modo {i}: T = {period:.4f} s")
    
    # 6. Información sobre archivos generados
    if 'visualization_files' in results:
        viz_files = results['visualization_files']
        if viz_files:
            print(f"\n📊 Archivos de visualización generados: {len(viz_files)}")
            for file in viz_files:
                print(f"   - {file}")
        else:
            print("\n📊 No se generaron archivos de visualización (disabled por defecto)")
    
    print(f"\n✅ Análisis completado exitosamente!")
    print(f"📁 Resultados guardados en: results/{model_info['name']}_results.json")

if __name__ == "__main__":
    main()
