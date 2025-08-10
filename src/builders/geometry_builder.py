"""
Geometry builder for creating structural geometry.

This builder is responsible for creating nodes and elements based on structural parameters.
"""

from typing import Dict, Tuple

from ..domain.geometry import Geometry, Node, Element
from ..domain.parameters import Parameters


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
        # Create parameters object (the "master keys")
        parameters = Parameters(
            L_B_ratio=L_B_ratio,
            B=B,
            nx=nx,
            ny=ny,
            num_floors=num_floors,
            floor_height=floor_height
        )
        
        # Create nodes and elements using parameters
        nodes = GeometryBuilder._create_nodes(parameters)
        elements = GeometryBuilder._create_elements(parameters)
        
        return Geometry(
            nodes=nodes,
            elements=elements
        )
    
    @staticmethod
    def _create_nodes(parameters: Parameters) -> Dict[int, Node]:
        """
        Create nodes for the structural model using parameters.
        
        Args:
            parameters: Parameters object containing all configuration
            
        Returns:
            Dictionary of nodes keyed by node tag
        """
        nodes = {}
        node_tag = 1
        
        # Grid spacing
        dx, dy = parameters.get_grid_dimensions()
        dz = parameters.floor_height
        
        # Create nodes for each floor (including base)
        for floor in range(parameters.num_floors + 1):
            z = floor * dz
            for j in range(parameters.ny + 1):
                for i in range(parameters.nx + 1):
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
    def _create_elements(parameters: Parameters) -> Dict[int, Element]:
        """
        Create elements for the structural model using parameters.
        
        Args:
            parameters: Parameters object containing all configuration
            
        Returns:
            Dictionary of elements keyed by element tag
        """
        elements = {}
        elem_tag = 1
        elem_tag = 1
        
        # Create slab elements (ShellMITC4) for each floor level (except base)
        for floor in range(1, parameters.num_floors + 1):
            base_node = floor * (parameters.nx + 1) * (parameters.ny + 1)
            for j in range(parameters.ny):
                for i in range(parameters.nx):
                    # Slab element nodes
                    n1 = base_node + j * (parameters.nx + 1) + i + 1
                    n2 = base_node + j * (parameters.nx + 1) + i + 2
                    n3 = base_node + (j + 1) * (parameters.nx + 1) + i + 2
                    n4 = base_node + (j + 1) * (parameters.nx + 1) + i + 1
                    
                    elements[elem_tag] = Element(
                        tag=elem_tag,
                        element_type='slab',
                        nodes=[n1, n2, n3, n4],
                        floor=floor,
                        section_tag=1
                    )
                    elem_tag += 1
        
        # Create column elements (elasticBeamColumn)
        for j in range(parameters.ny + 1):
            for i in range(parameters.nx + 1):
                for floor in range(parameters.num_floors):
                    # Column nodes
                    n1 = floor * (parameters.nx + 1) * (parameters.ny + 1) + j * (parameters.nx + 1) + i + 1
                    n2 = (floor + 1) * (parameters.nx + 1) * (parameters.ny + 1) + j * (parameters.nx + 1) + i + 1
                    
                    elements[elem_tag] = Element(
                        tag=elem_tag,
                        element_type='column',
                        nodes=[n1, n2],
                        floor=floor,
                        section_tag=2
                    )
                    elem_tag += 1
        
        # Create beam elements (elasticBeamColumn) for each floor level (except base)
        for floor in range(1, parameters.num_floors + 1):
            base_node = floor * (parameters.nx + 1) * (parameters.ny + 1)
            
            # Beams in X direction
            for j in range(parameters.ny + 1):
                for i in range(parameters.nx):
                    n1 = base_node + j * (parameters.nx + 1) + i + 1
                    n2 = base_node + j * (parameters.nx + 1) + i + 2
                    
                    elements[elem_tag] = Element(
                        tag=elem_tag,
                        element_type='beam_x',
                        nodes=[n1, n2],
                        floor=floor,
                        section_tag=3
                    )
                    elem_tag += 1
            
            # Beams in Y direction
            for j in range(parameters.ny):
                for i in range(parameters.nx + 1):
                    n1 = base_node + j * (parameters.nx + 1) + i + 1
                    n2 = base_node + (j + 1) * (parameters.nx + 1) + i + 1
                    
                    elements[elem_tag] = Element(
                        tag=elem_tag,
                        element_type='beam_y',
                        nodes=[n1, n2],
                        floor=floor,
                        section_tag=3
                    )
                    elem_tag += 1
        
        return elements
