"""
Analysis configuration domain objects.

Contains classes for representing analysis configurations and parameters.
"""

from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any


@dataclass
class StaticConfig:
    """Configuration for static analysis."""
    system: str = 'BandGeneral'
    numberer: str = 'RCM'
    constraints: str = 'Plain'
    integrator: str = 'LoadControl'
    algorithm: str = 'Linear'
    analysis: str = 'Static'
    steps: int = 10


@dataclass
class ModalConfig:
    """Configuration for modal analysis."""
    system: str = 'BandGeneral'
    numberer: str = 'RCM'
    constraints: str = 'Plain'
    integrator: str = 'LoadControl'
    algorithm: str = 'Linear'
    analysis: str = 'Static'
    num_modes: int = 6


@dataclass
class DynamicConfig:
    """Configuration for dynamic analysis."""
    system: str = 'BandGeneral'
    numberer: str = 'RCM'
    constraints: str = 'Plain'
    integrator: str = 'Newmark'
    algorithm: str = 'Newton'
    analysis: str = 'Transient'
    dt: float = 0.01
    num_steps: int = 1000


@dataclass
class VisualizationConfig:
    """Configuration for visualization."""
    enabled: bool = False
    static_deformed: bool = False
    modal_shapes: bool = False
    deform_scale: int = 100
    save_html: bool = True
    show_nodes: bool = True
    line_width: int = 2


@dataclass
class AnalysisConfig:
    """Configuration for all analysis types in a model."""
    enabled_analyses: List[str]
    static_config: Optional[StaticConfig] = None
    modal_config: Optional[ModalConfig] = None
    dynamic_config: Optional[DynamicConfig] = None
    visualization_config: VisualizationConfig = None
    
    def __post_init__(self):
        """Initialize default configurations based on enabled analyses."""
        if not self.enabled_analyses:
            raise ValueError("At least one analysis type must be enabled")
        
        # Initialize default visualization config if not provided
        if self.visualization_config is None:
            self.visualization_config = VisualizationConfig()
        
        # Initialize analysis configs based on enabled analyses
        if 'static' in self.enabled_analyses and self.static_config is None:
            self.static_config = StaticConfig()
        
        if 'modal' in self.enabled_analyses and self.modal_config is None:
            self.modal_config = ModalConfig()
        
        if 'dynamic' in self.enabled_analyses and self.dynamic_config is None:
            self.dynamic_config = DynamicConfig()
    
    def get_solver_config(self, analysis_type: str) -> Optional[Dict[str, Any]]:
        """
        Get solver configuration for a specific analysis type.
        
        Args:
            analysis_type: Type of analysis ('static', 'modal', 'dynamic')
            
        Returns:
            Configuration dictionary for the specified analysis type
        """
        if analysis_type == 'static' and self.static_config:
            return {
                'system': self.static_config.system,
                'numberer': self.static_config.numberer,
                'constraints': self.static_config.constraints,
                'integrator': self.static_config.integrator,
                'algorithm': self.static_config.algorithm,
                'analysis': self.static_config.analysis,
                'steps': self.static_config.steps
            }
        elif analysis_type == 'modal' and self.modal_config:
            return {
                'system': self.modal_config.system,
                'numberer': self.modal_config.numberer,
                'constraints': self.modal_config.constraints,
                'integrator': self.modal_config.integrator,
                'algorithm': self.modal_config.algorithm,
                'analysis': self.modal_config.analysis,
                'num_modes': self.modal_config.num_modes
            }
        elif analysis_type == 'dynamic' and self.dynamic_config:
            return {
                'system': self.dynamic_config.system,
                'numberer': self.dynamic_config.numberer,
                'constraints': self.dynamic_config.constraints,
                'integrator': self.dynamic_config.integrator,
                'algorithm': self.dynamic_config.algorithm,
                'analysis': self.dynamic_config.analysis,
                'dt': self.dynamic_config.dt,
                'num_steps': self.dynamic_config.num_steps
            }
        return None
    
    def is_enabled(self, analysis_type: str) -> bool:
        """
        Check if an analysis type is enabled.
        
        Args:
            analysis_type: Type of analysis to check
            
        Returns:
            True if the analysis type is enabled
        """
        return analysis_type in self.enabled_analyses
    
    def get_enabled_count(self) -> int:
        """Get the number of enabled analysis types."""
        return len(self.enabled_analyses)
    
    def update_visualization_config(self, **kwargs) -> None:
        """Update visualization configuration parameters."""
        for key, value in kwargs.items():
            if hasattr(self.visualization_config, key):
                setattr(self.visualization_config, key, value)
    
    def to_dict(self) -> dict:
        """Serialize analysis config to dictionary for JSON export."""
        result = {
            'enabled_analyses': self.enabled_analyses
        }
        
        if self.static_config:
            result['static_config'] = asdict(self.static_config)
        if self.modal_config:
            result['modal_config'] = asdict(self.modal_config)
        if self.dynamic_config:
            result['dynamic_config'] = asdict(self.dynamic_config)
        if self.visualization_config:
            result['visualization_config'] = asdict(self.visualization_config)
        
        return result
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AnalysisConfig':
        """Create analysis config from dictionary (JSON import)."""
        static_config = None
        if 'static_config' in data:
            static_config = StaticConfig(**data['static_config'])
        
        modal_config = None
        if 'modal_config' in data:
            modal_config = ModalConfig(**data['modal_config'])
        
        dynamic_config = None
        if 'dynamic_config' in data:
            dynamic_config = DynamicConfig(**data['dynamic_config'])
        
        visualization_config = None
        if 'visualization_config' in data:
            visualization_config = VisualizationConfig(**data['visualization_config'])
        
        return cls(
            enabled_analyses=data['enabled_analyses'],
            static_config=static_config,
            modal_config=modal_config,
            dynamic_config=dynamic_config,
            visualization_config=visualization_config
        )
