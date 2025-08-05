"""
OpstoolPipeline - Pipeline especializado para opstool.
Maneja la secuencia específica que requiere opstool para generar visualizaciones.
"""

import os
from typing import Dict, List, Any, Optional
from ..domain.analysis_results import AnalysisResults
from ..domain.structural_model import StructuralModel

# Verificar si opstool está disponible
try:
    import opstool as opst
    import opstool.vis.plotly as opsvis
    OPSTOOL_AVAILABLE = True
except ImportError:
    OPSTOOL_AVAILABLE = False
    opst = None
    opsvis = None


class OpstoolPipeline:
    """
    Pipeline especializado para generatear visualizaciones con opstool.
    
    Responsabilidad: Ejecutar la secuencia específica que requiere opstool
    para capturar resultados paso a paso y generar visualizaciones.
    """
    
    def __init__(self, output_dir: str = "results"):
        """
        Inicializa el pipeline de opstool.
        
        Args:
            output_dir: Directorio de salida
        """
        self.output_dir = output_dir
        self.ensure_output_dir()
        
        if not OPSTOOL_AVAILABLE:
            print("⚠️ Opstool no está disponible. Visualizaciones limitadas.")
    
    def ensure_output_dir(self):
        """Asegura que el directorio de salida existe."""
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Crear subdirectorio para visualizaciones
        viz_dir = os.path.join(self.output_dir, "visualizations")
        os.makedirs(viz_dir, exist_ok=True)
    
    def generate_visualizations(self,
                              structural_model: StructuralModel,
                              analysis_results: AnalysisResults,
                              config: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Genera visualizaciones a partir del modelo y resultados.
        
        Args:
            structural_model: Modelo estructural original
            analysis_results: Resultados del análisis
            config: Configuración específica de visualización
            
        Returns:
            Lista de archivos generados
        """
        config = config or {}
        generated_files = []
        
        if not analysis_results.success:
            print("❌ No se pueden generar visualizaciones: análisis falló")
            return generated_files
        
        print(f"📊 Generando visualizaciones para {analysis_results.model_name}")
        
        if OPSTOOL_AVAILABLE:
            # Generar visualizaciones con opstool
            generated_files.extend(self._run_static_with_opstool(structural_model, analysis_results, config))
            generated_files.extend(self._run_modal_with_opstool(structural_model, analysis_results, config))
        else:
            # Generar visualizaciones alternativas sin opstool
            generated_files.extend(self._generate_simple_visualizations(structural_model, analysis_results, config))
        
        return generated_files
    
    def _run_static_with_opstool(self,
                                structural_model: StructuralModel,
                                analysis_results: AnalysisResults,
                                config: Dict[str, Any]) -> List[str]:
        """Genera visualizaciones estáticas con opstool."""
        generated_files = []
        
        if not analysis_results.static_results:
            return generated_files
        
        print("   🔧 Ejecutando pipeline estático con opstool...")
        
        try:
            # NOTA: El pipeline opstool requiere RE-EJECUTAR el análisis para capturar datos
            # Esto es normal y necesario para el funcionamiento de opstool
            
            # 1. Reconstruir modelo en OpenSees para opstool
            build_info = structural_model.build_opensees_model()
            
            if not build_info.get('model_built', False):
                print(f"   ❌ Error reconstruyendo modelo para opstool: {build_info.get('error', 'Desconocido')}")
                return generated_files
            
            # 2. Configurar captura de opstool
            viz_dir = os.path.join(self.output_dir, "visualizations")
            
            # 3. Ejecutar análisis con captura de opstool
            # (Aquí iría la implementación específica de opstool)
            # Por ahora, crear archivos placeholder
            
            static_viz_file = os.path.join(viz_dir, f"static_analysis_{analysis_results.model_name}.html")
            with open(static_viz_file, 'w', encoding='utf-8') as f:
                f.write(self._create_static_html_placeholder(analysis_results))
            
            generated_files.append(static_viz_file)
            print(f"   ✅ Visualización estática: {os.path.basename(static_viz_file)}")
            
        except Exception as e:
            print(f"   ❌ Error en pipeline estático opstool: {e}")
        
        return generated_files
    
    def _run_modal_with_opstool(self,
                               structural_model: StructuralModel,
                               analysis_results: AnalysisResults,
                               config: Dict[str, Any]) -> List[str]:
        """Genera visualizaciones modales con opstool."""
        generated_files = []
        
        if not analysis_results.modal_results:
            return generated_files
        
        print("   🎵 Ejecutando pipeline modal con opstool...")
        
        try:
            viz_dir = os.path.join(self.output_dir, "visualizations")
            
            # Crear visualización de modos
            modal_viz_file = os.path.join(viz_dir, f"modal_analysis_{analysis_results.model_name}.html")
            with open(modal_viz_file, 'w', encoding='utf-8') as f:
                f.write(self._create_modal_html_placeholder(analysis_results))
            
            generated_files.append(modal_viz_file)
            print(f"   ✅ Visualización modal: {os.path.basename(modal_viz_file)}")
            
        except Exception as e:
            print(f"   ❌ Error en pipeline modal opstool: {e}")
        
        return generated_files
    
    def _generate_simple_visualizations(self,
                                       structural_model: StructuralModel,
                                       analysis_results: AnalysisResults,
                                       config: Dict[str, Any]) -> List[str]:
        """Genera visualizaciones simples sin opstool."""
        generated_files = []
        
        print("   📊 Generando visualizaciones simples (sin opstool)...")
        
        try:
            viz_dir = os.path.join(self.output_dir, "visualizations")
            
            # Crear resumen visual simple
            summary_file = os.path.join(viz_dir, f"summary_{analysis_results.model_name}.html")
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(self._create_summary_html(structural_model, analysis_results))
            
            generated_files.append(summary_file)
            print(f"   ✅ Resumen visual: {os.path.basename(summary_file)}")
            
        except Exception as e:
            print(f"   ❌ Error en visualizaciones simples: {e}")
        
        return generated_files
    
    def _create_static_html_placeholder(self, analysis_results: AnalysisResults) -> str:
        """Crea HTML placeholder para análisis estático."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Análisis Estático - {analysis_results.model_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 10px; border-radius: 5px; }}
                .result {{ margin: 10px 0; padding: 10px; border-left: 3px solid #007acc; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Análisis Estático</h1>
                <p>Modelo: {analysis_results.model_name}</p>
                <p>Timestamp: {analysis_results.timestamp}</p>
            </div>
            
            <div class="result">
                <h2>Resultados Estáticos</h2>
                <p><strong>Desplazamiento máximo:</strong> {analysis_results.static_results.max_displacement:.6f} m</p>
                <p><strong>Convergencia:</strong> {'Lograda' if analysis_results.static_results.convergence_achieved else 'No lograda'}</p>
                <p><strong>Iteraciones:</strong> {analysis_results.static_results.num_iterations}</p>
                <p><strong>Tiempo de análisis:</strong> {analysis_results.static_results.analysis_time:.3f} s</p>
            </div>
            
            <div class="result">
                <h3>Nota sobre Visualizaciones</h3>
                <p>Las visualizaciones completas con opstool requieren una configuración adicional.</p>
                <p>Este es un placeholder que muestra los resultados numéricos básicos.</p>
            </div>
        </body>
        </html>
        """
    
    def _create_modal_html_placeholder(self, analysis_results: AnalysisResults) -> str:
        """Crea HTML placeholder para análisis modal."""
        periods_str = ", ".join(f"{p:.3f}" for p in analysis_results.modal_results.periods[:5])
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Análisis Modal - {analysis_results.model_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 10px; border-radius: 5px; }}
                .result {{ margin: 10px 0; padding: 10px; border-left: 3px solid #007acc; }}
                .periods {{ background-color: #f9f9f9; padding: 10px; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Análisis Modal</h1>
                <p>Modelo: {analysis_results.model_name}</p>
                <p>Timestamp: {analysis_results.timestamp}</p>
            </div>
            
            <div class="result">
                <h2>Resultados Modales</h2>
                <p><strong>Número de modos:</strong> {len(analysis_results.modal_results.periods)}</p>
                <p><strong>Tiempo de análisis:</strong> {analysis_results.modal_results.analysis_time:.3f} s</p>
                
                <div class="periods">
                    <h3>Períodos (primeros 5 modos)</h3>
                    <p>{periods_str} segundos</p>
                </div>
            </div>
            
            <div class="result">
                <h3>Nota sobre Visualizaciones</h3>
                <p>Las visualizaciones de formas modales requieren opstool configurado.</p>
                <p>Este placeholder muestra los períodos calculados.</p>
            </div>
        </body>
        </html>
        """
    
    def _create_summary_html(self, structural_model: StructuralModel, analysis_results: AnalysisResults) -> str:
        """Crea HTML de resumen general."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Resumen de Análisis - {analysis_results.model_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #e8f5e8; padding: 15px; border-radius: 5px; }}
                .section {{ margin: 15px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
                .success {{ color: green; }}
                .error {{ color: red; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Resumen de Análisis Estructural</h1>
                <p>Modelo: {analysis_results.model_name}</p>
                <p>Estado: <span class="{'success' if analysis_results.success else 'error'}">
                    {'Exitoso' if analysis_results.success else 'Falló'}
                </span></p>
            </div>
            
            <div class="section">
                <h2>Información del Modelo</h2>
                <p><strong>Nodos:</strong> {len(structural_model.geometry.nodes)}</p>
                <p><strong>Elementos:</strong> {len(structural_model.geometry.elements)}</p>
                <p><strong>Análisis habilitados:</strong> {', '.join(structural_model.analysis_config.enabled_analyses)}</p>
            </div>
            
            {self._get_results_html_section(analysis_results)}
            
            <div class="section">
                <h2>Información Técnica</h2>
                <p><strong>Tiempo total:</strong> {analysis_results.total_analysis_time:.3f} s</p>
                <p><strong>Timestamp:</strong> {analysis_results.timestamp}</p>
            </div>
        </body>
        </html>
        """
    
    def _get_results_html_section(self, analysis_results: AnalysisResults) -> str:
        """Genera sección HTML con resultados."""
        if not analysis_results.success:
            return f"""
            <div class="section">
                <h2>Errores</h2>
                <ul>
                    {''.join(f'<li class="error">{error}</li>' for error in analysis_results.errors)}
                </ul>
            </div>
            """
        
        html = '<div class="section"><h2>Resultados</h2>'
        
        if analysis_results.static_results:
            html += f"""
            <h3>Análisis Estático</h3>
            <p><strong>Desplazamiento máximo:</strong> {analysis_results.static_results.max_displacement:.6f} m</p>
            <p><strong>Convergencia:</strong> {'Lograda' if analysis_results.static_results.convergence_achieved else 'No lograda'}</p>
            """
        
        if analysis_results.modal_results:
            html += f"""
            <h3>Análisis Modal</h3>
            <p><strong>Número de modos:</strong> {len(analysis_results.modal_results.periods)}</p>
            <p><strong>Primer período:</strong> {analysis_results.modal_results.periods[0]:.3f} s</p>
            """
        
        html += '</div>'
        return html
