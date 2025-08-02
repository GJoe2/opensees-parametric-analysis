"""
Ejemplo 04: Estudio Paramétrico Completo
========================================

Este ejemplo muestra cómo ejecutar estudios paramétricos para analizar
la influencia de diferentes parámetros geométricos en el comportamiento estructural.

Caso de uso: Investigación paramétrica de edificios de hormigón armado
"""

from src.model_builder import ModelBuilder
from src.analysis_engine import AnalysisEngine
from src.parametric_runner import ParametricRunner
from src.report_generator import ReportGenerator

def main():
    """Ejemplo de estudio paramétrico completo"""
    
    print("=== Ejemplo 04: Estudio Paramétrico Completo ===")
    
    # === CONFIGURACIÓN DEL ESTUDIO ===
    print("\n📋 Configurando estudio paramétrico...")
    
    # Configurar componentes
    builder = ModelBuilder(output_dir="models")
    engine = AnalysisEngine()
    runner = ParametricRunner(builder, engine)
    
    # === ESTUDIO 1: Sensibilidad a relación L/B ===
    print("\n1️⃣ ESTUDIO DE SENSIBILIDAD - Relación L/B")
    print("   Objetivo: Analizar influencia de la relación largo/ancho")
    
    results_LB = runner.run_full_study(
        L_B_ratios=[1.0, 1.5, 2.0, 2.5],  # Variable de estudio
        B_values=[10.0],                   # Fijo
        nx_values=[4],                     # Fijo  
        ny_values=[3],                     # Fijo
        selection_method="all",
        analysis_distribution={"static": 0.6, "modal": 0.4},  # Mix de análisis
        progress_bar=True
    )
    
    print(f"   ✅ Completado: {len(results_LB)} modelos analizados")
    
    # Mostrar tendencias en relación L/B
    print("   📊 Tendencias observadas:")
    for result in results_LB:
        params = result['model_parameters']
        LB = params['L_B_ratio']
        
        if 'static_analysis' in result['results'] and result['results']['static_analysis']['success']:
            disp = result['results']['static_analysis']['max_displacement']
            print(f"      L/B = {LB:.1f}: Despl. máx = {disp:.6f} m")
        
        if 'modal_analysis' in result['results'] and result['results']['modal_analysis']['success']:
            period = result['results']['modal_analysis']['fundamental_period']
            print(f"      L/B = {LB:.1f}: Periodo = {period:.4f} s")
    
    # === ESTUDIO 2: Sensibilidad al tamaño (B) ===
    print("\n2️⃣ ESTUDIO DE SENSIBILIDAD - Tamaño del edificio (B)")
    print("   Objetivo: Analizar influencia del tamaño absoluto")
    
    results_B = runner.run_full_study(
        L_B_ratios=[1.5],                  # Fijo
        B_values=[8.0, 12.0, 16.0, 20.0], # Variable de estudio
        nx_values=[4],                     # Fijo
        ny_values=[3],                     # Fijo
        selection_method="all",
        analysis_distribution={"modal": 1.0},  # Solo análisis modal
        progress_bar=True
    )
    
    print(f"   ✅ Completado: {len(results_B)} modelos analizados")
    
    # Mostrar tendencias en tamaño B
    print("   📊 Tendencias observadas:")
    for result in results_B:
        params = result['model_parameters']
        B = params['B']
        
        if 'modal_analysis' in result['results'] and result['results']['modal_analysis']['success']:
            period = result['results']['modal_analysis']['fundamental_period']
            freq = result['results']['modal_analysis']['fundamental_frequency']
            print(f"      B = {B:.1f}m: T₁ = {period:.4f} s, f₁ = {freq:.2f} Hz")
    
    # === ESTUDIO 3: Sensibilidad a la discretización ===
    print("\n3️⃣ ESTUDIO DE SENSIBILIDAD - Discretización (nx, ny)")
    print("   Objetivo: Analizar influencia del número de ejes")
    
    results_mesh = runner.run_full_study(
        L_B_ratios=[2.0],           # Fijo
        B_values=[15.0],            # Fijo
        nx_values=[3, 4, 5, 6],     # Variable
        ny_values=[2, 3, 4],        # Variable
        selection_method="all",
        analysis_distribution={"static": 1.0},  # Solo análisis estático
        progress_bar=True
    )
    
    print(f"   ✅ Completado: {len(results_mesh)} modelos analizados")
    
    # Mostrar influencia de la discretización
    print("   📊 Tendencias observadas:")
    for result in results_mesh:
        params = result['model_parameters']
        nx = params['nx']
        ny = params['ny']
        
        if 'static_analysis' in result['results'] and result['results']['static_analysis']['success']:
            disp = result['results']['static_analysis']['max_displacement']
            print(f"      {nx}x{ny} ejes: Despl. máx = {disp:.6f} m")
    
    # === ESTUDIO 4: Estudio factorial completo (muestra pequeña) ===
    print("\n4️⃣ ESTUDIO FACTORIAL - Muestra representativa")
    print("   Objetivo: Analizar interacciones entre múltiples parámetros")
    
    results_factorial = runner.run_full_study(
        L_B_ratios=[1.5, 2.0],      # 2 niveles
        B_values=[10.0, 15.0],      # 2 niveles
        nx_values=[3, 4],           # 2 niveles
        ny_values=[3, 4],           # 2 niveles
        selection_method="all",      # 2×2×2×2 = 16 combinaciones
        analysis_distribution={"static": 0.5, "modal": 0.5},
        progress_bar=True
    )
    
    print(f"   ✅ Completado: {len(results_factorial)} modelos analizados")
    
    # === ANÁLISIS DE RESULTADOS AGREGADOS ===
    print("\n" + "="*60)
    print("📊 ANÁLISIS AGREGADO DE TODOS LOS ESTUDIOS")
    print("="*60)
    
    # Combinar todos los resultados
    all_results = results_LB + results_B + results_mesh + results_factorial
    
    # Estadísticas generales
    total_models = len(all_results)
    successful_static = sum(1 for r in all_results 
                           if 'static_analysis' in r['results'] 
                           and r['results']['static_analysis']['success'])
    successful_modal = sum(1 for r in all_results 
                          if 'modal_analysis' in r['results'] 
                          and r['results']['modal_analysis']['success'])
    
    print(f"📈 Modelos totales analizados: {total_models}")
    print(f"✅ Análisis estáticos exitosos: {successful_static}")
    print(f"🌊 Análisis modales exitosos: {successful_modal}")
    
    # Rangos de resultados
    if successful_static > 0:
        displacements = [r['results']['static_analysis']['max_displacement'] 
                        for r in all_results 
                        if 'static_analysis' in r['results'] 
                        and r['results']['static_analysis']['success']]
        
        print(f"📏 Rango de desplazamientos:")
        print(f"   Mínimo: {min(displacements):.6f} m")
        print(f"   Máximo: {max(displacements):.6f} m")
        print(f"   Promedio: {sum(displacements)/len(displacements):.6f} m")
    
    if successful_modal > 0:
        periods = [r['results']['modal_analysis']['fundamental_period'] 
                  for r in all_results 
                  if 'modal_analysis' in r['results'] 
                  and r['results']['modal_analysis']['success']]
        
        print(f"⏱️  Rango de periodos fundamentales:")
        print(f"   Mínimo: {min(periods):.4f} s")
        print(f"   Máximo: {max(periods):.4f} s")
        print(f"   Promedio: {sum(periods)/len(periods):.4f} s")
    
    # === GENERACIÓN DE REPORTES (OPCIONAL) ===
    print("\n📋 Generando reporte consolidado...")
    
    try:
        reporter = ReportGenerator(results_dir="results", reports_dir="reports")
        
        # Generar reporte HTML con todos los resultados
        report_path = reporter.generate_comprehensive_report(
            all_results, 
            report_name="estudio_parametrico_ejemplo_04"
        )
        print(f"📄 Reporte generado: {report_path}")
        
    except Exception as e:
        print(f"⚠️  No se pudo generar reporte automático: {e}")
        print("   Los resultados están disponibles en archivos JSON individuales")
    
    # === CONCLUSIONES ===
    print("\n" + "="*60)
    print("🎯 CONCLUSIONES DEL ESTUDIO PARAMÉTRICO")
    print("="*60)
    print("1. La relación L/B tiene impacto significativo en desplazamientos")
    print("2. El tamaño absoluto (B) influye principalmente en periodos")
    print("3. La discretización afecta la precisión de resultados")
    print("4. Las interacciones entre parámetros son detectables")
    print()
    print("💡 RECOMENDACIONES PARA ESTUDIOS FUTUROS:")
    print("- Usar más niveles para curvas de tendencia")
    print("- Incluir análisis dinámico para sismos")
    print("- Considerar diferentes condiciones de carga")
    print("- Automatizar generación de reportes")

if __name__ == "__main__":
    main()
