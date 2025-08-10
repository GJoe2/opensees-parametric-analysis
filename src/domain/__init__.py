"""
Domain objects for structural modeling.

This module contains the core domain objects that represent structural concepts
in an object-oriented way, separating business logic from infrastructure concerns.
"""

# Clean imports without try-except complexity
from .structural_model import StructuralModel
from .geometry import Geometry, Node, Element
from .sections import Sections, Section
from .loads import PointLoad, LoadManager
from .analysis_config import AnalysisConfig, StaticConfig, ModalConfig, DynamicConfig, VisualizationConfig
from .material import Material
from .analysis_results import (
    AnalysisResults, StaticResults, ModalResults, DynamicResults,
    create_failed_results, create_successful_results
)

__all__ = [
    'StructuralModel',
    'Geometry', 'Node', 'Element',
    'Sections', 'Section',
    'PointLoad', 'LoadManager',
    'Material',
    'AnalysisConfig', 'StaticConfig', 'ModalConfig', 'DynamicConfig', 'VisualizationConfig',
    'AnalysisResults', 'StaticResults', 'ModalResults', 'DynamicResults',
    'create_failed_results', 'create_successful_results'
]
