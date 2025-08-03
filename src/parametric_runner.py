import os
import random
from typing import Dict, List

from .model_builder import ModelBuilder
from .analysis_engine import AnalysisEngine
from .report_generator import ReportGenerator
from .python_exporter import PythonExporter
from .utils.model_helpers import ModelBuilderHelpers

class ParametricRunner:
    """
    Orquesta estudios paramétricos completos.
    
    Arquitectura simplificada:
    - ModelBuilder: Genera modelos JSON con toda la configuración embebida
    - AnalysisEngine: Ejecutor puro que lee configuración del JSON y ejecuta análisis  
    - ReportGenerator: Procesa resultados y genera reportes
    - PythonExporter: Exporta scripts usando configuración del JSON
    
    ¿Por qué AnalysisEngine sigue siendo necesario?
    - Alguien tiene que ejecutar los análisis en OpenSees
    - Maneja la interfaz con OpenSeesPy (no trivial)
    - Separa lógica de ejecución de lógica de orquestación
    """

    def __init__(self, model_builder: ModelBuilder, analysis_engine: AnalysisEngine,
                 report_generator: ReportGenerator, python_exporter: PythonExporter):
        """
        Inicializa el orquestador del estudio.
        
        Nota: AnalysisEngine es necesario como ejecutor, aunque toda su configuración
        viene ahora de los archivos JSON de modelo.
        """
        self.builder = model_builder
        self.engine = analysis_engine
        self.reporter = report_generator
        self.exporter = python_exporter
        
        # Crear helpers para métodos de conveniencia
        self.helpers = ModelBuilderHelpers(self.builder)

    def generate_parametric_models(self, L_B_ratios: List[float], B_values: List[float],
                                   nx_values: List[int], ny_values: List[int],
                                   analysis_distribution: Dict[str, float] = None) -> List[Dict]:
        """
        Genera archivos de modelo JSON para todas las combinaciones de parámetros
        con distribución controlada de tipos de análisis.
        
        Args:
            analysis_distribution: Diccionario con distribución de análisis
                                 Ej: {"static": 0.6, "modal": 0.2, "complete": 0.2}
        """
        if analysis_distribution is None:
            analysis_distribution = {"complete": 1.0}  # Por defecto, todos completos
        
        models_info = []
        print("--- Iniciando generación de modelos paramétricos ---")
        
        # Generar todas las combinaciones
        all_combinations = []
        for L_B_ratio in L_B_ratios:
            for B in B_values:
                for nx in nx_values:
                    for ny in ny_values:
                        all_combinations.append((L_B_ratio, B, nx, ny))
        
        total_models = len(all_combinations)
        print(f"Total de combinaciones: {total_models}")
        
        # Calcular distribución
        static_count = int(total_models * analysis_distribution.get("static", 0))
        modal_count = int(total_models * analysis_distribution.get("modal", 0))
        dynamic_count = int(total_models * analysis_distribution.get("dynamic", 0))
        complete_count = total_models - static_count - modal_count - dynamic_count
        
        print(f"Distribución de análisis:")
        print(f"- Solo estático: {static_count} modelos")
        print(f"- Solo modal: {modal_count} modelos")
        print(f"- Solo dinámico: {dynamic_count} modelos")
        print(f"- Completo: {complete_count} modelos")
        
        # Crear lista de tipos de análisis según la distribución
        analysis_types = []
        analysis_types.extend(['static'] * static_count)
        analysis_types.extend(['modal'] * modal_count)
        analysis_types.extend(['dynamic'] * dynamic_count)
        analysis_types.extend(['complete'] * complete_count)
        
        # MEZCLAR ALEATORIAMENTE para distribución uniforme
        random.shuffle(analysis_types)
        
        print(f"Orden de análisis mezclado aleatoriamente...")
        
        # Generar modelos según el orden aleatorio
        for i, (L_B_ratio, B, nx, ny) in enumerate(all_combinations):
            analysis_type = analysis_types[i]
            try:
                if analysis_type == 'static':
                    model_info = self.helpers.create_static_only_model(L_B_ratio, B, nx, ny)
                elif analysis_type == 'modal':
                    model_info = self.helpers.create_modal_only_model(L_B_ratio, B, nx, ny)
                elif analysis_type == 'dynamic':
                    model_info = self.helpers.create_dynamic_model(L_B_ratio, B, nx, ny)
                else:  # complete
                    model_info = self.helpers.create_complete_model(L_B_ratio, B, nx, ny)
                
                models_info.append(model_info)
                print(f"{analysis_type.capitalize()} {i+1}/{total_models}: {model_info['name']}")
                
            except Exception as e:
                print(f"Error creando modelo {analysis_type} {i}: {e}")
        
        print(f"\nTotal de {len(models_info)} modelos generados en '{self.builder.output_dir}'.")
        return models_info
    
    def generate_parametric_models_by_criteria(self, L_B_ratios: List[float], B_values: List[float],
                                             nx_values: List[int], ny_values: List[int],
                                             analysis_criteria: Dict = None) -> List[Dict]:
        """
        Genera modelos con criterios específicos para la selección de análisis.
        
        Args:
            analysis_criteria: Diccionario con criterios de selección
                             Ej: {
                                 "static": {"L_B_ratio": [1.0, 1.5], "nx": [3, 4]},
                                 "modal": {"B": [10.0, 12.0]},
                                 "complete": {"nx": [5], "ny": [5]}
                             }
        """
        if analysis_criteria is None:
            # Criterios por defecto basados en complejidad computacional
            analysis_criteria = {
                "static": {"nx": [3, 4], "ny": [3, 4]},  # Modelos pequeños/medianos
                "modal": {"nx": [4, 5], "ny": [4, 5], "L_B_ratio": [1.5, 2.0]},  # Casos específicos
                "complete": {"nx": [5], "ny": [5]}  # Solo modelos grandes
            }
        
        models_info = []
        print("--- Generando modelos con criterios específicos ---")
        
        for L_B_ratio in L_B_ratios:
            for B in B_values:
                for nx in nx_values:
                    for ny in ny_values:
                        # Determinar tipo de análisis basado en criterios
                        analysis_type = self._determine_analysis_type(
                            L_B_ratio, B, nx, ny, analysis_criteria
                        )
                        
                        try:
                            if analysis_type == 'static':
                                model_info = self.helpers.create_static_only_model(L_B_ratio, B, nx, ny)
                            elif analysis_type == 'modal':
                                model_info = self.helpers.create_modal_only_model(L_B_ratio, B, nx, ny)
                            elif analysis_type == 'dynamic':
                                model_info = self.helpers.create_dynamic_model(L_B_ratio, B, nx, ny)
                            else:  # complete
                                model_info = self.helpers.create_complete_model(L_B_ratio, B, nx, ny)
                            
                            models_info.append(model_info)
                            print(f"{analysis_type.capitalize()}: {model_info['name']}")
                            
                        except Exception as e:
                            print(f"Error creando modelo: {e}")
        
        print(f"\nTotal de {len(models_info)} modelos generados con criterios.")
        return models_info
    
    def _determine_analysis_type(self, L_B_ratio: float, B: float, nx: int, ny: int, 
                               criteria: Dict) -> str:
        """
        Determina el tipo de análisis basado en los criterios dados.
        """
        params = {"L_B_ratio": L_B_ratio, "B": B, "nx": nx, "ny": ny}
        
        # Verificar cada tipo de análisis en orden de prioridad
        for analysis_type in ['complete', 'dynamic', 'modal', 'static']:
            if analysis_type in criteria:
                type_criteria = criteria[analysis_type]
                matches_all = True
                
                for param_name, param_values in type_criteria.items():
                    if param_name in params:
                        if params[param_name] not in param_values:
                            matches_all = False
                            break
                
                if matches_all:
                    return analysis_type
        
        # Si no coincide con ningún criterio, usar estático por defecto
        return 'static'

    def run_full_study(self, L_B_ratios: List[float], B_values: List[float],
                       nx_values: List[int], ny_values: List[int],
                       selection_method: str = "distribution",
                       analysis_distribution: Dict[str, float] = None,
                       analysis_criteria: Dict = None,
                       export_python: bool = False, separate_files: bool = False):
        """
        Ejecuta un estudio paramétrico completo con control flexible de tipos de análisis.
        
        Args:
            selection_method: Método de selección ("distribution" o "criteria")
            analysis_distribution: Distribución de tipos para método "distribution"
                                 Ej: {"static": 0.6, "modal": 0.2, "complete": 0.2}
            analysis_criteria: Criterios para método "criteria"
                             Ej: {"static": {"nx": [3, 4]}, "modal": {"L_B_ratio": [1.5, 2.0]}}
        """
        # 1. Generar modelos según el método elegido
        if selection_method == "criteria":
            print("Usando método de selección por CRITERIOS")
            models_info = self.generate_parametric_models_by_criteria(
                L_B_ratios, B_values, nx_values, ny_values, analysis_criteria
            )
        elif selection_method == "distribution":
            print("Usando método de selección por DISTRIBUCIÓN ALEATORIA")
            models_info = self.generate_parametric_models(
                L_B_ratios, B_values, nx_values, ny_values, analysis_distribution
            )
        else:
            raise ValueError(f"Método de selección '{selection_method}' no válido. Use 'distribution' o 'criteria'")
        
        if not models_info:
            print("No se generaron modelos. Abortando estudio.")
            return

        # 2. Opcional: Exportar a Python
        if export_python:
            print("\n--- Exportando modelos a scripts de Python ---")
            for model_info in models_info:
                self.exporter.export_script(model_info, separate_files=separate_files)
            print("Exportación a Python completada.")

        # 3. Analizar modelos (el AnalysisEngine respeta enabled_analyses automáticamente)
        print("\n--- Iniciando análisis de modelos ---")
        model_files = [info['file_path'] for info in models_info]
        analysis_results = self.engine.analyze_multiple_models(model_files)

        # 4. Generar reporte
        print("\n--- Generando reporte completo ---")
        report = self.reporter.generate_comprehensive_report(analysis_results)
        print(f"\nEstudio completado. Reporte guardado en: {report['html_report']}")
        
        return {
            'selection_method': selection_method,
            'models_generated': len(models_info),
            'analysis_results': analysis_results,
            'report': report
        }
    
    def run_full_study_hybrid(self, L_B_ratios: List[float], B_values: List[float],
                             nx_values: List[int], ny_values: List[int],
                             criteria_distribution: Dict[str, float] = None,
                             analysis_criteria: Dict = None,
                             export_python: bool = False, separate_files: bool = False):
        """
        Ejecuta un estudio híbrido: criterios + distribución aleatoria dentro de cada criterio.
        
        Args:
            criteria_distribution: Distribución de modelos por criterio
                                 Ej: {"criteria": 0.6, "random": 0.4}
            analysis_criteria: Criterios específicos para la parte dirigida
        """
        print("Usando método HÍBRIDO (criterios + distribución aleatoria)")
        
        if criteria_distribution is None:
            criteria_distribution = {"criteria": 0.7, "random": 0.3}
        
        if analysis_criteria is None:
            # Criterios por defecto inteligentes
            analysis_criteria = {
                "complete": {"nx": [5], "ny": [5]},  # Modelos complejos
                "modal": {"L_B_ratio": [1.75, 2.0]},  # Estructuras alargadas
                "dynamic": {"B": [12.0, 14.0]},  # Estructuras grandes
                "static": {"nx": [3, 4], "ny": [3, 4]}  # Resto
            }
        
        # Generar todas las combinaciones
        all_combinations = []
        for L_B_ratio in L_B_ratios:
            for B in B_values:
                for nx in nx_values:
                    for ny in ny_values:
                        all_combinations.append((L_B_ratio, B, nx, ny))
        
        total_models = len(all_combinations)
        criteria_count = int(total_models * criteria_distribution.get("criteria", 0.7))
        random_count = total_models - criteria_count
        
        print(f"Total de combinaciones: {total_models}")
        print(f"- Modelos por criterios: {criteria_count}")
        print(f"- Modelos aleatorios: {random_count}")
        
        models_info = []
        
        # 1. Generar modelos por criterios (primeros N)
        print("\n--- Generando modelos por criterios ---")
        for i in range(criteria_count):
            L_B_ratio, B, nx, ny = all_combinations[i]
            analysis_type = self._determine_analysis_type(L_B_ratio, B, nx, ny, analysis_criteria)
            
            try:
                model_info = self._create_model_by_type(analysis_type, L_B_ratio, B, nx, ny)
                models_info.append(model_info)
                print(f"Criterio {analysis_type} {i+1}/{criteria_count}: {model_info['name']}")
            except Exception as e:
                print(f"Error creando modelo por criterio {i}: {e}")
        
        # 2. Generar modelos aleatorios (restantes)
        if random_count > 0:
            print("\n--- Generando modelos con distribución aleatoria ---")
            remaining_combinations = all_combinations[criteria_count:]
            
            # Distribución por defecto para la parte aleatoria
            random_distribution = {"static": 0.5, "modal": 0.3, "complete": 0.2}
            
            # Crear tipos aleatorios
            static_count = int(random_count * random_distribution.get("static", 0))
            modal_count = int(random_count * random_distribution.get("modal", 0))
            complete_count = random_count - static_count - modal_count
            
            analysis_types = []
            analysis_types.extend(['static'] * static_count)
            analysis_types.extend(['modal'] * modal_count)
            analysis_types.extend(['complete'] * complete_count)
            random.shuffle(analysis_types)
            
            for i, (L_B_ratio, B, nx, ny) in enumerate(remaining_combinations):
                analysis_type = analysis_types[i] if i < len(analysis_types) else 'static'
                
                try:
                    model_info = self._create_model_by_type(analysis_type, L_B_ratio, B, nx, ny)
                    models_info.append(model_info)
                    print(f"Aleatorio {analysis_type} {i+1}/{random_count}: {model_info['name']}")
                except Exception as e:
                    print(f"Error creando modelo aleatorio {i}: {e}")
        
        # Continuar con exportación y análisis como en run_full_study...
        print(f"\nTotal de {len(models_info)} modelos generados (híbrido).")
        
        # Análisis y reporte
        if export_python:
            print("\n--- Exportando modelos a scripts de Python ---")
            for model_info in models_info:
                self.exporter.export_script(model_info, separate_files=separate_files)
            print("Exportación a Python completada.")

        print("\n--- Iniciando análisis de modelos ---")
        model_files = [info['file_path'] for info in models_info]
        analysis_results = self.engine.analyze_multiple_models(model_files)

        print("\n--- Generando reporte completo ---")
        report = self.reporter.generate_comprehensive_report(analysis_results)
        print(f"\nEstudio completado. Reporte guardado en: {report['html_report']}")
        
        return {
            'selection_method': 'hybrid',
            'criteria_models': criteria_count,
            'random_models': random_count,
            'models_generated': len(models_info),
            'analysis_results': analysis_results,
            'report': report
        }
    
    def _create_model_by_type(self, analysis_type: str, L_B_ratio: float, B: float, nx: int, ny: int):
        """Método auxiliar para crear modelo según el tipo de análisis usando helpers."""
        if analysis_type == 'static':
            return self.helpers.create_static_only_model(L_B_ratio, B, nx, ny)
        elif analysis_type == 'modal':
            return self.helpers.create_modal_only_model(L_B_ratio, B, nx, ny)
        elif analysis_type == 'dynamic':
            return self.helpers.create_dynamic_model(L_B_ratio, B, nx, ny)
        else:  # complete
            return self.helpers.create_complete_model(L_B_ratio, B, nx, ny)
    
    # Métodos de compatibilidad con tests existentes
    def generate_parameter_combinations(self, parameters: Dict) -> List[Dict]:
        """
        Genera todas las combinaciones posibles de parámetros.
        
        Args:
            parameters: Diccionario con listas de valores para cada parámetro
            
        Returns:
            Lista de diccionarios con combinaciones de parámetros
        """
        import itertools
        
        # Extraer nombres y valores de parámetros
        param_names = list(parameters.keys())
        param_values = list(parameters.values())
        
        # Generar combinaciones cartesianas
        combinations = []
        for combo in itertools.product(*param_values):
            combinations.append(dict(zip(param_names, combo)))
            
        return combinations
    
    def create_model_name(self, params: Dict, prefix: str = "model") -> str:
        """
        Crea nombre de modelo basado en parámetros.
        
        Args:
            params: Diccionario de parámetros
            prefix: Prefijo para el nombre
            
        Returns:
            Nombre del modelo
        """
        # Crear nombre basado en parámetros clave
        param_str = "_".join([
            str(params.get('L_B_ratio', '')).replace('.', '_'),
            str(params.get('B', '')).replace('.', '_'),
            str(params.get('nx', '')),
            str(params.get('ny', ''))
        ])
        return f"{prefix}_{param_str}"
    
    def run_single_model(self, params: Dict) -> Dict:
        """
        Ejecuta análisis de un modelo individual.
        
        Args:
            params: Parámetros del modelo
            
        Returns:
            Resultados del análisis
        """
        try:
            # Crear modelo
            model_name = self.create_model_name(params)
            model = self.builder.create_model(
                params['L_B_ratio'],
                params['B'],
                params['nx'],
                params['ny'],
                model_name
            )
            
            # Ejecutar análisis
            if model['success']:
                results = self.engine.analyze_model(model['file_path'])
                return {
                    'model_name': model_name,
                    'success': True,
                    'results': results
                }
            else:
                return {
                    'model_name': model_name,
                    'success': False,
                    'error': 'Model creation failed'
                }
                
        except Exception as e:
            return {
                'model_name': params.get('model_name', 'unknown'),
                'success': False,
                'error': str(e)
            }
    
    def run_parametric_study(self, parameters: Dict, max_models: int = None) -> Dict:
        """
        Ejecuta estudio paramétrico completo.
        
        Args:
            parameters: Diccionario de parámetros
            max_models: Máximo número de modelos a procesar
            
        Returns:
            Resumen del estudio
        """
        combinations = self.generate_parameter_combinations(parameters)
        
        if max_models:
            combinations = combinations[:max_models]
        
        results = []
        successful = 0
        
        for combo in combinations:
            result = self.run_single_model(combo)
            results.append(result)
            if result['success']:
                successful += 1
        
        return {
            'total_models': len(combinations),
            'successful_models': successful,
            'success_rate': successful / len(combinations) if combinations else 0,
            'results': results
        }
    
    def create_results_dataframe(self, results_data: List[Dict]):
        """
        Crea DataFrame de pandas con resultados.
        
        Args:
            results_data: Lista de resultados
            
        Returns:
            DataFrame con resultados
        """
        try:
            import pandas as pd
            return pd.DataFrame(results_data)
        except ImportError:
            print("Warning: pandas not available")
            return None
    
    def save_results_summary(self, summary: Dict, study_name: str) -> str:
        """
        Guarda resumen de resultados.
        
        Args:
            summary: Resumen del estudio
            study_name: Nombre del estudio
            
        Returns:
            Ruta del archivo guardado
        """
        import json
        
        file_path = f"results/{study_name}_summary.json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(summary, f, indent=2)
            
        return file_path
    
    def save_results_dataframe(self, df, study_name: str) -> str:
        """
        Guarda DataFrame como CSV.
        
        Args:
            df: DataFrame a guardar
            study_name: Nombre del estudio
            
        Returns:
            Ruta del archivo guardado
        """
        file_path = f"results/{study_name}_results.csv"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if df is not None:
            df.to_csv(file_path, index=False)
            
        return file_path
    
    def filter_successful_results(self, results_data: List[Dict]) -> List[Dict]:
        """
        Filtra solo resultados exitosos.
        
        Args:
            results_data: Lista de resultados
            
        Returns:
            Lista filtrada de resultados exitosos
        """
        return [r for r in results_data if r.get('success', False)]
    
    def calculate_study_statistics(self, results_data: List[Dict]) -> Dict:
        """
        Calcula estadísticas del estudio.
        
        Args:
            results_data: Lista de resultados
            
        Returns:
            Diccionario con estadísticas
        """
        total = len(results_data)
        successful = len(self.filter_successful_results(results_data))
        
        return {
            'total_models': total,
            'successful_models': successful,
            'failed_models': total - successful,
            'success_rate': successful / total if total > 0 else 0
        }
