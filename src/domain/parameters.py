"""
Parameters domain object.

Contains the parametric configuration that drives the entire structural model.
These are the "master keys" that control all aspects of the model generation.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class Parameters:
    """
    Represents the parametric configuration of a structural model.
    
    These parameters are the "master keys" that control:
    - Geometry generation (dimensions, grid, floors)
    - Section sizing (potentially)
    - Load distribution (potentially)
    - Analysis configuration (potentially)
    """
    # Primary geometric parameters
    L_B_ratio: float  # Length to width ratio
    B: float          # Width in Y direction (meters)
    nx: int           # Number of divisions in X direction
    ny: int           # Number of divisions in Y direction
    num_floors: int   # Number of floors
    floor_height: float  # Height of each floor (meters)
    
    # Additional parameters (for future extensions)
    additional_params: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate parameters after initialization."""
        if self.L_B_ratio <= 0:
            raise ValueError("L_B_ratio must be positive")
        if self.B <= 0:
            raise ValueError("B must be positive")
        if self.nx <= 0 or self.ny <= 0:
            raise ValueError("nx and ny must be positive")
        if self.num_floors <= 0:
            raise ValueError("num_floors must be positive")
        if self.floor_height <= 0:
            raise ValueError("floor_height must be positive")
        
        if self.additional_params is None:
            self.additional_params = {}
    
    @property
    def L(self) -> float:
        """Calculate length in X direction from B and L_B_ratio."""
        return self.B * self.L_B_ratio
    
    @property
    def total_height(self) -> float:
        """Calculate total height of the structure."""
        return self.num_floors * self.floor_height
    
    @property
    def footprint_area(self) -> float:
        """Calculate footprint area of the structure."""
        return self.L * self.B
    
    @property
    def aspect_ratio(self) -> float:
        """Get the aspect ratio L/B (same as L_B_ratio)."""
        return self.L_B_ratio
    
    @property
    def volume(self) -> float:
        """Calculate approximate volume of the structure."""
        return self.footprint_area * self.total_height
    
    def get_grid_dimensions(self) -> tuple[float, float]:
        """Get the spacing between grid lines in X and Y directions."""
        dx = self.L / self.nx
        dy = self.B / self.ny
        return dx, dy
    
    def get_parameter(self, key: str, default: Any = None) -> Any:
        """Get an additional parameter by key."""
        return self.additional_params.get(key, default)
    
    def set_parameter(self, key: str, value: Any) -> None:
        """Set an additional parameter."""
        self.additional_params[key] = value
    
    def get_model_scale_factor(self) -> str:
        """Get a qualitative description of the model scale."""
        area = self.footprint_area
        if area < 100:
            return "small"
        elif area < 500:
            return "medium"
        else:
            return "large"
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize parameters to dictionary for JSON export."""
        return {
            'L_B_ratio': self.L_B_ratio,
            'B': self.B,
            'nx': self.nx,
            'ny': self.ny,
            'num_floors': self.num_floors,
            'floor_height': self.floor_height,
            'L': self.L,  # Include calculated values for convenience
            'total_height': self.total_height,
            'footprint_area': self.footprint_area,
            'additional_params': self.additional_params
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Parameters':
        """Create parameters from dictionary (JSON import)."""
        return cls(
            L_B_ratio=data['L_B_ratio'],
            B=data['B'],
            nx=data['nx'],
            ny=data['ny'],
            num_floors=data['num_floors'],
            floor_height=data['floor_height'],
            additional_params=data.get('additional_params', {})
        )
    
    def copy(self) -> 'Parameters':
        """Create a copy of the parameters."""
        return Parameters(
            L_B_ratio=self.L_B_ratio,
            B=self.B,
            nx=self.nx,
            ny=self.ny,
            num_floors=self.num_floors,
            floor_height=self.floor_height,
            additional_params=self.additional_params.copy() if self.additional_params else None
        )
    
    def __str__(self) -> str:
        """String representation of parameters."""
        return (f"Parameters(L={self.L:.1f}m x B={self.B:.1f}m, "
                f"Grid={self.nx}x{self.ny}, Floors={self.num_floors}, "
                f"Height={self.floor_height:.1f}m)")
