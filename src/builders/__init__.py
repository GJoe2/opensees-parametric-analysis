"""
Specialized builders for structural model components.

This module contains builder classes that follow the Single Responsibility Principle,
each responsible for creating specific domain objects.
"""

try:
    # Try relative imports first (when used as module)
    from .geometry_builder import GeometryBuilder
    from .sections_builder import SectionsBuilder
    from .loads_builder import LoadsBuilder
    from .analysis_config_builder import AnalysisConfigBuilder
except ImportError:
    # Fall back to absolute imports (when run directly)
    from geometry_builder import GeometryBuilder
    from sections_builder import SectionsBuilder
    from loads_builder import LoadsBuilder
    from analysis_config_builder import AnalysisConfigBuilder

__all__ = [
    'GeometryBuilder',
    'SectionsBuilder',
    'LoadsBuilder',
    'AnalysisConfigBuilder'
]
