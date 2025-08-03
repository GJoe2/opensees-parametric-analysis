"""
Geometry domain objects.

Contains classes for representing geometric entities like nodes and elements.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class Node:
    """Represents a structural node."""
    tag: int
    coords: List[float]
    floor: int
    grid_pos: Optional[Tuple[int, int]] = None
    
    def __post_init__(self):
        """Validate node data after initialization."""
        if len(self.coords) != 3:
            raise ValueError("Node coordinates must have exactly 3 dimensions [x, y, z]")
        if self.floor < 0:
            raise ValueError("Floor number must be non-negative")


@dataclass
class Element:
    """Represents a structural element."""
    tag: int
    element_type: str  # 'slab', 'column', 'beam_x', 'beam_y'
    nodes: List[int]
    floor: int
    section_tag: int
    
    def __post_init__(self):
        """Validate element data after initialization."""
        if not self.nodes:
            raise ValueError("Element must have at least one node")
        if self.floor < 0:
            raise ValueError("Floor number must be non-negative")
        if self.section_tag <= 0:
            raise ValueError("Section tag must be positive")


@dataclass
class Geometry:
    """Represents the geometry of a structural model."""
    nodes: Dict[int, Node]
    elements: Dict[int, Element]
    L: float  # Length in X direction
    B: float  # Width in Y direction
    nx: int   # Number of divisions in X
    ny: int   # Number of divisions in Y
    num_floors: int
    floor_height: float
    
    def __post_init__(self):
        """Validate geometry data after initialization."""
        if self.L <= 0 or self.B <= 0:
            raise ValueError("Dimensions L and B must be positive")
        if self.nx <= 0 or self.ny <= 0:
            raise ValueError("Number of divisions nx and ny must be positive")
        if self.num_floors <= 0:
            raise ValueError("Number of floors must be positive")
        if self.floor_height <= 0:
            raise ValueError("Floor height must be positive")
    
    def get_boundary_nodes(self, floor: Optional[int] = None) -> List[Node]:
        """
        Get nodes on the boundary of the structure.
        
        Args:
            floor: Specific floor to get boundary nodes from. If None, gets from all floors.
            
        Returns:
            List of boundary nodes
        """
        boundary_nodes = []
        
        for node in self.nodes.values():
            if floor is not None and node.floor != floor:
                continue
                
            if node.grid_pos is not None:
                i, j = node.grid_pos
                # Node is on boundary if it's on the edge of the grid
                if i == 0 or i == self.nx or j == 0 or j == self.ny:
                    boundary_nodes.append(node)
        
        return boundary_nodes
    
    def get_floor_nodes(self, floor: int) -> List[Node]:
        """
        Get all nodes on a specific floor.
        
        Args:
            floor: Floor number
            
        Returns:
            List of nodes on the specified floor
        """
        return [node for node in self.nodes.values() if node.floor == floor]
    
    def get_elements_by_type(self, element_type: str, floor: Optional[int] = None) -> List[Element]:
        """
        Get elements of a specific type.
        
        Args:
            element_type: Type of element ('slab', 'column', 'beam_x', 'beam_y')
            floor: Specific floor to filter by. If None, gets from all floors.
            
        Returns:
            List of elements of the specified type
        """
        elements = []
        for element in self.elements.values():
            if element.element_type == element_type:
                if floor is None or element.floor == floor:
                    elements.append(element)
        return elements
    
    def get_total_height(self) -> float:
        """Get the total height of the structure."""
        return self.num_floors * self.floor_height
    
    def get_footprint_area(self) -> float:
        """Get the footprint area of the structure."""
        return self.L * self.B
    
    def get_aspect_ratio(self) -> float:
        """Get the aspect ratio L/B."""
        return self.L / self.B
