from src.model_builder import ModelBuilder
from src.analysis_engine import AnalysisEngine
from src.python_exporter import PythonExporter
from src.utils.model_helpers import ModelBuilderHelpers

def main():
    """
    Script de demostración para crear diferentes tipos de modelos.
    Para estudios completos, se debe usar ParametricRunner.
    """
    # 1. Inicializar los componentes necesarios
    builder = ModelBuilder(output_dir="models")
    helpers = ModelBuilderHelpers(builder)  # Crear helpers
    exporter = PythonExporter(output_dir="models")
    
    # --- Parámetros del modelo de prueba ---
    L_B_RATIO = 1.5  # Relación largo/ancho
    B_VALUE = 10.0   # Ancho en metros
    NX = 4           # Número de ejes en X
    NY = 4           # Número de ejes en Y
    # ------------------------------------

    # 2. Crear diferentes tipos de modelos
    print("--- Creando modelos de ejemplo ---")
    
    # Modelo completo (estático + modal) - COMPORTAMIENTO POR DEFECTO
    print("\n1. Modelo completo (estático + modal):")
    model_complete = builder.create_model(
        L_B_ratio=L_B_RATIO, B=B_VALUE, nx=NX, ny=NY, 
        model_name="ejemplo_completo"
    )
    print(f"   Creado: {model_complete['name']}")
    
    # Modelo solo estático (usando parámetros específicos)
    print("\n2. Modelo solo estático:")
    model_static = builder.create_model(
        L_B_ratio=L_B_RATIO, B=B_VALUE, nx=NX, ny=NY,
        model_name="ejemplo_estatico",
        enabled_analyses=['static'],
        analysis_params={'static': {'steps': 15}}  # Más pasos que por defecto
    )
    print(f"   Creado: {model_static['name']}")
    
    # Modelo solo modal (con más modos)
    print("\n3. Modelo solo modal:")
    model_modal = builder.create_model(
        L_B_ratio=L_B_RATIO, B=B_VALUE, nx=NX, ny=NY,
        model_name="ejemplo_modal",
        enabled_analyses=['modal'],
        analysis_params={'modal': {'num_modes': 10}}
    )
    print(f"   Creado: {model_modal['name']}")
    
    # Modelo dinámico (estático + dinámico)
    print("\n4. Modelo dinámico:")
    model_dynamic = builder.create_model(
        L_B_ratio=L_B_RATIO, B=B_VALUE, nx=NX, ny=NY,
        model_name="ejemplo_dinamico",
        enabled_analyses=['static', 'dynamic'],
        analysis_params={'dynamic': {'dt': 0.005, 'num_steps': 2000}}
    )
    print(f"   Creado: {model_dynamic['name']}")
    
    # Modelo con TODOS los análisis (el más completo)
    print("\n5. Modelo completo TOTAL (static + modal + dynamic):")
    model_all = builder.create_model(
        L_B_ratio=L_B_RATIO, B=B_VALUE, nx=NX, ny=NY,
        model_name="ejemplo_completo_total",
        enabled_analyses=['static', 'modal', 'dynamic'],
        analysis_params={
            'static': {'steps': 20},
            'modal': {'num_modes': 12},
            'dynamic': {'dt': 0.001, 'num_steps': 5000}
        }
    )
    print(f"   Creado: {model_all['name']}")
    
    # Modelo con visualización completa (para demostración)
    print("\n6. Modelo con visualización completa:")
    model_viz = builder.create_model(
        L_B_ratio=L_B_RATIO, B=B_VALUE, nx=NX, ny=NY,
        model_name="ejemplo_con_visualizacion",
        enabled_analyses=['static', 'modal'],
        analysis_params={
            'static': {'steps': 15},
            'modal': {'num_modes': 8},
            'visualization': {
                'enabled': True,
                'static_deformed': True,  # Deformada estática
                'modal_shapes': True,     # Formas modales
                'deform_scale': 150,
                'show_nodes': True
            }
        }
    )
    print(f"   Creado: {model_viz['name']} (con visualización habilitada)")
    
    # Modelo rápido (sin visualización)
    print("\n7. Modelo rápido (solo resultados numéricos):")
    model_fast = builder.create_model(
        L_B_ratio=L_B_RATIO, B=B_VALUE, nx=NX, ny=NY,
        model_name="ejemplo_rapido",
        enabled_analyses=['static', 'modal'],
        analysis_params={
            'static': {'steps': 5},
            'modal': {'num_modes': 3},
            'visualization': {'enabled': False}  # Sin visualización
        }
    )
    print(f"   Creado: {model_fast['name']} (análisis rápido)")
    
    # Usando métodos de conveniencia con visualización
    print("\n8. Métodos de conveniencia con visualización:")
    model_conv_viz = helpers.create_modal_only_model(
        L_B_ratio=L_B_RATIO, B=B_VALUE, nx=NX, ny=NY,
        model_name="ejemplo_modal_conveniente",
        num_modes=6, visualize=True
    )
    print(f"   Creado: {model_conv_viz['name']} (método de conveniencia)")

    # 3. Opcional: Exportar algunos modelos a Python
    print("\n--- Exportando modelos a Python ---")
    
    # Exportar modelo completo como archivo único
    print("Exportando modelo completo...")
    exporter.export_script(model_complete, separate_files=False)
    
    # Exportar modelo dinámico como archivos separados
    print("Exportando modelo dinámico...")
    exporter.export_script(model_dynamic, separate_files=True)
    
    print("\n¡Modelos creados y exportados exitosamente!")
    print(f"Archivos JSON en: {builder.output_dir}/")
    print(f"Scripts Python en: {exporter.output_dir}/")
    
    print("\n--- Resumen ---")
    print("Creados 8 modelos con diferentes configuraciones:")
    print("- ejemplo_completo: análisis estático + modal (por defecto)")
    print("- ejemplo_estatico: solo análisis estático (15 pasos)")
    print("- ejemplo_modal: solo análisis modal (10 modos)")
    print("- ejemplo_dinamico: análisis estático + dinámico")
    print("- ejemplo_completo_total: TODOS los análisis")
    print("- ejemplo_con_visualizacion: con visualización completa")
    print("- ejemplo_rapido: sin visualización (análisis rápido)")
    print("- ejemplo_modal_conveniente: método de conveniencia con viz")
    
    print("\n💡 Control de Visualización:")
    print("- visualization.enabled: true/false")
    print("- visualization.static_deformed: deformada estática")
    print("- visualization.modal_shapes: formas modales")
    print("- Para análisis rápidos: disabled visualization")
    print("- Para presentaciones: enabled complete visualization")

if __name__ == "__main__":
    main()
