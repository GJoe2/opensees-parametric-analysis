"""
Structural model domain object.

Contains the main domain object that represents a complete structural model.
"""

import json
import os
from dataclasses import dataclass
from typing import Dict, Any

from .geometry import Geometry
from .sections import Sections
from .loads import LoadManager
from .analysis_config import AnalysisConfig
from .material import Material
from .parameters import Parameters


@dataclass
class StructuralModel:
    """Represents a complete structural model."""
    parameters: Parameters  # Master keys - parametric configuration
    geometry: Geometry
    sections: Sections
    loads: LoadManager
    analysis_config: AnalysisConfig
    material: Material
    name: str
    
    def __post_init__(self):
        """Validate model data after initialization."""
        if not self.name:
            raise ValueError("Model name cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the model to a dictionary for JSON export.
        
        Returns:
            Dictionary representation of the model
        """
        # Get sections data and extract specific components
        sections_data = self.sections.to_dict()
        sections_dict = sections_data.get('sections', {})  # Extract sections dict
        transformations = sections_data.get('transformations', {})
        
        # Get loads data and extract load_pattern_params
        loads_data = self.loads.to_dict()
        loads_dict = loads_data.get('loads', {})  # Extract loads dict
        load_pattern_params = loads_data.get('load_pattern_params', {})
        
        # Get geometry data
        geometry_data = self.geometry.to_dict()
        nodes = geometry_data.get('nodes', {})
        elements = geometry_data.get('elements', {})
        
        # Build the result in the desired order
        result = {
            'name': self.name,
            'parameters': self.parameters.to_dict(),
            'material': self.material.to_dict(),
            'sections': sections_dict,  # Direct assignment of sections dict
            'transformations': transformations,
            'nodes': nodes,
            'elements': elements,
            'loads': loads_dict,  # Direct assignment of loads dict
            'analysis_config': self.analysis_config.to_dict()
        }
        
        # Add load_pattern_params if they exist
        if load_pattern_params:
            result['load_pattern_params'] = load_pattern_params
            
        return result
    
    def save(self, filepath: str) -> None:
        """
        Save the model to a JSON file.
        
        Args:
            filepath: Path where to save the model file
        """
        # Ensure the directory exists only if there's a directory in the path
        directory = os.path.dirname(filepath)
        if directory:  # Only create directory if there's one specified
            os.makedirs(directory, exist_ok=True)
        
        # Convert to dict and save
        model_dict = self.to_dict()
        model_dict['file_path'] = filepath  # Add file path to the saved data
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(model_dict, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load(cls, filepath: str) -> 'StructuralModel':
        """
        Load a model from a JSON file.
        
        Args:
            filepath: Path to the model file
            
        Returns:
            StructuralModel instance
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls.from_dict(data)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StructuralModel':
        """
        Create a StructuralModel from a dictionary (JSON import).
        
        Args:
            data: Dictionary containing model data
            
        Returns:
            StructuralModel instance
        """
        # Create parameters object
        parameters = Parameters.from_dict(data['parameters'])
        
        # Reconstruct geometry data
        geometry_data = {
            'nodes': data.get('nodes', {}),
            'elements': data.get('elements', {})
        }
        
        # Reconstruct sections data
        sections_data = data['sections'].copy()
        if 'transformations' in data:
            sections_data['transformations'] = data['transformations']
        
        # Reconstruct loads data
        loads_data = data.get('loads', {}).copy()
        if 'load_pattern_params' in data:
            loads_data['load_pattern_params'] = data['load_pattern_params']
        
        # Create domain objects
        geometry = Geometry.from_dict(geometry_data)
        sections = Sections.from_dict(sections_data)
        loads = LoadManager.from_dict(loads_data)
        analysis_config = AnalysisConfig.from_dict(data['analysis_config'])
        material = Material.from_dict(data['material'])
        
        return cls(
            parameters=parameters,
            geometry=geometry,
            sections=sections,
            loads=loads,
            analysis_config=analysis_config,
            material=material,
            name=data['name']
        )
    
    def get_model_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the model's key characteristics.
        
        Returns:
            Dictionary with model summary information
        """
        return {
            'name': self.name,
            'dimensions': {
                'L': self.parameters.L,
                'B': self.parameters.B,
                'aspect_ratio': self.parameters.aspect_ratio,
                'height': self.parameters.total_height,
                'footprint_area': self.parameters.footprint_area
            },
            'mesh': {
                'nx': self.parameters.nx,
                'ny': self.parameters.ny,
                'num_floors': self.parameters.num_floors
            },
            'counts': {
                'nodes': len(self.geometry.nodes),
                'elements': len(self.geometry.elements),
                'sections': len(self.sections.sections),
                'loads': len(self.loads.loads)
            },
            'analyses': {
                'enabled': self.analysis_config.enabled_analyses,
                'count': self.analysis_config.get_enabled_count()
            }
        }
