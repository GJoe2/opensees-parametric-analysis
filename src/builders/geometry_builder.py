"""
Geometry builder for creating structural geometry.

This builder is responsible for creating nodes and elements based on structural parameters.
"""

from typing import Dict, Tuple

try:
    # Try relative imports first (when used as module)
    from ..domain.geometry import Geometry, Node, Element
except ImportError:
    # Fall back to absolute imports (when run directly)
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from domain.geometry import Geometry, Node, Element


class GeometryBuilder:
    """Construye la geometría del modelo estructural."""
    
    @staticmethod
    def create(L_B_ratio: float, B: float, nx: int, ny: int, 
               num_floors: int, floor_height: float) -> Geometry:
        """
        Create a geometry object for the structural model.
        
        Args:
            L_B_ratio: Length to width ratio
            B: Width of the structure in meters
            nx: Number of divisions in X direction
            ny: Number of divisions in Y direction
            num_floors: Number of floors
            floor_height: Height of each floor
            
        Returns:
            Geometry object containing nodes and elements
        """
        # Calculate dimensions
        L = B * L_B_ratio
        
        # Create nodes and elements
        nodes = GeometryBuilder._create_nodes(L, B, nx, ny, num_floors, floor_height)
        elements = GeometryBuilder._create_elements(nx, ny, num_floors)
        
        return Geometry(
            nodes=nodes,
            elements=elements,
            L=L,
            B=B,
            nx=nx,
            ny=ny,
            num_floors=num_floors,
            floor_height=floor_height
        )
    
    @staticmethod
    def _create_nodes(L: float, B: float, nx: int, ny: int, 
                     num_floors: int, floor_height: float) -> Dict[int, Node]:
        """
        Create nodes for the structural model.
        
        Args:
            L: Length in X direction
            B: Width in Y direction
            nx: Number of divisions in X
            ny: Number of divisions in Y
            num_floors: Number of floors
            floor_height: Height of each floor
            
        Returns:
            Dictionary of nodes keyed by node tag
        """
        nodes = {}
        node_tag = 1
        
        # Grid spacing
        dx = L / nx
        dy = B / ny
        dz = floor_height
        
        # Create nodes for each floor (including base)
        for floor in range(num_floors + 1):
            z = floor * dz
            for j in range(ny + 1):
                for i in range(nx + 1):
                    x = i * dx
                    y = j * dy
                    
                    nodes[node_tag] = Node(
                        tag=node_tag,
                        coords=[x, y, z],
                        floor=floor,
                        grid_pos=(i, j)
                    )
                    node_tag += 1
        
        return nodes
    
    @staticmethod
    def _create_elements(nx: int, ny: int, num_floors: int) -> Dict[int, Element]:
        """
        Create elements for the structural model.
        
        Args:
            nx: Number of divisions in X
            ny: Number of divisions in Y
            num_floors: Number of floors
            
        Returns:
            Dictionary of elements keyed by element tag
        """
        elements = {}
        elem_tag = 1
        
        # Create slab elements (ShellMITC4) for each floor level (except base)
        for floor in range(1, num_floors + 1):
            base_node = floor * (nx + 1) * (ny + 1)
            for j in range(ny):
                for i in range(nx):
                    # Slab element nodes
                    n1 = base_node + j * (nx + 1) + i + 1
                    n2 = base_node + j * (nx + 1) + i + 2
                    n3 = base_node + (j + 1) * (nx + 1) + i + 2
                    n4 = base_node + (j + 1) * (nx + 1) + i + 1
                    
                    elements[elem_tag] = Element(
                        tag=elem_tag,
                        element_type='slab',
                        nodes=[n1, n2, n3, n4],
                        floor=floor,
                        section_tag=1
                    )
                    elem_tag += 1
        
        # Create column elements (elasticBeamColumn)
        for j in range(ny + 1):
            for i in range(nx + 1):
                for floor in range(num_floors):
                    # Column nodes
                    n1 = floor * (nx + 1) * (ny + 1) + j * (nx + 1) + i + 1
                    n2 = (floor + 1) * (nx + 1) * (ny + 1) + j * (nx + 1) + i + 1
                    
                    elements[elem_tag] = Element(
                        tag=elem_tag,
                        element_type='column',
                        nodes=[n1, n2],
                        floor=floor,
                        section_tag=2
                    )
                    elem_tag += 1
        
        # Create beam elements (elasticBeamColumn) for each floor level (except base)
        for floor in range(1, num_floors + 1):
            base_node = floor * (nx + 1) * (ny + 1)
            
            # Beams in X direction
            for j in range(ny + 1):
                for i in range(nx):
                    n1 = base_node + j * (nx + 1) + i + 1
                    n2 = base_node + j * (nx + 1) + i + 2
                    
                    elements[elem_tag] = Element(
                        tag=elem_tag,
                        element_type='beam_x',
                        nodes=[n1, n2],
                        floor=floor,
                        section_tag=3
                    )
                    elem_tag += 1
            
            # Beams in Y direction
            for j in range(ny):
                for i in range(nx + 1):
                    n1 = base_node + j * (nx + 1) + i + 1
                    n2 = base_node + (j + 1) * (nx + 1) + i + 1
                    
                    elements[elem_tag] = Element(
                        tag=elem_tag,
                        element_type='beam_y',
                        nodes=[n1, n2],
                        floor=floor,
                        section_tag=3
                    )
                    elem_tag += 1
        
        return elements
