"""
OpenSeesModelBuilder - Construye modelos StructuralModel en OpenSees.

Este módulo es responsable de tomar un objeto StructuralModel y construir
el modelo correspondiente en OpenSees, separando esta responsabilidad
del AnalysisEngine.
"""

import openseespy.opensees as ops
from typing import Dict, Any
import numpy as np


class OpenSeesModelBuilder:
    """Construye modelos StructuralModel en OpenSees."""
    
    @staticmethod
    def build_in_opensees(structural_model) -> None:
        """
        Construye el modelo en OpenSees desde un objeto StructuralModel.
        
        Args:
            structural_model: Objeto StructuralModel completo
        """
        try:
            # Limpiar modelo anterior
            ops.wipe()
            ops.model('basic', '-ndm', 3, '-ndf', 6)
            
            # Obtener datos del modelo estructural
            model_data = structural_model.to_opensees_dict()
            
            # Construir componentes en orden
            OpenSeesModelBuilder._create_nodes(model_data)
            OpenSeesModelBuilder._create_materials_and_sections(model_data)
            OpenSeesModelBuilder._create_transformations(model_data)
            OpenSeesModelBuilder._create_elements(model_data)
            OpenSeesModelBuilder._apply_boundary_conditions(model_data)
            OpenSeesModelBuilder._create_load_pattern(model_data)
            
        except Exception as e:
            raise RuntimeError(f"Error construyendo modelo en OpenSees: {str(e)}")
    
    @staticmethod
    def _create_nodes(model_data: Dict[str, Any]) -> None:
        """Crea nodos en OpenSees."""
        for node_tag, node_info in model_data['nodes'].items():
            x, y, z = node_info['coords']
            ops.node(int(node_tag), x, y, z)
    
    @staticmethod
    def _create_materials_and_sections(model_data: Dict[str, Any]) -> None:
        """Crea materiales y secciones en OpenSees."""
        params = model_data['parameters']
        E = params['E']
        nu = params['nu']
        rho = params['rho']
        G = E / (2 * (1 + nu))
        
        # Crear secciones
        for sec_tag, sec_info in model_data['sections'].items():
            tag = int(sec_tag)
            section_type = sec_info['type']
            
            if section_type == 'ElasticMembranePlateSection':
                thickness = sec_info['thickness']
                ops.section('ElasticMembranePlateSection', tag, E, nu, thickness, rho)
            
            elif section_type == 'Elastic':
                size = sec_info['size']
                w, h = size[0], size[1]
                
                # Calcular propiedades geométricas
                A = w * h
                Iz = w * h**3 / 12
                Iy = h * w**3 / 12
                
                # Calcular momento torsional (aproximación rectangular)
                a, b = max(w, h), min(w, h)
                J = a * b**3 * (1/3 - 0.21 * (b/a) * (1 - (b**4)/(12*a**4)))
                
                ops.section('Elastic', tag, E, A, Iz, Iy, G, J)
    
    @staticmethod
    def _create_transformations(model_data: Dict[str, Any]) -> None:
        """Crea transformaciones geométricas en OpenSees."""
        for transf_tag, transf_info in model_data['transformations'].items():
            tag = int(transf_tag)
            transf_type = transf_info['type']
            
            if transf_type == 'Linear':
                vecxz = transf_info['vecxz']
                ops.geomTransf('Linear', tag, *vecxz)
    
    @staticmethod
    def _create_elements(model_data: Dict[str, Any]) -> None:
        """Crea elementos en OpenSees."""
        for elem_tag, elem_info in model_data['elements'].items():
            nodes = [int(n) for n in elem_info['nodes']]
            elem_type = elem_info['type']
            section_tag = elem_info['section_tag']
            
            if elem_type == 'slab':
                # Elemento de losa (shell)
                ops.element('ShellMITC4', int(elem_tag), *nodes, section_tag)
            
            elif elem_type in ['column', 'beam_x', 'beam_y']:
                # Elementos de viga/columna
                section_info = model_data['sections'][str(section_tag)]
                transf_tag = section_info['transf_tag']
                ops.element('elasticBeamColumn', int(elem_tag), *nodes, 
                          int(section_tag), int(transf_tag))
    
    @staticmethod
    def _apply_boundary_conditions(model_data: Dict[str, Any]) -> None:
        """Aplica condiciones de frontera en OpenSees."""
        for node_tag, node_info in model_data['nodes'].items():
            if node_info['floor'] == 0:  # Nodos de la base
                # Empotrado: restringir todos los grados de libertad
                ops.fix(int(node_tag), 1, 1, 1, 1, 1, 1)
    
    @staticmethod
    def _create_load_pattern(model_data: Dict[str, Any]) -> None:
        """Crea patrón de carga en OpenSees."""
        # Definir serie temporal lineal
        ops.timeSeries('Linear', 1)
        
        # Crear patrón de carga
        ops.pattern('Plain', 1, 1)
        
        # Aplicar cargas nodales
        for node_tag, load_info in model_data['loads'].items():
            if load_info['direction'] == 'Z':
                # Carga vertical
                ops.load(int(node_tag), 0.0, 0.0, float(load_info['value']), 0.0, 0.0, 0.0)
    
    @staticmethod
    def verify_model() -> Dict[str, Any]:
        """
        Verifica que el modelo se haya construido correctamente.
        
        Returns:
            Diccionario con información del modelo construido
        """
        try:
            num_nodes = ops.getNumNodes()
            num_elements = ops.getNumElements()
            
            # Obtener información adicional si está disponible
            model_info = {
                'num_nodes': num_nodes,
                'num_elements': num_elements,
                'model_built': True
            }
            
            # Verificar que el modelo tiene contenido mínimo
            if num_nodes == 0 or num_elements == 0:
                model_info['model_built'] = False
                model_info['warning'] = 'Modelo sin nodos o elementos'
            
            return model_info
            
        except Exception as e:
            return {
                'num_nodes': 0,
                'num_elements': 0,
                'model_built': False,
                'error': str(e)
            }
    
    @staticmethod
    def cleanup() -> None:
        """Limpia el modelo de OpenSees."""
        try:
            ops.wipe()
        except:
            pass  # Si falla la limpieza, continuar


# Función de conveniencia para integración con StructuralModel
def build_structural_model_in_opensees(structural_model) -> Dict[str, Any]:
    """
    Función de conveniencia para construir modelo y verificar.
    
    Args:
        structural_model: Objeto StructuralModel
        
    Returns:
        Información de verificación del modelo construido
    """
    OpenSeesModelBuilder.build_in_opensees(structural_model)
    return OpenSeesModelBuilder.verify_model()
