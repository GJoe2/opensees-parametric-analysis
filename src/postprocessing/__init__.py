"""
Paquete de postprocesamiento.

Este paquete maneja todo el postprocesamiento separado del análisis numérico:
- Visualizaciones con opstool
- Generación de reportes
- Exportación de datos
"""

from .post_processor import PostProcessor
from .opstool_pipeline import OpstoolPipeline
from .report_generator import ReportGenerator
from .data_exporter import DataExporter

# Los componentes especializados se importan dinámicamente para evitar errores
# si no están todas las dependencias instaladas

__all__ = ['PostProcessor', 'OpstoolPipeline', 'ReportGenerator', 'DataExporter']
