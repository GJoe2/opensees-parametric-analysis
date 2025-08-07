"""
Material - Representa las propiedades de materiales estructurales.

Esta clase de dominio encapsula todas las propiedades de materiales
necesarias para el análisis estructural.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class Material:
    """
    Representa las propiedades de un material estructural.
    
    Attributes:
        E: Módulo de elasticidad (tonf/m²)
        nu: Coeficiente de Poisson
        rho: Densidad (tonf·s²/m⁴)
        fc: Resistencia a compresión del concreto (opcional)
        fy: Resistencia de fluencia del acero (opcional)
        name: Nombre identificativo del material
    """
    E: float                    # Módulo de elasticidad
    nu: float                   # Coeficiente de Poisson  
    rho: float                  # Densidad
    fc: Optional[float] = None  # Resistencia compresión concreto
    fy: Optional[float] = None  # Resistencia fluencia acero
    name: str = "concrete_default"
    
    def __post_init__(self):
        """Validación de parámetros después de inicialización."""
        if self.E <= 0:
            raise ValueError("Módulo de elasticidad debe ser positivo")
        if not (0 <= self.nu <= 0.5):
            raise ValueError("Coeficiente de Poisson debe estar entre 0 y 0.5")
        if self.rho <= 0:
            raise ValueError("Densidad debe ser positiva")
    
    @property
    def G(self) -> float:
        """Módulo de cortante calculado."""
        return self.E / (2 * (1 + self.nu))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario para serialización."""
        return {
            'name': self.name,
            'E': self.E,
            'nu': self.nu,
            'rho': self.rho,
            'G': self.G,
            'fc': self.fc,
            'fy': self.fy
        }
    
    @classmethod
    def create_concrete_c210(cls, name: str = "concrete_c210") -> 'Material':
        """Crea material de concreto C210 con propiedades típicas."""
        return cls(
            E=15000 * 210**0.5 * 0.001 / 0.01**2,  # Fórmula ACI
            nu=0.2,
            rho=(2.4 * 1.0 / 1.0**3) / 9.81,
            fc=210.0,  # kg/cm² 
            name=name
        )
    
    @classmethod
    def create_steel_a36(cls, name: str = "steel_a36") -> 'Material':
        """Crea material de acero A36 con propiedades típicas."""
        return cls(
            E=2040000,  # tonf/m²
            nu=0.3,
            rho=7.85 / 9.81,  # tonf·s²/m⁴
            fy=2530,  # tonf/m²
            name=name
        )
    
    @classmethod
    def create_custom(cls, E: float, nu: float, rho: float, 
                     fc: Optional[float] = None, fy: Optional[float] = None,
                     name: str = "custom_material") -> 'Material':
        """Crea material personalizado con parámetros específicos."""
        return cls(
            E=E,
            nu=nu,
            rho=rho,
            fc=fc,
            fy=fy,
            name=name
        )
