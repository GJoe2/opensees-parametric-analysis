"""
Sistema de Análisis Paramétrico OpenSees

Un sistema completo de análisis paramétrico para estructuras de hormigón armado
usando OpenSees con arquitectura modular refactorizada.
"""

__version__ = "1.0.0"
__author__ = "GJoe2"
__email__ = "tu-email@ejemplo.com"
__license__ = "Apache 2.0"

# Importaciones principales para facilitar el uso
from .model_builder import ModelBuilder
from .analysis_engine import AnalysisEngine
from .parametric_runner import ParametricRunner
from .python_exporter import PythonExporter
from .report_generator import ReportGenerator

__all__ = [
    "ModelBuilder",
    "AnalysisEngine", 
    "ParametricRunner",
    "PythonExporter",
    "ReportGenerator",
]