"""
MaterialBuilder - Constructor para materiales estructurales.

Crea objetos Material con diferentes configuraciones y parámetros.
"""

from typing import Dict, Any

try:
    # Try relative imports first (when used as module)
    from ..domain.material import Material
except ImportError:
    # Fall back to absolute imports (when run directly)
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from domain.material import Material


class MaterialBuilder:
    """Constructor especializado para materiales."""
    
    @staticmethod
    def create(material_params: Dict[str, Any]) -> Material:
        """
        Crea un objeto Material desde parámetros.
        
        Args:
            material_params: Diccionario con propiedades del material
            
        Returns:
            Objeto Material configurado
        """
        # Extraer parámetros con valores por defecto
        material_type = material_params.get('type', 'concrete')
        
        if material_type == 'concrete':
            return MaterialBuilder._create_concrete(material_params)
        elif material_type == 'steel':
            return MaterialBuilder._create_steel(material_params)
        else:
            return MaterialBuilder._create_custom(material_params)
    
    @staticmethod
    def _create_concrete(params: Dict[str, Any]) -> Material:
        """Crea material de concreto."""
        # Si se especifica resistencia, usar fórmula ACI
        if 'fc' in params:
            fc = params['fc']
            E = 15000 * (fc**0.5) * 0.001 / 0.01**2
        else:
            E = params.get('E', 15000 * 210**0.5 * 0.001 / 0.01**2)
        
        return Material(
            E=E,
            nu=params.get('nu', 0.2),
            rho=params.get('rho', (2.4 * 1.0 / 1.0**3) / 9.81),
            fc=params.get('fc'),
            name=params.get('name', 'concrete_default')
        )
    
    @staticmethod
    def _create_steel(params: Dict[str, Any]) -> Material:
        """Crea material de acero."""
        return Material(
            E=params.get('E', 2040000),
            nu=params.get('nu', 0.3),
            rho=params.get('rho', 7.85 / 9.81),
            fy=params.get('fy', 2530),
            name=params.get('name', 'steel_default')
        )
    
    @staticmethod
    def _create_custom(params: Dict[str, Any]) -> Material:
        """Crea material personalizado."""
        return Material(
            E=params['E'],
            nu=params['nu'], 
            rho=params['rho'],
            fc=params.get('fc'),
            fy=params.get('fy'),
            name=params.get('name', 'custom_material')
        )
