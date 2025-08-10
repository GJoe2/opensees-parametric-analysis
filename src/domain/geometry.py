"""
Geometry domain objects.

Contains classes for representing geometric entities like nodes and elements.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from .parameters import Parameters


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
    
    def to_dict(self) -> dict:
        """Serialize node to dictionary for JSON export."""
        return {
            'tag': self.tag,
            'coords': self.coords,
            'floor': self.floor,
            'grid_pos': list(self.grid_pos) if self.grid_pos else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Node':
        """Create node from dictionary (JSON import)."""
        return cls(
            tag=data['tag'],
            coords=data['coords'],
            floor=data['floor'],
            grid_pos=tuple(data['grid_pos']) if data['grid_pos'] else None
        )


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
    
    def to_dict(self) -> dict:
        """Serialize element to dictionary for JSON export."""
        return {
            'tag': self.tag,
            'element_type': self.element_type,
            'nodes': self.nodes,
            'floor': self.floor,
            'section_tag': self.section_tag
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Element':
        """Create element from dictionary (JSON import)."""
        return cls(
            tag=data['tag'],
            element_type=data['element_type'],
            nodes=data['nodes'],
            floor=data['floor'],
            section_tag=data['section_tag']
        )


@dataclass
class Geometry:
    """Represents the geometry of a structural model."""
    nodes: Dict[int, Node]
    elements: Dict[int, Element]
    
    def __post_init__(self):
        """Validate geometry data after initialization."""
        if not self.nodes:
            raise ValueError("Geometry must have at least one node")
        if not self.elements:
            raise ValueError("Geometry must have at least one element")
    
    def get_boundary_nodes(self, nx: int, ny: int, floor: Optional[int] = None) -> List[Node]:
        """
        Get nodes on the boundary of the structure.
        
        Args:
            nx: Number of divisions in X direction
            ny: Number of divisions in Y direction
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
                if i == 0 or i == nx or j == 0 or j == ny:
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
    
    def to_dict(self) -> dict:
        """Serialize geometry to dictionary for JSON export."""
        return {
            'nodes': {str(k): v.to_dict() for k, v in self.nodes.items()},
            'elements': {str(k): v.to_dict() for k, v in self.elements.items()}
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Geometry':
        """Create geometry from dictionary (JSON import)."""
        nodes = {int(k): Node.from_dict(v) for k, v in data['nodes'].items()}
        elements = {int(k): Element.from_dict(v) for k, v in data['elements'].items()}
        
        return cls(
            nodes=nodes,
            elements=elements
        )
