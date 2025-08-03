"""
Structural model domain object.

Contains the main domain object that represents a complete structural model.
"""

import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, Any

try:
    # Try relative imports first (when used as module)
    from .geometry import Geometry
    from .sections import Sections
    from .loads import Loads
    from .analysis_config import AnalysisConfig
except ImportError:
    # Fall back to absolute imports (when run directly)
    from geometry import Geometry
    from sections import Sections
    from loads import Loads
    from analysis_config import AnalysisConfig


@dataclass
class StructuralModel:
    """Represents a complete structural model."""
    geometry: Geometry
    sections: Sections
    loads: Loads
    analysis_config: AnalysisConfig
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
        # Convert nodes to serializable format
        nodes_dict = {}
        for tag, node in self.geometry.nodes.items():
            nodes_dict[tag] = {
                'coords': node.coords,
                'floor': node.floor,
                'grid_pos': node.grid_pos
            }
        
        # Convert elements to serializable format
        elements_dict = {}
        for tag, element in self.geometry.elements.items():
            elements_dict[tag] = {
                'type': element.element_type,
                'nodes': element.nodes,
                'floor': element.floor,
                'section_tag': element.section_tag
            }
        
        # Convert sections to serializable format
        sections_dict = {}
        for tag, section in self.sections.sections.items():
            section_data = {
                'type': section.section_type,
                **section.properties
            }
            if section.element_type:
                section_data['element_type'] = section.element_type
            if section.size:
                section_data['size'] = section.size
            if section.thickness:
                section_data['thickness'] = section.thickness
            if section.transf_tag:
                section_data['transf_tag'] = section.transf_tag
            sections_dict[tag] = section_data
        
        # Convert loads to serializable format
        loads_dict = {}
        for node_tag, load in self.loads.loads.items():
            loads_dict[node_tag] = {
                'type': load.load_type,
                'value': load.value,
                'direction': load.direction
            }
            if load.load_case:
                loads_dict[node_tag]['load_case'] = load.load_case
        
        # Convert analysis config to serializable format
        analysis_dict = {
            'enabled_analyses': self.analysis_config.enabled_analyses
        }
        
        # Add visualization config
        if self.analysis_config.visualization_config:
            analysis_dict['visualization'] = asdict(self.analysis_config.visualization_config)
        
        # Add specific analysis configs
        if self.analysis_config.static_config:
            analysis_dict['static'] = asdict(self.analysis_config.static_config)
        
        if self.analysis_config.modal_config:
            analysis_dict['modal'] = asdict(self.analysis_config.modal_config)
        
        if self.analysis_config.dynamic_config:
            analysis_dict['dynamic'] = asdict(self.analysis_config.dynamic_config)
        
        return {
            'name': self.name,
            'parameters': {
                'L_B_ratio': self.geometry.get_aspect_ratio(),
                'nx': self.geometry.nx,
                'ny': self.geometry.ny,
                'L': self.geometry.L,
                'B': self.geometry.B,
                'num_floors': self.geometry.num_floors,
                'floor_height': self.geometry.floor_height
            },
            'nodes': nodes_dict,
            'elements': elements_dict,
            'sections': sections_dict,
            'transformations': self.sections.transformations,
            'loads': loads_dict,
            'analysis_config': analysis_dict
        }
    
    def save(self, filepath: str) -> None:
        """
        Save the model to a JSON file.
        
        Args:
            filepath: Path where to save the model file
        """
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
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
        
        # This is a placeholder - full implementation would require
        # reconstructing all domain objects from the JSON data
        # For now, this shows the intended interface
        raise NotImplementedError("Model loading from JSON will be implemented in a future version")
    
    def get_model_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the model's key characteristics.
        
        Returns:
            Dictionary with model summary information
        """
        return {
            'name': self.name,
            'dimensions': {
                'L': self.geometry.L,
                'B': self.geometry.B,
                'aspect_ratio': self.geometry.get_aspect_ratio(),
                'height': self.geometry.get_total_height(),
                'footprint_area': self.geometry.get_footprint_area()
            },
            'mesh': {
                'nx': self.geometry.nx,
                'ny': self.geometry.ny,
                'num_floors': self.geometry.num_floors
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
