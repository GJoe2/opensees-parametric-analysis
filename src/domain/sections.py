"""
Section domain objects.

Contains classes for representing structural sections and their properties.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Any, Union


@dataclass
class Section(ABC):
    """Base class for structural sections."""
    tag: int
    section_type: str  # 'ElasticMembranePlateSection', 'Elastic', etc.
    properties: Dict[str, Any]
    element_type: str  # 'slab', 'column', 'beam'
    
    def __post_init__(self):
        """Validate section data after initialization."""
        if self.tag <= 0:
            raise ValueError("Section tag must be positive")
        if not self.section_type:
            raise ValueError("Section type cannot be empty")
        if not self.element_type:
            raise ValueError("Element type cannot be empty")
    
    @abstractmethod
    def to_dict(self) -> dict:
        """Serialize section to dictionary for JSON export."""
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> 'Section':
        """Create section from dictionary (JSON import)."""
        pass


@dataclass
class FrameSection(Section):
    """Section for frame elements (beams and columns)."""
    size: Tuple[float, float]  # (width, height)
    transf_tag: int  # transformation tag for frame elements
    
    def __post_init__(self):
        """Validate frame section data after initialization."""
        super().__post_init__()
        if self.element_type not in ['column', 'beam']:
            raise ValueError("FrameSection element_type must be 'column' or 'beam'")
        if not self.size or len(self.size) != 2:
            raise ValueError("FrameSection must have size as (width, height)")
        if self.transf_tag <= 0:
            raise ValueError("Transformation tag must be positive")
    
    def to_dict(self) -> dict:
        """Serialize frame section to dictionary for JSON export."""
        return {
            'tag': self.tag,
            'section_type': self.section_type,
            'properties': self.properties,
            'element_type': self.element_type,
            'size': list(self.size),
            'transf_tag': self.transf_tag,
            'section_class': 'FrameSection'
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'FrameSection':
        """Create frame section from dictionary (JSON import)."""
        return cls(
            tag=data['tag'],
            section_type=data['section_type'],
            properties=data['properties'],
            element_type=data['element_type'],
            size=tuple(data['size']),
            transf_tag=data['transf_tag']
        )


@dataclass
class ShellSection(Section):
    """Section for shell elements (slabs)."""
    thickness: float  # thickness for shell elements
    
    def __post_init__(self):
        """Validate shell section data after initialization."""
        super().__post_init__()
        if self.element_type != 'slab':
            raise ValueError("ShellSection element_type must be 'slab'")
        if self.thickness <= 0:
            raise ValueError("Thickness must be positive")
    
    def to_dict(self) -> dict:
        """Serialize shell section to dictionary for JSON export."""
        return {
            'tag': self.tag,
            'section_type': self.section_type,
            'properties': self.properties,
            'element_type': self.element_type,
            'thickness': self.thickness,
            'section_class': 'ShellSection'
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ShellSection':
        """Create shell section from dictionary (JSON import)."""
        return cls(
            tag=data['tag'],
            section_type=data['section_type'],
            properties=data['properties'],
            element_type=data['element_type'],
            thickness=data['thickness']
        )


@dataclass
class Sections:
    """Container for all sections in a model."""
    sections: Dict[int, Union[FrameSection, ShellSection]]
    transformations: Dict[int, Dict[str, Any]]
    
    def __post_init__(self):
        """Validate sections data after initialization."""
        if not self.sections:
            raise ValueError("Model must have at least one section")
    
    def get_section_by_tag(self, tag: int) -> Optional[Union[FrameSection, ShellSection]]:
        """Get a section by its tag."""
        return self.sections.get(tag)
    
    def get_sections_by_type(self, element_type: str) -> Dict[int, Union[FrameSection, ShellSection]]:
        """Get all sections of a specific element type."""
        return {
            tag: section for tag, section in self.sections.items()
            if section.element_type == element_type
        }
    
    def get_frame_sections(self) -> Dict[int, FrameSection]:
        """Get all frame sections (beams and columns)."""
        return {
            tag: section for tag, section in self.sections.items()
            if isinstance(section, FrameSection)
        }
    
    def get_shell_sections(self) -> Dict[int, ShellSection]:
        """Get all shell sections (slabs)."""
        return {
            tag: section for tag, section in self.sections.items()
            if isinstance(section, ShellSection)
        }
    
    def get_transformation(self, tag: int) -> Optional[Dict[str, Any]]:
        """Get a geometric transformation by its tag."""
        return self.transformations.get(tag)
    
    def add_section(self, section: Union[FrameSection, ShellSection]) -> None:
        """Add a section to the container."""
        self.sections[section.tag] = section
    
    def add_transformation(self, tag: int, transformation: Dict[str, Any]) -> None:
        """Add a geometric transformation."""
        self.transformations[tag] = transformation
    
    def to_dict(self) -> dict:
        """Serialize sections to dictionary for JSON export."""
        return {
            'sections': {str(k): v.to_dict() for k, v in self.sections.items()},
            'transformations': {str(k): v for k, v in self.transformations.items()}
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Sections':
        """Create sections from dictionary (JSON import)."""
        sections = {}
        for k, v in data['sections'].items():
            section_class = v.get('section_class', 'FrameSection')  # Default for backward compatibility
            if section_class == 'FrameSection':
                sections[int(k)] = FrameSection.from_dict(v)
            elif section_class == 'ShellSection':
                sections[int(k)] = ShellSection.from_dict(v)
            else:
                raise ValueError(f"Unknown section class: {section_class}")
        
        transformations = {int(k): v for k, v in data.get('transformations', {}).items()}
        
        return cls(
            sections=sections,
            transformations=transformations
        )
