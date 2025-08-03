"""
Analysis configuration builder for creating analysis configurations.

This builder is responsible for creating analysis configurations based on enabled analyses and parameters.
"""

from typing import List, Dict, Any, Optional

try:
    # Try relative imports first (when used as module)
    from ..domain.analysis_config import (
        AnalysisConfig, StaticConfig, ModalConfig, DynamicConfig, VisualizationConfig
    )
except ImportError:
    # Fall back to absolute imports (when run directly)
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from domain.analysis_config import (
        AnalysisConfig, StaticConfig, ModalConfig, DynamicConfig, VisualizationConfig
    )


class AnalysisConfigBuilder:
    """Construye la configuración de análisis del modelo."""
    
    @staticmethod
    def create(enabled_analyses: List[str], analysis_params: Dict[str, Any]) -> AnalysisConfig:
        """
        Create analysis configuration for the structural model.
        
        Args:
            enabled_analyses: List of enabled analysis types
            analysis_params: Dictionary containing analysis parameters
            
        Returns:
            AnalysisConfig object with all configurations
        """
        # Create visualization configuration
        viz_config = AnalysisConfigBuilder._create_visualization_config(
            analysis_params.get('visualization', {})
        )
        
        # Create specific analysis configurations
        static_config = None
        modal_config = None
        dynamic_config = None
        
        if 'static' in enabled_analyses:
            static_config = AnalysisConfigBuilder._create_static_config(
                analysis_params.get('static', {})
            )
        
        if 'modal' in enabled_analyses:
            modal_config = AnalysisConfigBuilder._create_modal_config(
                analysis_params.get('modal', {})
            )
        
        if 'dynamic' in enabled_analyses:
            dynamic_config = AnalysisConfigBuilder._create_dynamic_config(
                analysis_params.get('dynamic', {})
            )
        
        return AnalysisConfig(
            enabled_analyses=enabled_analyses,
            static_config=static_config,
            modal_config=modal_config,
            dynamic_config=dynamic_config,
            visualization_config=viz_config
        )
    
    @staticmethod
    def _create_static_config(static_params: Dict[str, Any]) -> StaticConfig:
        """
        Create static analysis configuration.
        
        Args:
            static_params: Static analysis parameters
            
        Returns:
            StaticConfig object
        """
        return StaticConfig(
            system=static_params.get('system', 'BandGeneral'),
            numberer=static_params.get('numberer', 'RCM'),
            constraints=static_params.get('constraints', 'Plain'),
            integrator=static_params.get('integrator', 'LoadControl'),
            algorithm=static_params.get('algorithm', 'Linear'),
            analysis=static_params.get('analysis', 'Static'),
            steps=static_params.get('steps', 10)
        )
    
    @staticmethod
    def _create_modal_config(modal_params: Dict[str, Any]) -> ModalConfig:
        """
        Create modal analysis configuration.
        
        Args:
            modal_params: Modal analysis parameters
            
        Returns:
            ModalConfig object
        """
        return ModalConfig(
            system=modal_params.get('system', 'BandGeneral'),
            numberer=modal_params.get('numberer', 'RCM'),
            constraints=modal_params.get('constraints', 'Plain'),
            integrator=modal_params.get('integrator', 'LoadControl'),
            algorithm=modal_params.get('algorithm', 'Linear'),
            analysis=modal_params.get('analysis', 'Static'),
            num_modes=modal_params.get('num_modes', 6)
        )
    
    @staticmethod
    def _create_dynamic_config(dynamic_params: Dict[str, Any]) -> DynamicConfig:
        """
        Create dynamic analysis configuration.
        
        Args:
            dynamic_params: Dynamic analysis parameters
            
        Returns:
            DynamicConfig object
        """
        return DynamicConfig(
            system=dynamic_params.get('system', 'BandGeneral'),
            numberer=dynamic_params.get('numberer', 'RCM'),
            constraints=dynamic_params.get('constraints', 'Plain'),
            integrator=dynamic_params.get('integrator', 'Newmark'),
            algorithm=dynamic_params.get('algorithm', 'Newton'),
            analysis=dynamic_params.get('analysis', 'Transient'),
            dt=dynamic_params.get('dt', 0.01),
            num_steps=dynamic_params.get('num_steps', 1000)
        )
    
    @staticmethod
    def _create_visualization_config(viz_params: Dict[str, Any]) -> VisualizationConfig:
        """
        Create visualization configuration.
        
        Args:
            viz_params: Visualization parameters
            
        Returns:
            VisualizationConfig object
        """
        return VisualizationConfig(
            enabled=viz_params.get('enabled', False),
            static_deformed=viz_params.get('static_deformed', False),
            modal_shapes=viz_params.get('modal_shapes', False),
            deform_scale=viz_params.get('deform_scale', 100),
            save_html=viz_params.get('save_html', True),
            show_nodes=viz_params.get('show_nodes', True),
            line_width=viz_params.get('line_width', 2)
        )
    
    @staticmethod
    def create_default_config(enabled_analyses: List[str]) -> AnalysisConfig:
        """
        Create default analysis configuration for specified analysis types.
        
        Args:
            enabled_analyses: List of analysis types to enable
            
        Returns:
            AnalysisConfig with default settings
        """
        return AnalysisConfigBuilder.create(enabled_analyses, {})
    
    @staticmethod
    def create_custom_static_config(
        system: str = 'BandGeneral',
        numberer: str = 'RCM',
        constraints: str = 'Plain',
        integrator: str = 'LoadControl',
        algorithm: str = 'Linear',
        analysis: str = 'Static',
        steps: int = 10
    ) -> StaticConfig:
        """
        Create custom static analysis configuration.
        
        Returns:
            Custom StaticConfig object
        """
        return StaticConfig(
            system=system,
            numberer=numberer,
            constraints=constraints,
            integrator=integrator,
            algorithm=algorithm,
            analysis=analysis,
            steps=steps
        )
    
    @staticmethod
    def create_custom_modal_config(
        num_modes: int = 6,
        system: str = 'BandGeneral',
        numberer: str = 'RCM',
        constraints: str = 'Plain'
    ) -> ModalConfig:
        """
        Create custom modal analysis configuration.
        
        Returns:
            Custom ModalConfig object
        """
        return ModalConfig(
            system=system,
            numberer=numberer,
            constraints=constraints,
            integrator='LoadControl',
            algorithm='Linear',
            analysis='Static',
            num_modes=num_modes
        )
