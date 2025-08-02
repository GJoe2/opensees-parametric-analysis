"""
Métodos de Conveniencia para ModelBuilder
========================================

Este módulo contiene métodos de conveniencia que simplifican el uso de ModelBuilder
para casos comunes. Estos métodos NO forman parte de la lógica core del ModelBuilder,
sino que son helpers que facilitan su uso.

Casos de uso:
- Análisis solo estático
- Análisis solo modal  
- Análisis dinámico (estático + dinámico)
- Análisis completo (todos los tipos)

Autor: OpenSees Model Builder
Fecha: Agosto 2025
"""

from typing import Dict
import sys
import os

# Agregar el directorio src al path para imports absolutos
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from model_builder import ModelBuilder


class ModelBuilderHelpers:
    """
    Clase que contiene métodos de conveniencia para ModelBuilder.
    Actúa como un wrapper que simplifica casos de uso comunes.
    """
    
    def __init__(self, model_builder: ModelBuilder):
        """
        Inicializa los helpers con una instancia de ModelBuilder.
        
        Args:
            model_builder: Instancia de ModelBuilder a usar
        """
        self.builder = model_builder
    
    def create_static_only_model(self, L_B_ratio: float, B: float, nx: int, ny: int, 
                                model_name: str = None, steps: int = 10, 
                                visualize: bool = False) -> Dict:
        """
        Método de conveniencia para crear modelo solo con análisis estático.
        
        Args:
            L_B_ratio: Relación L/B
            B: Ancho de la estructura en metros
            nx: Número de ejes en dirección X
            ny: Número de ejes en dirección Y
            model_name: Nombre del modelo (opcional)
            steps: Número de pasos del análisis estático
            visualize: Si habilitar visualización de deformada estática
            
        Returns:
            Diccionario con información del modelo creado
        """
        viz_config = {'enabled': visualize, 'static_deformed': visualize} if visualize else {}
        return self.builder.create_model(
            L_B_ratio, B, nx, ny, model_name,
            enabled_analyses=['static'],
            analysis_params={
                'static': {'steps': steps},
                'visualization': viz_config
            }
        )
    
    def create_modal_only_model(self, L_B_ratio: float, B: float, nx: int, ny: int, 
                               model_name: str = None, num_modes: int = 6,
                               visualize: bool = False) -> Dict:
        """
        Método de conveniencia para crear modelo solo con análisis modal.
        
        Args:
            L_B_ratio: Relación L/B
            B: Ancho de la estructura en metros
            nx: Número de ejes en dirección X
            ny: Número de ejes en dirección Y
            model_name: Nombre del modelo (opcional)
            num_modes: Número de modos a extraer
            visualize: Si habilitar visualización de formas modales
            
        Returns:
            Diccionario con información del modelo creado
        """
        viz_config = {'enabled': visualize, 'modal_shapes': visualize} if visualize else {}
        return self.builder.create_model(
            L_B_ratio, B, nx, ny, model_name,
            enabled_analyses=['modal'],
            analysis_params={
                'modal': {'num_modes': num_modes},
                'visualization': viz_config
            }
        )
    
    def create_dynamic_model(self, L_B_ratio: float, B: float, nx: int, ny: int, 
                           model_name: str = None, dt: float = 0.01, num_steps: int = 1000,
                           visualize: bool = False) -> Dict:
        """
        Método de conveniencia para crear modelo con análisis estático y dinámico.
        
        Args:
            L_B_ratio: Relación L/B
            B: Ancho de la estructura en metros
            nx: Número de ejes en dirección X
            ny: Número de ejes en dirección Y
            model_name: Nombre del modelo (opcional)
            dt: Paso de tiempo para análisis dinámico
            num_steps: Número de pasos para análisis dinámico
            visualize: Si habilitar visualización de deformada estática
            
        Returns:
            Diccionario con información del modelo creado
        """
        viz_config = {'enabled': visualize, 'static_deformed': visualize} if visualize else {}
        return self.builder.create_model(
            L_B_ratio, B, nx, ny, model_name,
            enabled_analyses=['static', 'dynamic'],
            analysis_params={
                'dynamic': {'dt': dt, 'num_steps': num_steps},
                'visualization': viz_config
            }
        )
    
    def create_complete_model(self, L_B_ratio: float, B: float, nx: int, ny: int, 
                            model_name: str = None, visualize: bool = False) -> Dict:
        """
        Método de conveniencia para crear modelo con todos los análisis.
        
        Args:
            L_B_ratio: Relación L/B
            B: Ancho de la estructura en metros
            nx: Número de ejes en dirección X
            ny: Número de ejes en dirección Y
            model_name: Nombre del modelo (opcional)
            visualize: Si habilitar visualización completa (estática + modal)
            
        Returns:
            Diccionario con información del modelo creado
        """
        viz_config = {
            'enabled': visualize, 
            'static_deformed': visualize, 
            'modal_shapes': visualize
        } if visualize else {}
        return self.builder.create_model(
            L_B_ratio, B, nx, ny, model_name,
            enabled_analyses=['static', 'modal', 'dynamic'],
            analysis_params={'visualization': viz_config}
        )
    
    def create_research_model(self, L_B_ratio: float, B: float, nx: int, ny: int,
                            model_name: str = None, analysis_type: str = "complete",
                            high_precision: bool = False, visualize: bool = True) -> Dict:
        """
        Método de conveniencia para crear modelos de investigación con configuraciones avanzadas.
        
        Args:
            L_B_ratio: Relación L/B
            B: Ancho de la estructura en metros
            nx: Número de ejes en dirección X
            ny: Número de ejes en dirección Y
            model_name: Nombre del modelo (opcional)
            analysis_type: Tipo de análisis ("static", "modal", "dynamic", "complete")
            high_precision: Si usar configuración de alta precisión
            visualize: Si habilitar visualización
            
        Returns:
            Diccionario con información del modelo creado
        """
        # Configuraciones de alta precisión para investigación
        if high_precision:
            static_config = {
                'steps': 50,
                'integrator': 'DisplacementControl',
                'algorithm': 'NewtonLineSearch'
            }
            modal_config = {
                'num_modes': 30,
                'system': 'UmfPack'
            }
            dynamic_config = {
                'dt': 0.0001,
                'num_steps': 100000,
                'integrator': 'HHT',
                'algorithm': 'ModifiedNewton'
            }
        else:
            static_config = {'steps': 20}
            modal_config = {'num_modes': 12}
            dynamic_config = {'dt': 0.005, 'num_steps': 5000}
        
        # Determinar análisis habilitados
        if analysis_type == "static":
            enabled_analyses = ['static']
            analysis_params = {'static': static_config}
            viz_config = {'enabled': visualize, 'static_deformed': visualize}
        elif analysis_type == "modal":
            enabled_analyses = ['modal']
            analysis_params = {'modal': modal_config}
            viz_config = {'enabled': visualize, 'modal_shapes': visualize}
        elif analysis_type == "dynamic":
            enabled_analyses = ['static', 'dynamic']
            analysis_params = {'static': static_config, 'dynamic': dynamic_config}
            viz_config = {'enabled': visualize, 'static_deformed': visualize}
        else:  # complete
            enabled_analyses = ['static', 'modal', 'dynamic']
            analysis_params = {
                'static': static_config,
                'modal': modal_config, 
                'dynamic': dynamic_config
            }
            viz_config = {
                'enabled': visualize,
                'static_deformed': visualize,
                'modal_shapes': visualize
            }
        
        if visualize:
            analysis_params['visualization'] = viz_config
        
        return self.builder.create_model(
            L_B_ratio, B, nx, ny, model_name,
            enabled_analyses=enabled_analyses,
            analysis_params=analysis_params
        )
    
    def create_quick_test_model(self, L_B_ratio: float = 1.5, B: float = 10.0, 
                              nx: int = 3, ny: int = 3, model_name: str = None) -> Dict:
        """
        Método de conveniencia para crear un modelo de prueba rápida.
        Configurado para análisis rápido sin visualización.
        
        Args:
            L_B_ratio: Relación L/B (por defecto 1.5)
            B: Ancho de la estructura en metros (por defecto 10.0)
            nx: Número de ejes en dirección X (por defecto 3)
            ny: Número de ejes en dirección Y (por defecto 3)
            model_name: Nombre del modelo (opcional)
            
        Returns:
            Diccionario con información del modelo creado
        """
        return self.builder.create_model(
            L_B_ratio, B, nx, ny, model_name,
            enabled_analyses=['static', 'modal'],
            analysis_params={
                'static': {'steps': 5},
                'modal': {'num_modes': 3},
                'visualization': {'enabled': False}
            }
        )


# Función de conveniencia para crear helpers
def create_model_helpers(output_dir: str = "models") -> ModelBuilderHelpers:
    """
    Función de conveniencia para crear ModelBuilderHelpers.
    
    Args:
        output_dir: Directorio donde se guardarán los modelos
        
    Returns:
        Instancia de ModelBuilderHelpers lista para usar
    """
    builder = ModelBuilder(output_dir=output_dir)
    return ModelBuilderHelpers(builder)


# Funciones de conveniencia globales (para compatibilidad)
def create_static_only_model(L_B_ratio: float, B: float, nx: int, ny: int,
                           output_dir: str = "models", **kwargs) -> Dict:
    """Función global de conveniencia para crear modelo estático."""
    helpers = create_model_helpers(output_dir)
    return helpers.create_static_only_model(L_B_ratio, B, nx, ny, **kwargs)


def create_modal_only_model(L_B_ratio: float, B: float, nx: int, ny: int,
                          output_dir: str = "models", **kwargs) -> Dict:
    """Función global de conveniencia para crear modelo modal."""
    helpers = create_model_helpers(output_dir)
    return helpers.create_modal_only_model(L_B_ratio, B, nx, ny, **kwargs)


def create_complete_model(L_B_ratio: float, B: float, nx: int, ny: int,
                        output_dir: str = "models", **kwargs) -> Dict:
    """Función global de conveniencia para crear modelo completo."""
    helpers = create_model_helpers(output_dir)
    return helpers.create_complete_model(L_B_ratio, B, nx, ny, **kwargs)
