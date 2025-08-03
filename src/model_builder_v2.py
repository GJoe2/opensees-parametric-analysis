"""
Refactored ModelBuilder using the new domain objects and specialized builders.

This is the new improved ModelBuilder that orchestrates the creation of structural models
using specialized builders following the Single Responsibility Principle.
"""

import os
import sys
from typing import Dict, List, Optional, Any

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    # Try relative imports first (when used as module)
    from .domain import StructuralModel
    from .builders import GeometryBuilder, SectionsBuilder, LoadsBuilder, AnalysisConfigBuilder
except ImportError:
    # Fall back to absolute imports (when run directly)
    from domain import StructuralModel
    from builders import GeometryBuilder, SectionsBuilder, LoadsBuilder, AnalysisConfigBuilder


class ModelBuilder:
    """
    Factory mejorado - orquesta la creación usando builders especializados.
    
    This ModelBuilder follows the improved architecture suggested in the proposal,
    separating concerns and improving maintainability.
    """
    
    def __init__(self, output_dir: str = "models"):
        """
        Initialize the model builder.
        
        Args:
            output_dir: Directory where models will be saved
        """
        self.output_dir = output_dir
        self.ensure_output_dir()
        
        # Fixed parameters for the structural model
        self.fixed_params = {
            'column_size': (0.40, 0.40),  # 40x40 cm
            'beam_size': (0.25, 0.40),    # 25x40 cm
            'slab_thickness': 0.10,       # 10 cm
            'num_floors': 2,              # 2 floors
            'floor_height': 3.0,          # 3 m per floor
            'E': 15000 * 210**0.5 * 0.001 / 0.01**2,  # Elastic modulus in tonf/m²
            'nu': 0.2,                    # Poisson's ratio
            'rho': (2.4 * 1.0 / 1.0**3) / 9.81  # Density in tonf·s²/m⁴
        }
    
    def ensure_output_dir(self) -> None:
        """Ensure that the output directory exists."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_model_name(self, L_B_ratio: float, B: float, nx: int, ny: int) -> str:
        """
        Generate encoded name for the model.
        
        Args:
            L_B_ratio: L/B ratio (aspect ratio)
            B: Width of the structure in meters
            nx: Number of axes in X direction
            ny: Number of axes in Y direction
            
        Returns:
            Encoded model name (e.g., F01_15_10_1224)
        """
        # Convert L/B ratio to 2-digit format (e.g., 1.5 -> 15)
        aspect_code = int(L_B_ratio * 10)
        
        # Convert B to 2-digit format (e.g., 10.0 -> 10)
        B_code = int(B)
        
        # Combine nx and ny into 4-digit format (e.g., nx=12, ny=24 -> 1224)
        grid_code = nx * 100 + ny
        
        return f"F01_{aspect_code:02d}_{B_code:02d}_{grid_code:04d}"
    
    def calculate_dimensions(self, L_B_ratio: float, B: float) -> tuple:
        """
        Calculate L and B dimensions based on L/B ratio.
        
        Args:
            L_B_ratio: L/B ratio
            B: Width of the structure in meters
            
        Returns:
            Tuple with (L, B) in meters
        """
        L = B * L_B_ratio
        return L, B
    
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
            model_name = self.generate_model_name(L_B_ratio, B, nx, ny)
        
        # Set default enabled analyses
        if enabled_analyses is None:
            enabled_analyses = ['static', 'modal']
        
        # Set default analysis parameters
        if analysis_params is None:
            analysis_params = {}
        
        # Calculate dimensions
        L, B = self.calculate_dimensions(L_B_ratio, B)
        
        # Create components using specialized builders
        geometry = GeometryBuilder.create(
            L_B_ratio=L_B_ratio,
            B=B,
            nx=nx,
            ny=ny,
            num_floors=self.fixed_params['num_floors'],
            floor_height=self.fixed_params['floor_height']
        )
        
        sections = SectionsBuilder.create(self.fixed_params)
        
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
            name=model_name
        )
        
        # Save model to file
        model_file = os.path.join(self.output_dir, f"{model_name}.json")
        model.save(model_file)
        
        return model
    
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
    
    def set_output_dir(self, output_dir: str) -> None:
        """
        Set the output directory and ensure it exists.
        
        Args:
            output_dir: New output directory path
        """
        self.output_dir = output_dir
        self.ensure_output_dir()
