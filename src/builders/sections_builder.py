"""
Sections builder for creating structural sections and transformations.

This builder is responsible for creating sections and geometric transformations.
"""

from typing import Dict, Any, Tuple

try:
    # Try relative imports first (when used as module)
    from ..domain.sections import Sections, Section
except ImportError:
    # Fall back to absolute imports (when run directly)
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from domain.sections import Sections, Section


class SectionsBuilder:
    """Construye las secciones y transformaciones del modelo."""
    
    @staticmethod
    def create(fixed_params: Dict[str, Any]) -> Sections:
        """
        Create sections and transformations for the structural model.
        
        Args:
            fixed_params: Dictionary containing fixed model parameters
            
        Returns:
            Sections object containing all sections and transformations
        """
        # Create sections
        sections = SectionsBuilder._create_sections(fixed_params)
        
        # Create geometric transformations
        transformations = SectionsBuilder._create_transformations()
        
        return Sections(
            sections=sections,
            transformations=transformations
        )
    
    @staticmethod
    def _create_sections(fixed_params: Dict[str, Any]) -> Dict[int, Section]:
        """
        Create all sections for the model.
        
        Args:
            fixed_params: Dictionary containing fixed model parameters
            
        Returns:
            Dictionary of sections keyed by section tag
        """
        sections = {}
        
        # Section 1: Slab (ElasticMembranePlateSection)
        sections[1] = Section(
            tag=1,
            section_type='ElasticMembranePlateSection',
            properties={},
            element_type='slab',
            thickness=fixed_params.get('slab_thickness', 0.10)
        )
        
        # Section 2: Column (Elastic)
        sections[2] = Section(
            tag=2,
            section_type='Elastic',
            properties={},
            element_type='column',
            size=fixed_params.get('column_size', (0.40, 0.40)),
            transf_tag=4  # Transformation tag for columns
        )
        
        # Section 3: Beam (Elastic)
        sections[3] = Section(
            tag=3,
            section_type='Elastic',
            properties={},
            element_type='beam',
            size=fixed_params.get('beam_size', (0.25, 0.40)),
            transf_tag=5  # Transformation tag for beams
        )
        
        return sections
    
    @staticmethod
    def _create_transformations() -> Dict[int, Dict[str, Any]]:
        """
        Create geometric transformations for frame elements.
        
        Returns:
            Dictionary of transformations keyed by transformation tag
        """
        transformations = {}
        
        # Transformation 4: For columns (Linear with Y as vertical axis)
        transformations[4] = {
            'type': 'Linear',
            'vecxz': [0, 1, 0]  # Y axis as the reference vector
        }
        
        # Transformation 5: For beams (Linear with Z as vertical axis)
        transformations[5] = {
            'type': 'Linear',
            'vecxz': [0, 0, 1]  # Z axis as the reference vector
        }
        
        return transformations
    
    @staticmethod
    def create_custom_section(tag: int, section_type: str, element_type: str, 
                             **kwargs) -> Section:
        """
        Create a custom section with specified parameters.
        
        Args:
            tag: Section tag
            section_type: Type of section
            element_type: Type of element this section is for
            **kwargs: Additional section properties
            
        Returns:
            Section object
        """
        return Section(
            tag=tag,
            section_type=section_type,
            properties=kwargs.get('properties', {}),
            element_type=element_type,
            size=kwargs.get('size'),
            thickness=kwargs.get('thickness'),
            transf_tag=kwargs.get('transf_tag')
        )
