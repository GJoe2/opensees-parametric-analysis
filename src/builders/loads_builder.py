"""
Loads builder for creating structural loads.

This builder is responsible for creating loads based on geometry and load parameters.
"""

from typing import Dict, Any

try:
    # Try relative imports first (when used as module)
    from ..domain.geometry import Geometry
    from ..domain.loads import Loads, Load
except ImportError:
    # Fall back to absolute imports (when run directly)
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from domain.geometry import Geometry
    from domain.loads import Loads, Load


class LoadsBuilder:
    """Construye las cargas del modelo estructural."""
    
    @staticmethod
    def create(geometry: Geometry, load_params: Dict[str, Any]) -> Loads:
        """
        Create loads for the structural model.
        
        Args:
            geometry: Geometry object containing nodes and elements
            load_params: Dictionary containing load parameters
            
        Returns:
            Loads object containing all loads
        """
        loads_dict = LoadsBuilder._create_distributed_loads(geometry, load_params)
        
        # Additional load patterns can be added here
        # loads_dict.update(LoadsBuilder._create_point_loads(geometry, load_params))
        # loads_dict.update(LoadsBuilder._create_seismic_loads(geometry, load_params))
        
        return Loads(
            loads=loads_dict,
            load_pattern_params=load_params
        )
    
    @staticmethod
    def _create_distributed_loads(geometry: Geometry, load_params: Dict[str, Any]) -> Dict[int, Load]:
        """
        Create distributed loads on the top floor.
        
        Args:
            geometry: Geometry object
            load_params: Load parameters
            
        Returns:
            Dictionary of loads keyed by node tag
        """
        loads = {}
        
        # Get distributed load magnitude (default 1.0 tonf/m²)
        q = load_params.get('distributed_load', 1.0)
        
        # Apply load to all nodes on the top floor
        top_floor = geometry.num_floors
        for node_tag, node in geometry.nodes.items():
            if node.floor == top_floor:
                loads[node_tag] = Load(
                    node_tag=node_tag,
                    load_type='distributed_load',
                    value=-q,  # Negative for downward load
                    direction='Z',
                    load_case='dead'
                )
        
        return loads
    
    @staticmethod
    def _create_point_loads(geometry: Geometry, load_params: Dict[str, Any]) -> Dict[int, Load]:
        """
        Create point loads at specific locations.
        
        Args:
            geometry: Geometry object
            load_params: Load parameters
            
        Returns:
            Dictionary of loads keyed by node tag
        """
        loads = {}
        
        # Get point load specifications
        point_loads = load_params.get('point_loads', [])
        
        for point_load in point_loads:
            node_tag = point_load.get('node_tag')
            if node_tag and node_tag in geometry.nodes:
                loads[node_tag] = Load(
                    node_tag=node_tag,
                    load_type='point_load',
                    value=point_load.get('value', 0.0),
                    direction=point_load.get('direction', 'Z'),
                    load_case=point_load.get('load_case', 'live')
                )
        
        return loads
    
    @staticmethod
    def _create_seismic_loads(geometry: Geometry, load_params: Dict[str, Any]) -> Dict[int, Load]:
        """
        Create seismic loads based on structural characteristics.
        
        Args:
            geometry: Geometry object
            load_params: Load parameters
            
        Returns:
            Dictionary of loads keyed by node tag
        """
        loads = {}
        
        # Get seismic parameters
        seismic_params = load_params.get('seismic', {})
        if not seismic_params.get('enabled', False):
            return loads
        
        # Seismic load implementation would go here
        # This is a placeholder for future seismic load calculation
        
        return loads
    
    @staticmethod
    def create_custom_load_pattern(geometry: Geometry, 
                                 load_specifications: list) -> Dict[int, Load]:
        """
        Create custom load pattern based on specifications.
        
        Args:
            geometry: Geometry object
            load_specifications: List of load specifications
            
        Returns:
            Dictionary of loads keyed by node tag
        """
        loads = {}
        
        for spec in load_specifications:
            node_tag = spec.get('node_tag')
            if node_tag and node_tag in geometry.nodes:
                loads[node_tag] = Load(
                    node_tag=node_tag,
                    load_type=spec.get('load_type', 'custom'),
                    value=spec.get('value', 0.0),
                    direction=spec.get('direction', 'Z'),
                    load_case=spec.get('load_case', 'custom')
                )
        
        return loads
