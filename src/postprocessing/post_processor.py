"""
PostProcessor - Orchestrador de postprocesamiento.
Separa análisis numérico de visualización/reportes.

Responsabilidad: Procesar resultados numéricos para generar visualizaciones/reportes.
"""

import os
from typing import List, Optional, Dict, Any
from ..domain.analysis_results import AnalysisResults
from ..domain.structural_model import StructuralModel


class PostProcessor:
    """
    Orchestrador de postprocesamiento.
    Responsabilidad: Procesar resultados numéricos para generar visualizaciones/reportes.
    """
    
    def __init__(self, output_dir: str = "results"):
        """
        Inicializa el postprocesador.
        
        Args:
            output_dir: Directorio de salida
        """
        self.output_dir = output_dir
        self.ensure_output_dir()
        
        # Importar componentes especializados cuando estén disponibles
        self.opstool_pipeline = None
        self.report_generator = None
        self.data_exporter = None
        
        # Inicializar componentes disponibles
        self._initialize_components()
    
    def ensure_output_dir(self):
        """Asegura que el directorio de salida existe."""
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _initialize_components(self):
        """Inicializa componentes de postprocesamiento disponibles."""
        try:
            from .opstool_pipeline import OpstoolPipeline
            self.opstool_pipeline = OpstoolPipeline(self.output_dir)
        except ImportError:
            print("⚠️ OpstoolPipeline no disponible")
        
        try:
            from .report_generator import ReportGenerator
            self.report_generator = ReportGenerator(self.output_dir)
        except ImportError:
            print("⚠️ ReportGenerator no disponible")
        
        try:
            from .data_exporter import DataExporter
            self.data_exporter = DataExporter(self.output_dir)
        except ImportError:
            print("⚠️ DataExporter no disponible")
    
    def process_results(self, 
                       structural_model: StructuralModel,
                       analysis_results: AnalysisResults,
                       config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa resultados de análisis para generar postprocesamiento.
        
        Args:
            structural_model: Modelo estructural original
            analysis_results: Resultados del análisis
            config: Configuración de postprocesamiento
            
        Returns:
            Diccionario con archivos generados
        """
        if not analysis_results.success:
            print(f"❌ Análisis falló: {analysis_results.errors}")
            return {}
        
        config = config or {}
        generated_files = {}
        
        print(f"🎨 Iniciando postprocesamiento: {analysis_results.model_name}")
        
        # 1. Visualizaciones con opstool (si está habilitado)
        if config.get('enable_visualizations', True) and self.opstool_pipeline:
            try:
                print("📊 Generando visualizaciones...")
                viz_files = self.opstool_pipeline.generate_visualizations(
                    structural_model, 
                    analysis_results, 
                    config.get('visualization_config', {})
                )
                generated_files['visualizations'] = viz_files
                print(f"   ✅ {len(viz_files)} archivos de visualización generados")
            except Exception as e:
                print(f"   ❌ Error en visualizaciones: {e}")
                generated_files['visualization_errors'] = [str(e)]
        
        # 2. Reportes (si está habilitado)
        if config.get('enable_reports', True) and self.report_generator:
            try:
                print("📋 Generando reportes...")
                report_files = self.report_generator.generate_reports(
                    analysis_results,
                    config.get('report_config', {})
                )
                generated_files['reports'] = report_files
                print(f"   ✅ {len(report_files)} reportes generados")
            except Exception as e:
                print(f"   ❌ Error en reportes: {e}")
                generated_files['report_errors'] = [str(e)]
        
        # 3. Exportación de datos (si está habilitado)
        if config.get('enable_data_export', True) and self.data_exporter:
            try:
                print("💾 Exportando datos...")
                export_files = self.data_exporter.export_data(
                    analysis_results,
                    config.get('export_config', {})
                )
                generated_files['exports'] = export_files
                print(f"   ✅ {len(export_files)} archivos de datos exportados")
            except Exception as e:
                print(f"   ❌ Error en exportación: {e}")
                generated_files['export_errors'] = [str(e)]
        
        # 4. Crear índice de archivos generados
        if generated_files:
            index_file = self._create_index_file(analysis_results.model_name, generated_files)
            generated_files['index'] = index_file
        
        print(f"🎉 Postprocesamiento completado para {analysis_results.model_name}")
        return generated_files
    
    def process_multiple_results(self, 
                                results_list: List[tuple],
                                config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa múltiples resultados de análisis.
        
        Args:
            results_list: Lista de tuplas (structural_model, analysis_results)
            config: Configuración de postprocesamiento
            
        Returns:
            Diccionario con todos los archivos generados
        """
        config = config or {}
        all_generated_files = {}
        
        print(f"🔄 Procesando {len(results_list)} conjuntos de resultados...")
        
        for i, (structural_model, analysis_results) in enumerate(results_list, 1):
            print(f"\n📊 Procesando resultado {i}/{len(results_list)}: {analysis_results.model_name}")
            
            try:
                files = self.process_results(structural_model, analysis_results, config)
                all_generated_files[analysis_results.model_name] = files
            except Exception as e:
                print(f"   ❌ Error procesando {analysis_results.model_name}: {e}")
                all_generated_files[analysis_results.model_name] = {'error': str(e)}
        
        # Crear reporte consolidado para múltiples resultados
        if all_generated_files and config.get('create_consolidated_report', True):
            try:
                consolidated_file = self._create_consolidated_report(all_generated_files)
                all_generated_files['_consolidated_report'] = consolidated_file
            except Exception as e:
                print(f"   ⚠️ Error creando reporte consolidado: {e}")
        
        return all_generated_files
    
    def _create_index_file(self, model_name: str, generated_files: Dict[str, Any]) -> str:
        """Crea archivo índice con archivos generados."""
        import json
        from datetime import datetime
        
        index_data = {
            "model_name": model_name,
            "timestamp": datetime.now().isoformat(),
            "postprocessing_summary": {
                "total_categories": len([k for k in generated_files.keys() if not k.endswith('_errors')]),
                "total_files": sum(len(v) for k, v in generated_files.items() 
                                 if isinstance(v, list) and not k.endswith('_errors')),
                "errors": [k for k in generated_files.keys() if k.endswith('_errors')]
            },
            "generated_files": generated_files
        }
        
        index_file = os.path.join(self.output_dir, f"postprocessing_index_{model_name}.json")
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
        
        print(f"   📋 Índice creado: {os.path.basename(index_file)}")
        return index_file
    
    def _create_consolidated_report(self, all_files: Dict[str, Any]) -> str:
        """Crea reporte consolidado para múltiples modelos."""
        import json
        from datetime import datetime
        
        summary = {
            "consolidation_timestamp": datetime.now().isoformat(),
            "total_models": len([k for k in all_files.keys() if not k.startswith('_')]),
            "successful_models": len([k for k, v in all_files.items() 
                                    if not k.startswith('_') and 'error' not in v]),
            "failed_models": len([k for k, v in all_files.items() 
                                if not k.startswith('_') and 'error' in v]),
            "models_summary": {}
        }
        
        for model_name, files in all_files.items():
            if not model_name.startswith('_'):
                if 'error' in files:
                    summary["models_summary"][model_name] = {"status": "failed", "error": files['error']}
                else:
                    file_count = sum(len(v) for v in files.values() if isinstance(v, list))
                    summary["models_summary"][model_name] = {"status": "success", "files_generated": file_count}
        
        summary["detailed_files"] = all_files
        
        consolidated_file = os.path.join(self.output_dir, "consolidated_postprocessing_report.json")
        with open(consolidated_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Reporte consolidado creado: {os.path.basename(consolidated_file)}")
        return consolidated_file
    
    def get_available_components(self) -> Dict[str, bool]:
        """Retorna qué componentes están disponibles."""
        return {
            "opstool_pipeline": self.opstool_pipeline is not None,
            "report_generator": self.report_generator is not None,
            "data_exporter": self.data_exporter is not None
        }
    
    def create_simple_summary(self, 
                             structural_model: StructuralModel,
                             analysis_results: AnalysisResults) -> str:
        """
        Crea un resumen simple cuando no hay componentes especializados disponibles.
        
        Args:
            structural_model: Modelo estructural
            analysis_results: Resultados del análisis
            
        Returns:
            Ruta al archivo de resumen creado
        """
        import json
        from datetime import datetime
        
        summary = {
            "model_name": analysis_results.model_name,
            "timestamp": datetime.now().isoformat(),
            "analysis_success": analysis_results.success,
            "model_info": {
                "nodes": len(structural_model.geometry.nodes),
                "elements": len(structural_model.geometry.elements),
                "enabled_analyses": structural_model.analysis_config.enabled_analyses
            },
            "results": {}
        }
        
        if analysis_results.static_results:
            summary["results"]["static"] = {
                "max_displacement": analysis_results.static_results.max_displacement,
                "convergence": analysis_results.static_results.convergence_achieved,
                "analysis_time": analysis_results.static_results.analysis_time
            }
        
        if analysis_results.modal_results:
            summary["results"]["modal"] = {
                "num_modes": len(analysis_results.modal_results.periods),
                "first_period": analysis_results.modal_results.periods[0] if analysis_results.modal_results.periods else None,
                "analysis_time": analysis_results.modal_results.analysis_time
            }
        
        if analysis_results.errors:
            summary["errors"] = analysis_results.errors
        
        summary_file = os.path.join(self.output_dir, f"simple_summary_{analysis_results.model_name}.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"📝 Resumen simple creado: {os.path.basename(summary_file)}")
        return summary_file
