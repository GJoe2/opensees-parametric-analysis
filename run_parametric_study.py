"""
Script principal para ejecutar estudios paramétricos completos.
Demuestra la nueva arquitectura simplificada donde:
- ModelBuilder: Maneja toda la configuración de análisis
- AnalysisEngine: Solo ejecuta (lee configuración del JSON)
- ParametricRunner: Orquesta el proceso
"""

from src.model_builder import ModelBuilder
from src.analysis_engine import AnalysisEngine
from src.report_generator import ReportGenerator
from src.python_exporter import PythonExporter
from src.parametric_runner import ParametricRunner

def main():
    """Ejecuta estudio paramétrico con arquitectura simplificada."""
    
    # 1. Inicializar componentes (más simple ahora)
    builder = ModelBuilder(output_dir="models")
    engine = AnalysisEngine(models_dir="models", results_dir="results")  # Sin configuración propia
    reporter = ReportGenerator(results_dir="results")
    exporter = PythonExporter(output_dir="models")
    
    # 2. Crear orquestador
    runner = ParametricRunner(builder, engine, reporter, exporter)
    
    # 3. Definir parámetros del estudio
    L_B_ratios = [1.0, 1.5, 2.0]
    B_values = [8.0, 10.0, 12.0]
    nx_values = [3, 4, 5]
    ny_values = [3, 4, 5]
    # Total: 3 × 3 × 3 × 3 = 81 modelos
    
    print("=== ESTUDIO PARAMÉTRICO SIMPLIFICADO ===")
    print(f"Combinaciones totales: {len(L_B_ratios) * len(B_values) * len(nx_values) * len(ny_values)}")
    
    # 4. OPCIÓN 1: Distribución aleatoria
    print("\n--- MÉTODO 1: DISTRIBUCIÓN ALEATORIA ---")
    results_random = runner.run_full_study(
        L_B_ratios=L_B_ratios,
        B_values=B_values,
        nx_values=nx_values,
        ny_values=ny_values,
        selection_method="distribution",
        analysis_distribution={
            "static": 0.6,    # 60% solo estático
            "modal": 0.25,    # 25% solo modal
            "complete": 0.15  # 15% completo
        }
    )
    
    print(f"Resultado: {results_random['models_generated']} modelos generados")
    
    # 5. OPCIÓN 2: Por criterios (comentado para no duplicar)
    # print("\n--- MÉTODO 2: POR CRITERIOS ---")
    # results_criteria = runner.run_full_study(
    #     L_B_ratios=L_B_ratios,
    #     B_values=B_values,
    #     nx_values=nx_values,
    #     ny_values=ny_values,
    #     selection_method="criteria",
    #     analysis_criteria={
    #         "complete": {"nx": [5], "ny": [5]},  # Modelos complejos
    #         "modal": {"L_B_ratio": [2.0]},       # Estructuras alargadas
    #         "static": {"nx": [3, 4], "ny": [3, 4]}  # Resto
    #     }
    # )

    # 6. OPCIÓN 3: Híbrido (comentado para no duplicar)
    # print("\n--- MÉTODO 3: HÍBRIDO ---")
    # results_hybrid = runner.run_full_study_hybrid(
    #     L_B_ratios=L_B_ratios,
    #     B_values=B_values,
    #     nx_values=nx_values,
    #     ny_values=ny_values,
    #     criteria_distribution={"criteria": 0.7, "random": 0.3}
    # )

def ejemplo_uso_directo():
    """Ejemplo de uso directo de ModelBuilder sin ParametricRunner."""
    
    print("\n=== USO DIRECTO DE MODELBUILDER ===")
    builder = ModelBuilder(output_dir="models")
    
    # Crear modelos específicos directamente
    print("Creando modelos específicos...")
    
    # Modelo solo estático
    static_model = builder.create_static_only_model(
        L_B_ratio=1.5, B=10.0, nx=4, ny=4,
        model_name="directo_estatico"
    )
    print(f"✓ Estático: {static_model['name']}")
    
    # Modelo solo modal con más modos
    modal_model = builder.create_modal_only_model(
        L_B_ratio=2.0, B=12.0, nx=5, ny=5,
        model_name="directo_modal",
        num_modes=12
    )
    print(f"✓ Modal: {modal_model['name']}")
    
    # Modelo dinámico
    dynamic_model = builder.create_dynamic_model(
        L_B_ratio=1.0, B=8.0, nx=3, ny=3,
        model_name="directo_dinamico",
        dt=0.005, num_steps=5000
    )
    print(f"✓ Dinámico: {dynamic_model['name']}")
    
    # Ahora analizar directamente
    engine = AnalysisEngine()
    
    print("\nAnalizando modelos...")
    static_results = engine.analyze_model(static_model['file_path'])
    modal_results = engine.analyze_model(modal_model['file_path'])
    dynamic_results = engine.analyze_model(dynamic_model['file_path'])
    
    print(f"✓ Análisis estático: {'exitoso' if static_results['static_analysis']['success'] else 'falló'}")
    print(f"✓ Análisis modal: {'exitoso' if modal_results['modal_analysis']['success'] else 'falló'}")
    print(f"✓ Análisis dinámico: pendiente de implementar")

def mostrar_ventajas():
    """Muestra las ventajas de la nueva arquitectura."""
    
    print("\n=== VENTAJAS DE LA NUEVA ARQUITECTURA ===")
    print("✅ ModelBuilder: Controla TODA la configuración de análisis")
    print("✅ AnalysisEngine: Solo ejecuta (más simple, sin configuración redundante)")
    print("✅ JSON: Fuente única de verdad para configuración")
    print("✅ ParametricRunner: Orquesta sin duplicar lógica")
    print("✅ Menos acoplamiento: Cada clase tiene una responsabilidad clara")
    print("✅ Más mantenible: Cambios de configuración solo en ModelBuilder")
    print("✅ Más testeable: Cada componente es independiente")
    
    print("\n=== FLUJO SIMPLIFICADO ===")
    print("1. ModelBuilder → JSON con configuración completa")
    print("2. AnalysisEngine → Lee JSON y ejecuta análisis")
    print("3. Resultados → Incluyen configuración utilizada")
    print("4. Reportes → Basados en resultados completos")

if __name__ == "__main__":
    # Ejecutar estudio principal
    main()
    
    # Mostrar ejemplo de uso directo
    ejemplo_uso_directo()
    
    # Explicar ventajas
    mostrar_ventajas()
