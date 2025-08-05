"""
ReportGenerator - Generador de reportes PDF/HTML a partir de resultados numéricos.
"""

import os
import json
from typing import List, Dict, Any
from datetime import datetime
from ..domain.analysis_results import AnalysisResults


class ReportGenerator:
    """Genera reportes a partir de resultados de análisis."""
    
    def __init__(self, output_dir: str):
        """
        Inicializa el generador de reportes.
        
        Args:
            output_dir: Directorio de salida
        """
        self.output_dir = output_dir
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Asegura que el directorio de salida existe."""
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Crear subdirectorio para reportes
        reports_dir = os.path.join(self.output_dir, "reports")
        os.makedirs(reports_dir, exist_ok=True)
    
    def generate_reports(self, 
                        analysis_results: AnalysisResults,
                        config: Dict[str, Any] = None) -> List[str]:
        """
        Genera reportes a partir de resultados de análisis.
        
        Args:
            analysis_results: Resultados del análisis
            config: Configuración de reportes
            
        Returns:
            Lista de archivos de reportes generados
        """
        config = config or {}
        generated_files = []
        
        print(f"📋 Generando reportes para {analysis_results.model_name}")
        
        # 1. Reporte HTML detallado
        if config.get('generate_html', True):
            html_file = self._generate_html_report(analysis_results, config)
            if html_file:
                generated_files.append(html_file)
        
        # 2. Reporte JSON estructurado
        if config.get('generate_json', True):
            json_file = self._generate_json_report(analysis_results, config)
            if json_file:
                generated_files.append(json_file)
        
        # 3. Reporte de texto simple
        if config.get('generate_text', True):
            text_file = self._generate_text_report(analysis_results, config)
            if text_file:
                generated_files.append(text_file)
        
        return generated_files
    
    def generate_consolidated_report(self,
                                   results_list: List[AnalysisResults],
                                   config: Dict[str, Any] = None) -> List[str]:
        """
        Genera reporte consolidado para múltiples análisis.
        
        Args:
            results_list: Lista de resultados de análisis
            config: Configuración de reportes
            
        Returns:
            Lista de archivos de reportes generados
        """
        config = config or {}
        generated_files = []
        
        print(f"📊 Generando reporte consolidado para {len(results_list)} modelos")
        
        # Reporte consolidado HTML
        html_file = self._generate_consolidated_html(results_list, config)
        if html_file:
            generated_files.append(html_file)
        
        # Reporte consolidado JSON
        json_file = self._generate_consolidated_json(results_list, config)
        if json_file:
            generated_files.append(json_file)
        
        return generated_files
    
    def _generate_html_report(self, analysis_results: AnalysisResults, config: Dict[str, Any]) -> str:
        """Genera reporte HTML detallado."""
        try:
            reports_dir = os.path.join(self.output_dir, "reports")
            html_file = os.path.join(reports_dir, f"report_{analysis_results.model_name}.html")
            
            html_content = self._create_detailed_html(analysis_results, config)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"   ✅ Reporte HTML: {os.path.basename(html_file)}")
            return html_file
            
        except Exception as e:
            print(f"   ❌ Error generando reporte HTML: {e}")
            return None
    
    def _generate_json_report(self, analysis_results: AnalysisResults, config: Dict[str, Any]) -> str:
        """Genera reporte JSON estructurado."""
        try:
            reports_dir = os.path.join(self.output_dir, "reports")
            json_file = os.path.join(reports_dir, f"report_{analysis_results.model_name}.json")
            
            report_data = self._create_structured_report_data(analysis_results, config)
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Reporte JSON: {os.path.basename(json_file)}")
            return json_file
            
        except Exception as e:
            print(f"   ❌ Error generando reporte JSON: {e}")
            return None
    
    def _generate_text_report(self, analysis_results: AnalysisResults, config: Dict[str, Any]) -> str:
        """Genera reporte de texto simple."""
        try:
            reports_dir = os.path.join(self.output_dir, "reports")
            text_file = os.path.join(reports_dir, f"report_{analysis_results.model_name}.txt")
            
            text_content = self._create_text_report(analysis_results, config)
            
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(text_content)
            
            print(f"   ✅ Reporte TXT: {os.path.basename(text_file)}")
            return text_file
            
        except Exception as e:
            print(f"   ❌ Error generando reporte TXT: {e}")
            return None
    
    def _create_detailed_html(self, analysis_results: AnalysisResults, config: Dict[str, Any]) -> str:
        """Crea contenido HTML detallado."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Reporte de Análisis - {analysis_results.model_name}</title>
            <meta charset="utf-8">
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 0; 
                    padding: 20px; 
                    background-color: #f5f5f5; 
                }}
                .container {{ 
                    max-width: 1000px; 
                    margin: 0 auto; 
                    background-color: white; 
                    padding: 30px; 
                    border-radius: 8px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                }}
                .header {{ 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; 
                    padding: 20px; 
                    border-radius: 8px; 
                    margin-bottom: 30px; 
                }}
                .section {{ 
                    margin: 20px 0; 
                    padding: 20px; 
                    border: 1px solid #ddd; 
                    border-radius: 5px; 
                    background-color: #fafafa; 
                }}
                .success {{ color: #28a745; font-weight: bold; }}
                .error {{ color: #dc3545; font-weight: bold; }}
                .metric {{ 
                    display: inline-block; 
                    margin: 10px; 
                    padding: 15px; 
                    background-color: white; 
                    border-radius: 5px; 
                    border-left: 4px solid #007bff; 
                    min-width: 200px; 
                }}
                .metric-value {{ font-size: 1.5em; font-weight: bold; color: #007bff; }}
                .metric-label {{ color: #666; font-size: 0.9em; }}
                table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f8f9fa; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Reporte de Análisis Estructural</h1>
                    <h2>{analysis_results.model_name}</h2>
                    <p>Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>Estado del análisis: <span class="{'success' if analysis_results.success else 'error'}">
                        {'✅ Exitoso' if analysis_results.success else '❌ Falló'}
                    </span></p>
                </div>
                
                {self._get_summary_metrics_html(analysis_results)}
                
                {self._get_static_results_html(analysis_results)}
                
                {self._get_modal_results_html(analysis_results)}
                
                {self._get_technical_info_html(analysis_results)}
                
                {self._get_errors_html(analysis_results)}
            </div>
        </body>
        </html>
        """
    
    def _get_summary_metrics_html(self, analysis_results: AnalysisResults) -> str:
        """Genera sección de métricas resumen."""
        if not analysis_results.success:
            return ""
        
        metrics = []
        
        if analysis_results.static_results:
            metrics.append(f"""
            <div class="metric">
                <div class="metric-value">{analysis_results.static_results.max_displacement:.6f} m</div>
                <div class="metric-label">Desplazamiento Máximo</div>
            </div>
            """)
            
            metrics.append(f"""
            <div class="metric">
                <div class="metric-value">{'✅' if analysis_results.static_results.convergence_achieved else '❌'}</div>
                <div class="metric-label">Convergencia</div>
            </div>
            """)
        
        if analysis_results.modal_results and analysis_results.modal_results.periods:
            metrics.append(f"""
            <div class="metric">
                <div class="metric-value">{analysis_results.modal_results.periods[0]:.3f} s</div>
                <div class="metric-label">Primer Período</div>
            </div>
            """)
            
            metrics.append(f"""
            <div class="metric">
                <div class="metric-value">{len(analysis_results.modal_results.periods)}</div>
                <div class="metric-label">Modos Calculados</div>
            </div>
            """)
        
        metrics.append(f"""
        <div class="metric">
            <div class="metric-value">{analysis_results.total_analysis_time:.3f} s</div>
            <div class="metric-label">Tiempo Total</div>
        </div>
        """)
        
        return f"""
        <div class="section">
            <h2>📈 Métricas Principales</h2>
            {''.join(metrics)}
        </div>
        """
    
    def _get_static_results_html(self, analysis_results: AnalysisResults) -> str:
        """Genera sección de resultados estáticos."""
        if not analysis_results.static_results:
            return ""
        
        sr = analysis_results.static_results
        
        return f"""
        <div class="section">
            <h2>🔧 Análisis Estático</h2>
            <table>
                <tr><th>Parámetro</th><th>Valor</th></tr>
                <tr><td>Desplazamiento Máximo</td><td>{sr.max_displacement:.6f} m</td></tr>
                <tr><td>Esfuerzo Máximo</td><td>{sr.max_stress:.2f} MPa</td></tr>
                <tr><td>Convergencia Lograda</td><td>{'Sí' if sr.convergence_achieved else 'No'}</td></tr>
                <tr><td>Número de Iteraciones</td><td>{sr.num_iterations}</td></tr>
                <tr><td>Tiempo de Análisis</td><td>{sr.analysis_time:.3f} s</td></tr>
            </table>
        </div>
        """
    
    def _get_modal_results_html(self, analysis_results: AnalysisResults) -> str:
        """Genera sección de resultados modales."""
        if not analysis_results.modal_results:
            return ""
        
        mr = analysis_results.modal_results
        
        periods_table = ""
        for i, (period, freq) in enumerate(zip(mr.periods[:10], mr.frequencies[:10]), 1):
            periods_table += f"<tr><td>Modo {i}</td><td>{period:.4f} s</td><td>{freq:.2f} Hz</td></tr>"
        
        return f"""
        <div class="section">
            <h2>🎵 Análisis Modal</h2>
            <p><strong>Número total de modos:</strong> {len(mr.periods)}</p>
            <p><strong>Tiempo de análisis:</strong> {mr.analysis_time:.3f} s</p>
            
            <h3>Períodos y Frecuencias (primeros 10 modos)</h3>
            <table>
                <tr><th>Modo</th><th>Período</th><th>Frecuencia</th></tr>
                {periods_table}
            </table>
        </div>
        """
    
    def _get_technical_info_html(self, analysis_results: AnalysisResults) -> str:
        """Genera sección de información técnica."""
        return f"""
        <div class="section">
            <h2>🔧 Información Técnica</h2>
            <table>
                <tr><th>Parámetro</th><th>Valor</th></tr>
                <tr><td>Nombre del Modelo</td><td>{analysis_results.model_name}</td></tr>
                <tr><td>Timestamp</td><td>{analysis_results.timestamp}</td></tr>
                <tr><td>Tiempo Total de Análisis</td><td>{analysis_results.total_analysis_time:.3f} s</td></tr>
                <tr><td>Estado del Análisis</td><td>{'Exitoso' if analysis_results.success else 'Falló'}</td></tr>
            </table>
        </div>
        """
    
    def _get_errors_html(self, analysis_results: AnalysisResults) -> str:
        """Genera sección de errores si los hay."""
        if not analysis_results.errors:
            return ""
        
        errors_list = "".join(f"<li>{error}</li>" for error in analysis_results.errors)
        
        return f"""
        <div class="section">
            <h2 class="error">❌ Errores Encontrados</h2>
            <ul>{errors_list}</ul>
        </div>
        """
    
    def _create_structured_report_data(self, analysis_results: AnalysisResults, config: Dict[str, Any]) -> Dict[str, Any]:
        """Crea datos estructurados para reporte JSON."""
        report_data = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "model_name": analysis_results.model_name,
                "analysis_timestamp": analysis_results.timestamp,
                "report_version": "1.0.0"
            },
            "analysis_summary": {
                "success": analysis_results.success,
                "total_time": analysis_results.total_analysis_time,
                "errors": analysis_results.errors
            }
        }
        
        if analysis_results.static_results:
            report_data["static_analysis"] = {
                "max_displacement": analysis_results.static_results.max_displacement,
                "max_stress": analysis_results.static_results.max_stress,
                "convergence_achieved": analysis_results.static_results.convergence_achieved,
                "num_iterations": analysis_results.static_results.num_iterations,
                "analysis_time": analysis_results.static_results.analysis_time
            }
        
        if analysis_results.modal_results:
            report_data["modal_analysis"] = {
                "num_modes": len(analysis_results.modal_results.periods),
                "periods": analysis_results.modal_results.periods,
                "frequencies": analysis_results.modal_results.frequencies,
                "analysis_time": analysis_results.modal_results.analysis_time
            }
        
        return report_data
    
    def _create_text_report(self, analysis_results: AnalysisResults, config: Dict[str, Any]) -> str:
        """Crea reporte en formato de texto."""
        lines = [
            "=" * 60,
            f"REPORTE DE ANÁLISIS ESTRUCTURAL",
            "=" * 60,
            f"Modelo: {analysis_results.model_name}",
            f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Estado: {'EXITOSO' if analysis_results.success else 'FALLÓ'}",
            f"Tiempo total: {analysis_results.total_analysis_time:.3f} s",
            "",
        ]
        
        if analysis_results.static_results:
            lines.extend([
                "ANÁLISIS ESTÁTICO",
                "-" * 20,
                f"Desplazamiento máximo: {analysis_results.static_results.max_displacement:.6f} m",
                f"Esfuerzo máximo: {analysis_results.static_results.max_stress:.2f} MPa",
                f"Convergencia: {'Sí' if analysis_results.static_results.convergence_achieved else 'No'}",
                f"Iteraciones: {analysis_results.static_results.num_iterations}",
                f"Tiempo: {analysis_results.static_results.analysis_time:.3f} s",
                "",
            ])
        
        if analysis_results.modal_results:
            lines.extend([
                "ANÁLISIS MODAL",
                "-" * 20,
                f"Número de modos: {len(analysis_results.modal_results.periods)}",
                f"Primer período: {analysis_results.modal_results.periods[0]:.4f} s",
                f"Tiempo: {analysis_results.modal_results.analysis_time:.3f} s",
                "",
                "Períodos (primeros 10 modos):",
            ])
            
            for i, period in enumerate(analysis_results.modal_results.periods[:10], 1):
                lines.append(f"  Modo {i:2d}: {period:.4f} s")
            
            lines.append("")
        
        if analysis_results.errors:
            lines.extend([
                "ERRORES",
                "-" * 20,
            ])
            for error in analysis_results.errors:
                lines.append(f"  • {error}")
            lines.append("")
        
        lines.extend([
            "=" * 60,
            "Fin del reporte",
            "=" * 60,
        ])
        
        return "\n".join(lines)
    
    def _generate_consolidated_html(self, results_list: List[AnalysisResults], config: Dict[str, Any]) -> str:
        """Genera reporte HTML consolidado."""
        try:
            reports_dir = os.path.join(self.output_dir, "reports")
            html_file = os.path.join(reports_dir, "consolidated_report.html")
            
            # Crear contenido HTML consolidado
            html_content = self._create_consolidated_html_content(results_list, config)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"   ✅ Reporte consolidado HTML: {os.path.basename(html_file)}")
            return html_file
            
        except Exception as e:
            print(f"   ❌ Error generando reporte consolidado HTML: {e}")
            return None
    
    def _generate_consolidated_json(self, results_list: List[AnalysisResults], config: Dict[str, Any]) -> str:
        """Genera reporte JSON consolidado."""
        try:
            reports_dir = os.path.join(self.output_dir, "reports")
            json_file = os.path.join(reports_dir, "consolidated_report.json")
            
            consolidated_data = {
                "report_metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "total_models": len(results_list),
                    "report_type": "consolidated",
                    "report_version": "1.0.0"
                },
                "summary": {
                    "successful_analyses": len([r for r in results_list if r.success]),
                    "failed_analyses": len([r for r in results_list if not r.success]),
                    "total_analysis_time": sum(r.total_analysis_time for r in results_list)
                },
                "individual_results": [
                    self._create_structured_report_data(result, config) 
                    for result in results_list
                ]
            }
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(consolidated_data, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Reporte consolidado JSON: {os.path.basename(json_file)}")
            return json_file
            
        except Exception as e:
            print(f"   ❌ Error generando reporte consolidado JSON: {e}")
            return None
    
    def _create_consolidated_html_content(self, results_list: List[AnalysisResults], config: Dict[str, Any]) -> str:
        """Crea contenido HTML para reporte consolidado."""
        successful = [r for r in results_list if r.success]
        failed = [r for r in results_list if not r.success]
        
        models_table = ""
        for result in results_list:
            status = "✅ Exitoso" if result.success else "❌ Falló"
            max_disp = f"{result.static_results.max_displacement:.6f}" if result.static_results else "N/A"
            first_period = f"{result.modal_results.periods[0]:.3f}" if result.modal_results and result.modal_results.periods else "N/A"
            
            models_table += f"""
            <tr>
                <td>{result.model_name}</td>
                <td>{status}</td>
                <td>{max_disp}</td>
                <td>{first_period}</td>
                <td>{result.total_analysis_time:.3f} s</td>
            </tr>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Reporte Consolidado de Análisis</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #e8f5e8; padding: 20px; border-radius: 5px; }}
                .summary {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .summary-box {{ text-align: center; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
                .summary-number {{ font-size: 2em; font-weight: bold; color: #007bff; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f8f9fa; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Reporte Consolidado de Análisis</h1>
                <p>Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Total de modelos analizados: {len(results_list)}</p>
            </div>
            
            <div class="summary">
                <div class="summary-box">
                    <div class="summary-number">{len(successful)}</div>
                    <div>Exitosos</div>
                </div>
                <div class="summary-box">
                    <div class="summary-number">{len(failed)}</div>
                    <div>Fallos</div>
                </div>
                <div class="summary-box">
                    <div class="summary-number">{sum(r.total_analysis_time for r in results_list):.1f}s</div>
                    <div>Tiempo Total</div>
                </div>
            </div>
            
            <h2>Resultados por Modelo</h2>
            <table>
                <tr>
                    <th>Modelo</th>
                    <th>Estado</th>
                    <th>Despl. Máx (m)</th>
                    <th>Primer Período (s)</th>
                    <th>Tiempo (s)</th>
                </tr>
                {models_table}
            </table>
        </body>
        </html>
        """
