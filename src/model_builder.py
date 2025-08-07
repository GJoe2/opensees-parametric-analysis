"""
Refactored ModelBuilder using the new domain objects and specialized builders.

This is the new improved ModelBuilder that orchestrates the creation of structural models
using specialized builders following the Single Responsibility Principle.
"""


import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

from .builders.utility_object_builder import UtilityBuilder
from .domain import StructuralModel
from .builders import GeometryBuilder, SectionsBuilder, LoadsBuilder, AnalysisConfigBuilder, MaterialBuilder


class ModelBuilder:
    """
    Factory mejorado - orquesta la creación usando builders especializados.
    
    This ModelBuilder follows the improved architecture suggested in the proposal,
    separating concerns and improving maintainability.
    """
    
    def __init__(self):
        """
        Initialize the model builder.
        
        The ModelBuilder creates models in memory. Output directory is only needed
        when exporting models to files.
        """
        # Fixed parameters for geometry and sections
        self.fixed_params = {
            'column_size': (0.40, 0.40),  # 40x40 cm
            'beam_size': (0.25, 0.40),    # 25x40 cm
            'slab_thickness': 0.10,       # 10 cm
            'num_floors': 2,              # 2 floors
            'floor_height': 3.0,          # 3 m per floor
        }
        
        # Material parameters separated for better organization
        self.material_params = {
            'type': 'concrete',
            'E': 15000 * 210**0.5 * 0.001 / 0.01**2,  # Elastic modulus in tonf/m²
            'nu': 0.2,                    # Poisson's ratio
            'rho': (2.4 * 1.0 / 1.0**3) / 9.81,  # Density in tonf·s²/m⁴
            'fc': 210.0,                  # Concrete compressive strength
            'name': 'concrete_c210'
        }
    
    def _get_default_output_dir(self) -> str:
        """
        Get the default output directory relative to the current working directory.
        
        Returns:
            Default output directory path
        """
        if hasattr(sys.modules['__main__'], '__file__'):
            # Si se ejecuta como script
            script_dir = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
        else:
            # Si se ejecuta desde REPL/Jupyter, usar directorio actual
            script_dir = os.getcwd()
        
        return os.path.join(script_dir, "models")
    
    def update_material_params(self, **kwargs):
        """
        Update material parameters.
        
        Args:
            **kwargs: Material parameters to update (E, nu, rho, fc, fy, name, type)
        
        Example:
            builder.update_material_params(E=25000, fc=280, name="concrete_c280")
        """
        self.material_params.update(kwargs)
    
    def update_fixed_params(self, **kwargs):
        """
        Update fixed geometry/section parameters.
        
        Args:
            **kwargs: Fixed parameters to update (column_size, beam_size, slab_thickness, etc.)
        
        Example:
            builder.update_fixed_params(column_size=(0.50, 0.50), beam_size=(0.30, 0.50))
        """
        self.fixed_params.update(kwargs)
    
    def _ensure_output_dir(self, output_dir: str) -> str:
        """
        Ensure that the specified output directory exists and return absolute path.
        
        Args:
            output_dir: Directory path to create if it doesn't exist
            
        Returns:
            Absolute path to the output directory
        """
        # Convert relative paths to absolute paths based on script location
        if not os.path.isabs(output_dir):
            if hasattr(sys.modules['__main__'], '__file__'):
                # Si se ejecuta como script, relativo al script
                script_dir = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
                output_dir = os.path.join(script_dir, output_dir)
            else:
                # Si se ejecuta desde REPL/Jupyter, relativo al directorio actual
                output_dir = os.path.abspath(output_dir)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        return output_dir
    
    
    def create_model(self, L_B_ratio: float, B: float, nx: int, ny: int,
                    model_name: Optional[str] = None,
                    enabled_analyses: Optional[List[str]] = None,
                    analysis_params: Optional[Dict[str, Any]] = None) -> StructuralModel:
        """
        Create a structural model using specialized builders.
        
        Args:
            L_B_ratio: L/B ratio
            B: Width of the structure in meters
            nx: Number of axes in X direction
            ny: Number of axes in Y direction
            model_name: Model name (optional, will be auto-generated if not provided)
            enabled_analyses: List of analyses to enable ['static', 'modal', 'dynamic']
                            If None, uses ['static', 'modal'] by default
            analysis_params: Dictionary with custom parameters for analyses
                           e.g., {'modal': {'num_modes': 10}, 'dynamic': {'dt': 0.005}}
            
        Returns:
            StructuralModel instance
        """

        # Generate model name if not provided
        if model_name is None:
            model_name = UtilityBuilder.generate_model_name(L_B_ratio, B, nx, ny)

        # Set default enabled analyses
        if enabled_analyses is None:
            enabled_analyses = ['static', 'modal']

        # Set default analysis parameters
        if analysis_params is None:
            analysis_params = {}

        # Calculate dimensions
        L, B = UtilityBuilder.calculate_dimensions(L_B_ratio, B)
        
        # Create components using specialized builders
        geometry = GeometryBuilder.create(
            L_B_ratio=L_B_ratio,
            B=B,
            nx=nx,
            ny=ny,
            num_floors=self.fixed_params['num_floors'],
            floor_height=self.fixed_params['floor_height']
        )
        
        # Create material using MaterialBuilder
        material = MaterialBuilder.create(self.material_params)
        
        # Create sections with material reference
        sections = SectionsBuilder.create(self.fixed_params, material=material)
        
        loads = LoadsBuilder.create(
            geometry=geometry,
            load_params={'distributed_load': 1.0}
        )
        analysis_config = AnalysisConfigBuilder.create(
            enabled_analyses=enabled_analyses,
            analysis_params=analysis_params
        )
        
        # Create and save model
        model = StructuralModel(
            geometry=geometry,
            sections=sections,
            loads=loads,
            analysis_config=analysis_config,
            material=material,
            name=model_name
        )
        return model

    def export_model(self, model: StructuralModel, output_dir: Optional[str] = None) -> str:
        """
        Export the StructuralModel object to a JSON file.
        
        Args:
            model: StructuralModel instance to export
            output_dir: Directory where to save the model. If None, uses default directory
            
        Returns:
            Path to the exported file
        """
        if output_dir is None:
            output_dir = self._get_default_output_dir()
        
        output_dir = self._ensure_output_dir(output_dir)
        model_file = os.path.join(output_dir, f"{model.name}.json")
        model.save(model_file)
        return model_file
    
    def export_multiple_models(self, models: List[StructuralModel], output_dir: Optional[str] = None) -> List[str]:
        """
        Export multiple models to JSON files.
        
        Args:
            models: List of StructuralModel instances to export
            output_dir: Directory where to save the models. If None, uses default directory
            
        Returns:
            List of paths to the exported files
        """
        if output_dir is None:
            output_dir = self._get_default_output_dir()
        
        output_dir = self._ensure_output_dir(output_dir)
        exported_files = []
        
        for model in models:
            model_file = os.path.join(output_dir, f"{model.name}.json")
            model.save(model_file)
            exported_files.append(model_file)
        
        return exported_files
    
    def create_multiple_models(self, parameter_combinations: List[Dict]) -> List[StructuralModel]:
        """
        Create multiple models from parameter combinations.
        
        Args:
            parameter_combinations: List of dictionaries with model parameters
            
        Returns:
            List of created StructuralModel instances
        """
        models = []
        
        for params in parameter_combinations:
            model = self.create_model(
                L_B_ratio=params['L_B_ratio'],
                B=params['B'],
                nx=params['nx'],
                ny=params['ny'],
                model_name=params.get('model_name'),
                enabled_analyses=params.get('enabled_analyses'),
                analysis_params=params.get('analysis_params')
            )
            models.append(model)
        
        return models
    
    def get_model_summary(self, model: StructuralModel) -> Dict[str, Any]:
        """
        Get summary information about a model.
        
        Args:
            model: StructuralModel instance
            
        Returns:
            Dictionary with model summary
        """
        return model.get_model_summary()
    
    def update_fixed_params(self, **kwargs) -> None:
        """
        Update fixed parameters.
        
        Args:
            **kwargs: Parameters to update
        """
        self.fixed_params.update(kwargs)
    
    def get_fixed_params(self) -> Dict[str, Any]:
        """
        Get current fixed parameters.
        
        Returns:
            Dictionary with fixed parameters
        """
        return self.fixed_params.copy()
