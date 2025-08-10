"""
Load domain objects.

Contains classes for representing structural loads and loading conditions.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Any


@dataclass
class PointLoad:
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
    
    def to_dict(self) -> dict:
        """Serialize load to dictionary for JSON export."""
        return {
            'node_tag': self.node_tag,
            'load_type': self.load_type,
            'value': self.value,
            'direction': self.direction,
            'load_case': self.load_case
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PointLoad':
        """Create load from dictionary (JSON import)."""
        return cls(
            node_tag=data['node_tag'],
            load_type=data['load_type'],
            value=data['value'],
            direction=data['direction'],
            load_case=data.get('load_case')
        )


@dataclass
class LoadManager:
    """Container for all loads in a model."""
    loads: Dict[int, PointLoad]  # keyed by node_tag
    load_pattern_params: Dict[str, Any]
    
    def __init__(self, loads: Dict[int, PointLoad] = None, load_pattern_params: Dict[str, Any] = None):
        """Initialize loads container."""
        self.loads = loads or {}
        self.load_pattern_params = load_pattern_params or {}
    
    def add_load(self, load: PointLoad) -> None:
        """Add a load to the container."""
        self.loads[load.node_tag] = load
    
    def get_load_by_node(self, node_tag: int) -> Optional[PointLoad]:
        """Get the load applied to a specific node."""
        return self.loads.get(node_tag)
    
    def get_loads_by_type(self, load_type: str) -> Dict[int, PointLoad]:
        """Get all loads of a specific type."""
        return {
            node_tag: load for node_tag, load in self.loads.items()
            if load.load_type == load_type
        }
    
    def get_loads_by_case(self, load_case: str) -> Dict[int, PointLoad]:
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
    
    def to_dict(self) -> dict:
        """Serialize loads to dictionary for JSON export."""
        return {
            'loads': {str(k): v.to_dict() for k, v in self.loads.items()},
            'load_pattern_params': self.load_pattern_params
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'LoadManager':
        """Create loads from dictionary (JSON import)."""
        loads = {int(k): PointLoad.from_dict(v) for k, v in data.get('loads', {}).items()}
        load_pattern_params = data.get('load_pattern_params', {})
        
        return cls(
            loads=loads,
            load_pattern_params=load_pattern_params
        )
