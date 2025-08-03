"""
Domain objects for structural modeling.

This module contains the core domain objects that represent structural concepts
in an object-oriented way, separating business logic from infrastructure concerns.
"""

try:
    # Try relative imports first (when used as module)
    from .structural_model import StructuralModel
    from .geometry import Geometry, Node, Element
    from .sections import Sections, Section
    from .loads import Loads, Load
    from .analysis_config import AnalysisConfig, StaticConfig, ModalConfig, DynamicConfig, VisualizationConfig
except ImportError:
    # Fall back to absolute imports (when run directly)
    from structural_model import StructuralModel
    from geometry import Geometry, Node, Element
    from sections import Sections, Section
    from loads import Loads, Load
    from analysis_config import AnalysisConfig, StaticConfig, ModalConfig, DynamicConfig, VisualizationConfig

__all__ = [
    'StructuralModel',
    'Geometry', 'Node', 'Element',
    'Sections', 'Section',
    'Loads', 'Load',
    'AnalysisConfig', 'StaticConfig', 'ModalConfig', 'DynamicConfig', 'VisualizationConfig'
]
