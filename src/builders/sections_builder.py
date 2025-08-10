"""
Sections builder for creating structural sections and transformations.

This builder is responsible for creating sections and geometric transformations.
"""

from typing import Dict, Any, Tuple

from ..domain.sections import Sections, FrameSection, ShellSection


class SectionsBuilder:
    """Construye las secciones y transformaciones del modelo."""
    
    @staticmethod
    def create(fixed_params: Dict[str, Any], material=None) -> Sections:
        """
        Create sections and transformations for the structural model.
        
        Args:
            fixed_params: Dictionary containing fixed model parameters
            material: Material object with properties (optional for backward compatibility)
            
        Returns:
            Sections object containing all sections and transformations
        """
        # Create sections
        sections = SectionsBuilder._create_sections(fixed_params, material)
        
        # Create geometric transformations
        transformations = SectionsBuilder._create_transformations()
        
        return Sections(
            sections=sections,
            transformations=transformations
        )
    
    @staticmethod
    def _create_sections(fixed_params: Dict[str, Any], material=None) -> Dict[int, Any]:
        """
        Create all sections for the model.
        
        Args:
            fixed_params: Dictionary containing fixed model parameters
            material: Material object with properties (optional)
            
        Returns:
            Dictionary of sections keyed by section tag
        """
        sections = {}
        
        # Get material name for reference (if material is provided)
        material_name = material.name if material else None
        
        # Section 1: Slab (ElasticMembranePlateSection)
        sections[1] = ShellSection(
            tag=1,
            section_type='ElasticMembranePlateSection',
            properties={'material_name': material_name} if material_name else {},
            element_type='slab',
            thickness=fixed_params.get('slab_thickness', 0.10)
        )
        
        # Section 2: Column (Elastic)
        sections[2] = FrameSection(
            tag=2,
            section_type='Elastic',
            properties={'material_name': material_name} if material_name else {},
            element_type='column',
            size=fixed_params.get('column_size', (0.40, 0.40)),
            transf_tag=4  # Transformation tag for columns
        )
        
        # Section 3: Beam (Elastic)
        sections[3] = FrameSection(
            tag=3,
            section_type='Elastic',
            properties={'material_name': material_name} if material_name else {},
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
                             **kwargs):
        """
        Create a custom section with specified parameters.
        
        Args:
            tag: Section tag
            section_type: Type of section
            element_type: Type of element this section is for
            **kwargs: Additional section properties
            
        Returns:
            FrameSection or ShellSection object depending on element_type
        """
        properties = kwargs.get('properties', {})
        
        if element_type == 'slab':
            if 'thickness' not in kwargs:
                raise ValueError("ShellSection requires 'thickness' parameter")
            return ShellSection(
                tag=tag,
                section_type=section_type,
                properties=properties,
                element_type=element_type,
                thickness=kwargs['thickness']
            )
        elif element_type in ['column', 'beam']:
            if 'size' not in kwargs or 'transf_tag' not in kwargs:
                raise ValueError("FrameSection requires 'size' and 'transf_tag' parameters")
            return FrameSection(
                tag=tag,
                section_type=section_type,
                properties=properties,
                element_type=element_type,
                size=kwargs['size'],
                transf_tag=kwargs['transf_tag']
            )
        else:
            raise ValueError(f"Unknown element_type: {element_type}. Must be 'slab', 'column', or 'beam'.")
