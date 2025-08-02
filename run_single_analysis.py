import os
from src.model_builder import ModelBuilder
from src.analysis_engine import AnalysisEngine

def main():
    """
    Ejecuta el análisis para el modelo específico creado por 'create_model.py'
    y muestra un resumen de los resultados.
    """
    # --- 1. Definir los parámetros del modelo a analizar ---
    # Estos deben coincidir con los usados en create_model.py para encontrar el archivo.
    L_B_ratio = 1.5
    B = 10.0
    nx = 4
    ny = 4

    # --- 2. Generar el nombre del modelo para encontrar el archivo ---
    # Usamos ModelBuilder para asegurar que el nombre es consistente.
    # Asumimos que los modelos están en el directorio por defecto "models".
    builder = ModelBuilder(output_dir="models")
    model_name = builder.generate_model_name(L_B_ratio, B, nx, ny)
    model_file = os.path.join(builder.output_dir, f"{model_name}.json")

    # Verificar si el modelo existe. Si no, sugerir ejecutar create_model.py
    if not os.path.exists(model_file):
        print(f"Error: El archivo del modelo '{model_file}' no fue encontrado.")
        print("Por favor, ejecute 'create_model.py' primero para generar el modelo.")
        return

    print(f"Iniciando análisis para el modelo: {model_name}")
    print(f"Archivo de modelo: {model_file}")

    # --- 3. Inicializar y ejecutar el motor de análisis ---
    # Asumimos que los resultados se guardan en el directorio por defecto "results".
    engine = AnalysisEngine(models_dir="models", results_dir="results")
    
    # El tag ODB que se usará dentro de analyze_model
    odb_tag_for_viz = 1
    # Analizar el modelo (estático y modal). Los resultados se guardan en un JSON.
    analysis_results = engine.analyze_model(model_file, odb_tag=odb_tag_for_viz)

    # --- 4. Mostrar un resumen de los resultados ---
    if analysis_results:
        print("\n--- Resumen del Análisis ---")
        
        # Resultados estáticos
        static_analysis = analysis_results.get('static_analysis', {})
        static_success = static_analysis.get('success', False)
        print(f"\nAnálisis Estático Exitoso: {static_success}")
        if static_success:
            max_disp = static_analysis.get('max_displacement', 0.0)
            print(f"  - Desplazamiento Máximo: {max_disp:.4f} m")

        # Resultados modales
        modal_analysis = analysis_results.get('modal_analysis', {})
        modal_success = modal_analysis.get('success', False)
        print(f"\nAnálisis Modal Exitoso: {modal_success}")
        if modal_success:
            periods = modal_analysis.get('periods', [])
            print("  - Períodos (s):")
            for i, period in enumerate(periods[:5]): # Mostrar los primeros 5 modos
                print(f"    - Modo {i+1}: {period:.4f} s")

        # --- 5. Crear visualización del modelo deformado ---
        # Gracias a la refactorización, el estado de OpenSees y el ODB
        # siguen disponibles después de llamar a analyze_model().
        # Ya no es necesario volver a ejecutar el análisis.
        print("\nGenerando visualización del modelo deformado...")
        if static_success:
            html_file = engine.create_visualization(analysis_results, odb_tag=odb_tag_for_viz)
            if html_file:
                print(f"Visualización guardada en: {html_file}")
                print(f"Puede abrir este archivo en su navegador.")
        else:
            print("No se pudo crear la visualización porque el análisis estático falló.")

        print("\nAnálisis completado.")
        results_file = os.path.join(engine.results_dir, f"{model_name}_results.json")
        print(f"Resultados completos guardados en: {results_file}")
    else:
        print("El análisis no pudo ser completado.")

if __name__ == '__main__':
    main()