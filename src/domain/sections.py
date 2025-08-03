"""
Section domain objects.

Contains classes for representing structural sections and their properties.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Any


@dataclass
class Section:
    """Represents a structural section."""
    tag: int
    section_type: str  # 'ElasticMembranePlateSection', 'Elastic'
    properties: Dict[str, Any]
    element_type: Optional[str] = None  # 'slab', 'column', 'beam'
    size: Optional[Tuple[float, float]] = None  # (width, height) for beams/columns
    thickness: Optional[float] = None  # for slabs
    transf_tag: Optional[int] = None  # transformation tag for frame elements
    
    def __post_init__(self):
        """Validate section data after initialization."""
        if self.tag <= 0:
            raise ValueError("Section tag must be positive")
        if not self.section_type:
            raise ValueError("Section type cannot be empty")


@dataclass
class Sections:
    """Container for all sections in a model."""
    sections: Dict[int, Section]
    transformations: Dict[int, Dict[str, Any]]
    
    def __post_init__(self):
        """Validate sections data after initialization."""
        if not self.sections:
            raise ValueError("Model must have at least one section")
    
    def get_section_by_tag(self, tag: int) -> Optional[Section]:
        """Get a section by its tag."""
        return self.sections.get(tag)
    
    def get_sections_by_type(self, element_type: str) -> Dict[int, Section]:
        """Get all sections of a specific element type."""
        return {
            tag: section for tag, section in self.sections.items()
            if section.element_type == element_type
        }
    
    def get_transformation(self, tag: int) -> Optional[Dict[str, Any]]:
        """Get a geometric transformation by its tag."""
        return self.transformations.get(tag)
    
    def add_section(self, section: Section) -> None:
        """Add a section to the container."""
        self.sections[section.tag] = section
    
    def add_transformation(self, tag: int, transformation: Dict[str, Any]) -> None:
        """Add a geometric transformation."""
        self.transformations[tag] = transformation
