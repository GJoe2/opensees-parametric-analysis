import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Optional
import seaborn as sns

class ReportGenerator:
    """
    Clase para generar reportes de análisis paramétrico.
    Incluye desplazamientos y respuestas modales.
    """
    
    def __init__(self, results_dir: str = "results", reports_dir: str = "reports"):
        """
        Inicializa el generador de reportes.
        
        Args:
            results_dir: Directorio donde están los resultados
            reports_dir: Directorio donde se guardarán los reportes
        """
        self.results_dir = results_dir
        self.reports_dir = reports_dir
        self.ensure_reports_dir()
        
        # Configuración de gráficos
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def ensure_reports_dir(self):
        """Asegura que el directorio de reportes existe."""
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
    
    def load_analysis_results(self, results_file: str) -> Dict:
        """
        Carga resultados de análisis desde archivo.
        
        Args:
            results_file: Ruta al archivo de resultados
            
        Returns:
            Diccionario con los resultados
        """
        with open(results_file, 'r') as f:
            results = json.load(f)
        return results
    
    def load_all_results(self) -> List[Dict]:
        """
        Carga todos los resultados de análisis.
        
        Returns:
            Lista de diccionarios con resultados
        """
        results = []
        if os.path.exists(self.results_dir):
            for file in os.listdir(self.results_dir):
                if file.endswith('_results.json'):
                    file_path = os.path.join(self.results_dir, file)
                    try:
                        result = self.load_analysis_results(file_path)
                        results.append(result)
                    except Exception as e:
                        print(f"Error cargando {file}: {e}")
        return results
    
    def create_summary_dataframe(self, results: List[Dict]) -> pd.DataFrame:
        """
        Crea un DataFrame resumen con todos los resultados.
        
        Args:
            results: Lista de resultados de análisis
            
        Returns:
            DataFrame con resumen de resultados
        """
        summary_data = []
        
        for result in results:
            model_name = result['model_name']
            params = result['model_parameters']
            static = result['static_analysis']
            modal = result['modal_analysis']
            
            row = {
                'model_name': model_name,
                'L_B_ratio': params['L_B_ratio'],
                'nx': params['nx'],
                'ny': params['ny'],
                'L': params['L'],
                'B': params['B'],
                'static_success': static.get('success', False),
                'modal_success': modal.get('success', False),
                'max_displacement': static.get('max_displacement', 0.0),
                'num_modes': len(modal.get('frequencies', [])),
                'fundamental_period': modal.get('periods', [0.0])[0] if modal.get('periods') else 0.0,
                'fundamental_frequency': modal.get('frequencies', [0.0])[0] if modal.get('frequencies') else 0.0
            }
            
            # Agregar períodos de los primeros 3 modos
            periods = modal.get('periods', [])
            for i in range(3):
                row[f'period_mode_{i+1}'] = periods[i] if i < len(periods) else 0.0
            
            summary_data.append(row)
        
        return pd.DataFrame(summary_data)
    
    def generate_displacement_report(self, results: List[Dict], save_plots: bool = True) -> Dict:
        """
        Genera reporte de desplazamientos.
        
        Args:
            results: Lista de resultados de análisis
            save_plots: Si guardar las gráficas
            
        Returns:
            Diccionario con información del reporte
        """
        # Crear DataFrame resumen
        df = self.create_summary_dataframe(results)
        
        # Filtrar solo análisis exitosos
        df_success = df[df['static_success'] == True]
        
        if df_success.empty:
            print("No hay análisis estáticos exitosos para reportar")
            return {}
        
        # Gráficas de desplazamientos
        plots = {}
        
        # 1. Desplazamiento máximo vs L/B ratio
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        for nx_val in df_success['nx'].unique():
            data_nx = df_success[df_success['nx'] == nx_val]
            ax1.plot(data_nx['L_B_ratio'], data_nx['max_displacement'], 
                    marker='o', label=f'nx={nx_val}')
        
        ax1.set_xlabel('Relación L/B')
        ax1.set_ylabel('Desplazamiento Máximo (m)')
        ax1.set_title('Desplazamiento Máximo vs Relación L/B')
        ax1.legend()
        ax1.grid(True)
        
        if save_plots:
            plot_file1 = os.path.join(self.reports_dir, 'displacement_vs_LB_ratio.png')
            plt.savefig(plot_file1, dpi=300, bbox_inches='tight')
            plots['displacement_vs_LB_ratio'] = plot_file1
        
        # 2. Desplazamiento máximo vs nx
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        for lb_ratio in df_success['L_B_ratio'].unique():
            data_lb = df_success[df_success['L_B_ratio'] == lb_ratio]
            ax2.plot(data_lb['nx'], data_lb['max_displacement'], 
                    marker='s', label=f'L/B={lb_ratio}')
        
        ax2.set_xlabel('Número de ejes en X (nx)')
        ax2.set_ylabel('Desplazamiento Máximo (m)')
        ax2.set_title('Desplazamiento Máximo vs Número de ejes en X')
        ax2.legend()
        ax2.grid(True)
        
        if save_plots:
            plot_file2 = os.path.join(self.reports_dir, 'displacement_vs_nx.png')
            plt.savefig(plot_file2, dpi=300, bbox_inches='tight')
            plots['displacement_vs_nx'] = plot_file2
        
        # 3. Gráfica 3D de desplazamientos
        fig3d = go.Figure(data=[go.Scatter3d(
            x=df_success['L_B_ratio'],
            y=df_success['nx'],
            z=df_success['max_displacement'],
            mode='markers',
            marker=dict(
                size=8,
                color=df_success['max_displacement'],
                colorscale='Viridis',
                opacity=0.8
            ),
            text=df_success['model_name'],
            hovertemplate='<b>%{text}</b><br>' +
                         'L/B: %{x}<br>' +
                         'nx: %{y}<br>' +
                         'Desplazamiento: %{z:.4f} m<br>' +
                         '<extra></extra>'
        )])
        
        fig3d.update_layout(
            title='Desplazamiento Máximo vs Parámetros del Modelo',
            scene=dict(
                xaxis_title='Relación L/B',
                yaxis_title='Número de ejes en X (nx)',
                zaxis_title='Desplazamiento Máximo (m)'
            ),
            width=800,
            height=600
        )
        
        if save_plots:
            plot_file3d = os.path.join(self.reports_dir, 'displacement_3d.html')
            fig3d.write_html(plot_file3d)
            plots['displacement_3d'] = plot_file3d
        
        # Guardar datos en CSV
        csv_file = os.path.join(self.reports_dir, 'displacement_summary.csv')
        df_success.to_csv(csv_file, index=False)
        
        return {
            'plots': plots,
            'csv_file': csv_file,
            'summary_stats': {
                'total_models': len(df),
                'successful_models': len(df_success),
                'max_displacement': df_success['max_displacement'].max(),
                'min_displacement': df_success['max_displacement'].min(),
                'mean_displacement': df_success['max_displacement'].mean()
            }
        }
    
    def generate_modal_report(self, results: List[Dict], save_plots: bool = True) -> Dict:
        """
        Genera reporte de análisis modal.
        
        Args:
            results: Lista de resultados de análisis
            save_plots: Si guardar las gráficas
            
        Returns:
            Diccionario con información del reporte
        """
        # Crear DataFrame resumen
        df = self.create_summary_dataframe(results)
        
        # Filtrar solo análisis modales exitosos
        df_success = df[df['modal_success'] == True]
        
        if df_success.empty:
            print("No hay análisis modales exitosos para reportar")
            return {}
        
        # Gráficas modales
        plots = {}
        
        # 1. Período fundamental vs L/B ratio
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        for nx_val in df_success['nx'].unique():
            data_nx = df_success[df_success['nx'] == nx_val]
            ax1.plot(data_nx['L_B_ratio'], data_nx['fundamental_period'], 
                    marker='o', label=f'nx={nx_val}')
        
        ax1.set_xlabel('Relación L/B')
        ax1.set_ylabel('Período Fundamental (s)')
        ax1.set_title('Período Fundamental vs Relación L/B')
        ax1.legend()
        ax1.grid(True)
        
        if save_plots:
            plot_file1 = os.path.join(self.reports_dir, 'fundamental_period_vs_LB_ratio.png')
            plt.savefig(plot_file1, dpi=300, bbox_inches='tight')
            plots['fundamental_period_vs_LB_ratio'] = plot_file1
        
        # 2. Frecuencia fundamental vs nx
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        for lb_ratio in df_success['L_B_ratio'].unique():
            data_lb = df_success[df_success['L_B_ratio'] == lb_ratio]
            ax2.plot(data_lb['nx'], data_lb['fundamental_frequency'], 
                    marker='s', label=f'L/B={lb_ratio}')
        
        ax2.set_xlabel('Número de ejes en X (nx)')
        ax2.set_ylabel('Frecuencia Fundamental (Hz)')
        ax2.set_title('Frecuencia Fundamental vs Número de ejes en X')
        ax2.legend()
        ax2.grid(True)
        
        if save_plots:
            plot_file2 = os.path.join(self.reports_dir, 'fundamental_frequency_vs_nx.png')
            plt.savefig(plot_file2, dpi=300, bbox_inches='tight')
            plots['fundamental_frequency_vs_nx'] = plot_file2
        
        # 3. Comparación de períodos de los primeros 3 modos
        fig3, (ax3a, ax3b, ax3c) = plt.subplots(1, 3, figsize=(15, 5))
        
        for i, (ax, mode_num) in enumerate(zip([ax3a, ax3b, ax3c], [1, 2, 3])):
            for nx_val in df_success['nx'].unique():
                data_nx = df_success[df_success['nx'] == nx_val]
                ax.plot(data_nx['L_B_ratio'], data_nx[f'period_mode_{mode_num}'], 
                       marker='o', label=f'nx={nx_val}')
            
            ax.set_xlabel('Relación L/B')
            ax.set_ylabel(f'Período Modo {mode_num} (s)')
            ax.set_title(f'Período Modo {mode_num} vs Relación L/B')
            ax.legend()
            ax.grid(True)
        
        if save_plots:
            plot_file3 = os.path.join(self.reports_dir, 'periods_modes_1_2_3.png')
            plt.savefig(plot_file3, dpi=300, bbox_inches='tight')
            plots['periods_modes_1_2_3'] = plot_file3
        
        # 4. Gráfica 3D de períodos fundamentales
        fig3d = go.Figure(data=[go.Scatter3d(
            x=df_success['L_B_ratio'],
            y=df_success['nx'],
            z=df_success['fundamental_period'],
            mode='markers',
            marker=dict(
                size=8,
                color=df_success['fundamental_period'],
                colorscale='Plasma',
                opacity=0.8
            ),
            text=df_success['model_name'],
            hovertemplate='<b>%{text}</b><br>' +
                         'L/B: %{x}<br>' +
                         'nx: %{y}<br>' +
                         'Período: %{z:.4f} s<br>' +
                         '<extra></extra>'
        )])
        
        fig3d.update_layout(
            title='Período Fundamental vs Parámetros del Modelo',
            scene=dict(
                xaxis_title='Relación L/B',
                yaxis_title='Número de ejes en X (nx)',
                zaxis_title='Período Fundamental (s)'
            ),
            width=800,
            height=600
        )
        
        if save_plots:
            plot_file3d = os.path.join(self.reports_dir, 'fundamental_period_3d.html')
            fig3d.write_html(plot_file3d)
            plots['fundamental_period_3d'] = plot_file3d
        
        # Guardar datos en CSV
        csv_file = os.path.join(self.reports_dir, 'modal_summary.csv')
        df_success.to_csv(csv_file, index=False)
        
        return {
            'plots': plots,
            'csv_file': csv_file,
            'summary_stats': {
                'total_models': len(df),
                'successful_models': len(df_success),
                'max_period': df_success['fundamental_period'].max(),
                'min_period': df_success['fundamental_period'].min(),
                'mean_period': df_success['fundamental_period'].mean(),
                'max_frequency': df_success['fundamental_frequency'].max(),
                'min_frequency': df_success['fundamental_frequency'].min(),
                'mean_frequency': df_success['fundamental_frequency'].mean()
            }
        }
    
    def generate_comprehensive_report(self, results: List[Dict]) -> Dict:
        """
        Genera reporte completo combinando desplazamientos y análisis modal.
        
        Args:
            results: Lista de resultados de análisis
            
        Returns:
            Diccionario con información del reporte completo
        """
        print("Generando reporte completo...")
        
        # Generar reportes individuales
        displacement_report = self.generate_displacement_report(results)
        modal_report = self.generate_modal_report(results)
        
        # Crear reporte HTML completo
        html_content = self._create_html_report(results, displacement_report, modal_report)
        html_file = os.path.join(self.reports_dir, 'comprehensive_report.html')
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Crear resumen ejecutivo
        summary_file = os.path.join(self.reports_dir, 'executive_summary.txt')
        self._create_executive_summary(results, summary_file)
        
        return {
            'html_report': html_file,
            'summary_file': summary_file,
            'displacement_report': displacement_report,
            'modal_report': modal_report
        }
    
    def _create_html_report(self, results: List[Dict], displacement_report: Dict, 
                           modal_report: Dict) -> str:
        """Crea contenido HTML para el reporte completo."""
        df = self.create_summary_dataframe(results)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Reporte de Análisis Paramétrico</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2, h3 {{ color: #2c3e50; }}
                .summary {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; }}
                .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .stat-box {{ background-color: #e9ecef; padding: 10px; border-radius: 5px; text-align: center; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                img {{ max-width: 100%; height: auto; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <h1>Reporte de Análisis Paramétrico</h1>
            
            <div class="summary">
                <h2>Resumen Ejecutivo</h2>
                <div class="stats">
                    <div class="stat-box">
                        <h3>Total de Modelos</h3>
                        <p>{len(df)}</p>
                    </div>
                    <div class="stat-box">
                        <h3>Análisis Estáticos Exitosos</h3>
                        <p>{len(df[df['static_success'] == True])}</p>
                    </div>
                    <div class="stat-box">
                        <h3>Análisis Modales Exitosos</h3>
                        <p>{len(df[df['modal_success'] == True])}</p>
                    </div>
                </div>
            </div>
            
            <h2>Parámetros Analizados</h2>
            <ul>
                <li>Relaciones L/B: {sorted(df['L_B_ratio'].unique())}</li>
                <li>Valores de nx: {sorted(df['nx'].unique())}</li>
                <li>Valores de ny: {sorted(df['ny'].unique())}</li>
            </ul>
            
            <h2>Resultados de Desplazamientos</h2>
            <p>Estadísticas de desplazamientos máximos:</p>
            <ul>
                <li>Máximo: {displacement_report.get('summary_stats', {}).get('max_displacement', 0):.4f} m</li>
                <li>Mínimo: {displacement_report.get('summary_stats', {}).get('min_displacement', 0):.4f} m</li>
                <li>Promedio: {displacement_report.get('summary_stats', {}).get('mean_displacement', 0):.4f} m</li>
            </ul>
            
            <h2>Resultados Modales</h2>
            <p>Estadísticas de períodos fundamentales:</p>
            <ul>
                <li>Máximo: {modal_report.get('summary_stats', {}).get('max_period', 0):.4f} s</li>
                <li>Mínimo: {modal_report.get('summary_stats', {}).get('min_period', 0):.4f} s</li>
                <li>Promedio: {modal_report.get('summary_stats', {}).get('mean_period', 0):.4f} s</li>
            </ul>
            
            <h2>Tabla de Resultados</h2>
            {df.to_html(index=False)}
            
        </body>
        </html>
        """
        
        return html
    
    def _create_executive_summary(self, results: List[Dict], summary_file: str):
        """Crea un resumen ejecutivo en texto plano."""
        df = self.create_summary_dataframe(results)
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("RESUMEN EJECUTIVO - ANÁLISIS PARAMÉTRICO\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total de modelos analizados: {len(df)}\n")
            f.write(f"Análisis estáticos exitosos: {len(df[df['static_success'] == True])}\n")
            f.write(f"Análisis modales exitosos: {len(df[df['modal_success'] == True])}\n\n")
            
            f.write("PARÁMETROS ANALIZADOS:\n")
            f.write(f"- Relaciones L/B: {sorted(df['L_B_ratio'].unique())}\n")
            f.write(f"- Valores de nx: {sorted(df['nx'].unique())}\n")
            f.write(f"- Valores de ny: {sorted(df['ny'].unique())}\n\n")
            
            if not df[df['static_success'] == True].empty:
                df_static = df[df['static_success'] == True]
                f.write("RESULTADOS DE DESPLAZAMIENTOS:\n")
                f.write(f"- Desplazamiento máximo: {df_static['max_displacement'].max():.4f} m\n")
                f.write(f"- Desplazamiento mínimo: {df_static['max_displacement'].min():.4f} m\n")
                f.write(f"- Desplazamiento promedio: {df_static['max_displacement'].mean():.4f} m\n\n")
            
            if not df[df['modal_success'] == True].empty:
                df_modal = df[df['modal_success'] == True]
                f.write("RESULTADOS MODALES:\n")
                f.write(f"- Período fundamental máximo: {df_modal['fundamental_period'].max():.4f} s\n")
                f.write(f"- Período fundamental mínimo: {df_modal['fundamental_period'].min():.4f} s\n")
                f.write(f"- Período fundamental promedio: {df_modal['fundamental_period'].mean():.4f} s\n")
                f.write(f"- Frecuencia fundamental máxima: {df_modal['fundamental_frequency'].max():.4f} Hz\n")
                f.write(f"- Frecuencia fundamental mínima: {df_modal['fundamental_frequency'].min():.4f} Hz\n")
                f.write(f"- Frecuencia fundamental promedio: {df_modal['fundamental_frequency'].mean():.4f} Hz\n") 