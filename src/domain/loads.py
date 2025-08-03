"""
Load domain objects.

Contains classes for representing structural loads and loading conditions.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Any


@dataclass
class Load:
    """Represents a structural load applied to a node."""
    node_tag: int
    load_type: str  # 'distributed_load', 'point_load', 'moment', etc.
    value: float
    direction: str  # 'X', 'Y', 'Z', 'RX', 'RY', 'RZ'
    load_case: Optional[str] = None  # 'dead', 'live', 'seismic', etc.
    
    def __post_init__(self):
        """Validate load data after initialization."""
        if self.node_tag <= 0:
            raise ValueError("Node tag must be positive")
        if not self.load_type:
            raise ValueError("Load type cannot be empty")
        if self.direction not in ['X', 'Y', 'Z', 'RX', 'RY', 'RZ']:
            raise ValueError("Direction must be one of: X, Y, Z, RX, RY, RZ")


@dataclass
class Loads:
    """Container for all loads in a model."""
    loads: Dict[int, Load]  # keyed by node_tag
    load_pattern_params: Dict[str, Any]
    
    def __init__(self, loads: Dict[int, Load] = None, load_pattern_params: Dict[str, Any] = None):
        """Initialize loads container."""
        self.loads = loads or {}
        self.load_pattern_params = load_pattern_params or {}
    
    def add_load(self, load: Load) -> None:
        """Add a load to the container."""
        self.loads[load.node_tag] = load
    
    def get_load_by_node(self, node_tag: int) -> Optional[Load]:
        """Get the load applied to a specific node."""
        return self.loads.get(node_tag)
    
    def get_loads_by_type(self, load_type: str) -> Dict[int, Load]:
        """Get all loads of a specific type."""
        return {
            node_tag: load for node_tag, load in self.loads.items()
            if load.load_type == load_type
        }
    
    def get_loads_by_case(self, load_case: str) -> Dict[int, Load]:
        """Get all loads of a specific load case."""
        return {
            node_tag: load for node_tag, load in self.loads.items()
            if load.load_case == load_case
        }
    
    def get_total_vertical_load(self) -> float:
        """Calculate total vertical load (Z direction)."""
        total = 0.0
        for load in self.loads.values():
            if load.direction == 'Z':
                total += abs(load.value)
        return total
    
    def get_loaded_nodes(self) -> list:
        """Get list of all nodes that have loads applied."""
        return list(self.loads.keys())
