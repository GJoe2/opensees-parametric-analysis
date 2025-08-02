"""
Ejemplo 06: Generación de Reportes
==================================

Este ejemplo muestra cómo generar reportes completos de análisis
con gráficas interactivas y documentación automática.

Caso de uso: Documentación automática de estudios de investigación
"""

from src.model_builder import ModelBuilder
from src.analysis_engine import AnalysisEngine
from src.parametric_runner import ParametricRunner
from src.report_generator import ReportGenerator
import os

def main():
    """Ejemplo de generación de reportes completos"""
    
    print("=== Ejemplo 06: Generación de Reportes ===")
    
    # === PREPARAR DATOS PARA REPORTES ===
    print("\n📊 Generando datos para reportes...")
    
    # Configurar componentes
    builder = ModelBuilder(output_dir="models")
    engine = AnalysisEngine()
    runner = ParametricRunner(builder, engine)
    
    # Generar conjunto de datos representativo
    print("\n1️⃣ Generando datos de ejemplo...")
    
    study_results = runner.run_full_study(
        L_B_ratios=[1.0, 1.5, 2.0],        # 3 relaciones
        B_values=[8.0, 12.0, 16.0],        # 3 tamaños
        nx_values=[3, 4, 5],               # 3 discretizaciones X
        ny_values=[3, 4],                  # 2 discretizaciones Y
        selection_method="distribution",    # Muestra representativa
        analysis_distribution={
            "static": 0.4,
            "modal": 0.4, 
            "complete": 0.2  # Algunos con análisis completo
        },
        progress_bar=True
    )
    
    print(f"   ✅ Datos generados: {len(study_results)} análisis")
    
    # === CONFIGURAR GENERADOR DE REPORTES ===
    print("\n📋 Configurando generador de reportes...")
    
    reporter = ReportGenerator(
        results_dir="results",
        reports_dir="reports",
        template_dir=None  # Usar plantillas por defecto
    )
    
    # === REPORTE 1: Reporte Básico ===
    print("\n2️⃣ Generando REPORTE BÁSICO...")
    
    basic_report = reporter.generate_basic_report(
        study_results,
        report_name="reporte_basico_ejemplo06",
        include_plots=['displacement_summary', 'period_summary'],
        export_format='html'
    )
    
    if basic_report:
        print(f"   ✅ Reporte básico generado: {basic_report}")
    
    # === REPORTE 2: Reporte Completo ===
    print("\n3️⃣ Generando REPORTE COMPLETO...")
    
    comprehensive_report = reporter.generate_comprehensive_report(
        study_results,
        report_name="reporte_completo_ejemplo06",
        include_sections=[
            'summary',
            'parameter_analysis', 
            'correlation_analysis',
            'detailed_results',
            'conclusions'
        ],
        export_formats=['html', 'pdf']  # Múltiples formatos
    )
    
    if comprehensive_report:
        print(f"   ✅ Reporte completo generado: {comprehensive_report}")
    
    # === REPORTE 3: Reporte de Comparación ===
    print("\n4️⃣ Generando REPORTE DE COMPARACIÓN...")
    
    # Filtrar resultados para comparación específica
    comparison_data = reporter.filter_results(
        study_results,
        filters={
            'B': [12.0],           # Solo edificios de 12m
            'nx': [3, 4, 5],       # Comparar discretizaciones
            'analysis_type': ['static', 'modal']  # Solo estos análisis
        }
    )
    
    comparison_report = reporter.generate_comparison_report(
        comparison_data,
        comparison_parameter='nx',  # Comparar por número de ejes X
        report_name="comparacion_discretizacion_ejemplo06",
        metrics=['max_displacement', 'fundamental_period'],
        include_charts=True
    )
    
    if comparison_report:
        print(f"   ✅ Reporte de comparación generado: {comparison_report}")
    
    # === REPORTE 4: Reporte Personalizado ===
    print("\n5️⃣ Generando REPORTE PERSONALIZADO...")
    
    # Configuración personalizada del reporte
    custom_config = {
        'title': 'Análisis Paramétrico de Edificios de Hormigón Armado',
        'subtitle': 'Ejemplo 06 - Sistema OpenSees',
        'author': 'Sistema Automatizado',
        'date': 'Agosto 2025',
        'include_methodology': True,
        'include_raw_data': False,
        'chart_style': 'professional',
        'color_scheme': 'blue_theme'
    }
    
    custom_report = reporter.generate_custom_report(
        study_results,
        config=custom_config,
        report_name="reporte_personalizado_ejemplo06",
        template='research_template'  # Plantilla específica
    )
    
    if custom_report:
        print(f"   ✅ Reporte personalizado generado: {custom_report}")
    
    # === EXPORTACIÓN DE DATOS ===
    print("\n6️⃣ Exportando DATOS EN MÚLTIPLES FORMATOS...")
    
    # Exportar a CSV para análisis externo
    csv_export = reporter.export_to_csv(
        study_results,
        filename="datos_ejemplo06.csv",
        include_metadata=True
    )
    
    if csv_export:
        print(f"   ✅ Datos exportados a CSV: {csv_export}")
    
    # Exportar a Excel con múltiples hojas
    excel_export = reporter.export_to_excel(
        study_results,
        filename="datos_ejemplo06.xlsx",
        separate_sheets=['parameters', 'static_results', 'modal_results']
    )
    
    if excel_export:
        print(f"   ✅ Datos exportados a Excel: {excel_export}")
    
    # Exportar metadatos
    metadata_export = reporter.export_metadata(
        study_results,
        filename="metadatos_ejemplo06.json",
        include_system_info=True
    )
    
    if metadata_export:
        print(f"   ✅ Metadatos exportados: {metadata_export}")
    
    # === ANÁLISIS ESTADÍSTICO AUTOMÁTICO ===
    print("\n7️⃣ Generando ANÁLISIS ESTADÍSTICO...")
    
    statistical_report = reporter.generate_statistical_analysis(
        study_results,
        report_name="analisis_estadistico_ejemplo06",
        include_analyses=[
            'descriptive_statistics',
            'correlation_matrix',
            'regression_analysis',
            'sensitivity_analysis'
        ],
        confidence_level=0.95
    )
    
    if statistical_report:
        print(f"   ✅ Análisis estadístico generado: {statistical_report}")
    
    # === RESUMEN DE ARCHIVOS GENERADOS ===
    print("\n" + "="*60)
    print("📁 RESUMEN DE ARCHIVOS GENERADOS")
    print("="*60)
    
    reports_dir = "reports"
    if os.path.exists(reports_dir):
        report_files = os.listdir(reports_dir)
        
        # Clasificar archivos por tipo
        html_files = [f for f in report_files if f.endswith('.html')]
        pdf_files = [f for f in report_files if f.endswith('.pdf')]
        csv_files = [f for f in report_files if f.endswith('.csv')]
        excel_files = [f for f in report_files if f.endswith('.xlsx')]
        json_files = [f for f in report_files if f.endswith('.json')]
        
        print(f"📄 Reportes HTML: {len(html_files)}")
        for file in html_files:
            print(f"   - {file}")
        
        print(f"📕 Reportes PDF: {len(pdf_files)}")
        for file in pdf_files:
            print(f"   - {file}")
        
        print(f"📊 Archivos de datos CSV: {len(csv_files)}")
        for file in csv_files:
            print(f"   - {file}")
        
        print(f"📈 Archivos Excel: {len(excel_files)}")
        for file in excel_files:
            print(f"   - {file}")
        
        print(f"⚙️  Archivos de metadatos: {len(json_files)}")
        for file in json_files:
            print(f"   - {file}")
        
        # Calcular tamaño total
        total_size = 0
        for file in report_files:
            file_path = os.path.join(reports_dir, file)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
        
        print(f"\\n💾 Tamaño total de reportes: {total_size / 1024:.1f} KB")
    
    # === INSTRUCCIONES DE USO ===
    print("\n" + "="*60)
    print("📖 INSTRUCCIONES DE USO DE REPORTES")
    print("="*60)
    
    print("""
🔍 TIPOS DE REPORTES GENERADOS:

1️⃣ REPORTE BÁSICO:
   - Resumen rápido de resultados
   - Gráficas principales
   - Ideal para revisiones rápidas

2️⃣ REPORTE COMPLETO:
   - Análisis detallado
   - Todas las gráficas y tablas
   - Conclusiones automáticas
   - Ideal para documentación final

3️⃣ REPORTE DE COMPARACIÓN:
   - Enfoque en un parámetro específico
   - Análisis comparativo detallado
   - Ideal para estudios de sensibilidad

4️⃣ REPORTE PERSONALIZADO:
   - Configuración específica
   - Branding personalizado
   - Ideal para presentaciones

5️⃣ ANÁLISIS ESTADÍSTICO:
   - Correlaciones y regresiones
   - Análisis de sensibilidad
   - Ideal para investigación académica

📊 FORMATOS DE EXPORTACIÓN:
   - HTML: Interactivo, gráficas dinámicas
   - PDF: Estático, ideal para impresión
   - CSV: Datos para análisis externo
   - Excel: Datos organizados en hojas
   - JSON: Metadatos del estudio
    """)
    
    # === RECOMENDACIONES FINALES ===
    print("\n💡 RECOMENDACIONES:")
    print("- Usar reportes básicos para revisiones diarias")
    print("- Usar reportes completos para documentación final")
    print("- Exportar a CSV para análisis en R/Python/MATLAB")
    print("- Usar reportes personalizados para presentaciones")
    print("- Mantener metadatos para reproducibilidad")
    
    print(f"\n✅ Ejemplo de reportes completado!")
    print(f"📁 Todos los reportes disponibles en: {reports_dir}/")

if __name__ == "__main__":
    main()
