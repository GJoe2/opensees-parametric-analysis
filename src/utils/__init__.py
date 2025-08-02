"""
Utilidades para el Sistema OpenSees Model Builder
================================================

Este paquete contiene módulos de utilidades y helpers que extienden
la funcionalidad del sistema principal.

Módulos disponibles:
- model_helpers: Métodos de conveniencia para ModelBuilder
- analysis_types: Clases especializadas para cada tipo de análisis
- visualization_helper: Helper para manejo de visualizaciones con opstool

Autor: OpenSees Model Builder
Fecha: Agosto 2025
"""

try:
    from .model_helpers import ModelBuilderHelpers
    from .analysis_types import StaticAnalysis, ModalAnalysis, DynamicAnalysis
    from .visualization_helper import VisualizationHelper
except ImportError:
    # Fallback para casos donde los imports relativos no funcionan
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    from model_helpers import ModelBuilderHelpers
    from analysis_types import StaticAnalysis, ModalAnalysis, DynamicAnalysis
    from visualization_helper import VisualizationHelper

__all__ = ['ModelBuilderHelpers']
