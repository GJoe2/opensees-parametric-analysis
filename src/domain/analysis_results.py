"""
Objetos de dominio para resultados de análisis.

Este módulo contiene las clases que representan los resultados de análisis
estructural con OpenSees, proporcionando una interfaz tipada y métodos
de consulta.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple, Any
import json
import pandas as pd
from datetime import datetime


@dataclass
class StaticResults:
    """Resultados específicos del análisis estático."""
    
    max_displacement: float
    max_stress: float
    convergence_achieved: bool
    num_iterations: int
    node_displacements: Dict[int, Tuple[float, float, float]]
    element_forces: Dict[int, Dict[str, float]]
    analysis_time: float
    
    def get_max_displacement_location(self) -> Tuple[int, Tuple[float, float, float]]:
        """Retorna el nodo y desplazamiento máximo."""
        max_node = max(self.node_displacements.items(), 
                      key=lambda x: abs(max(x[1])))
        return max_node
    
    def get_displacement_summary(self) -> Dict[str, float]:
        """Retorna resumen de desplazamientos."""
        displacements = list(self.node_displacements.values())
        max_x = max(abs(d[0]) for d in displacements)
        max_y = max(abs(d[1]) for d in displacements)
        max_z = max(abs(d[2]) for d in displacements)
        
        return {
            'max_x': max_x,
            'max_y': max_y, 
            'max_z': max_z,
            'max_total': max(max_x, max_y, max_z)
        }


@dataclass
class ModalResults:
    """Resultados específicos del análisis modal."""
    
    periods: List[float]
    frequencies: List[float]
    mode_shapes: Dict[int, Dict[int, Tuple[float, float, float]]]
    participation_factors: List[float]
    effective_mass_ratios: List[float]
    analysis_time: float
    
    def get_fundamental_period(self) -> float:
        """Retorna el período fundamental (primer modo)."""
        return self.periods[0] if self.periods else 0.0
    
    def get_period_range(self) -> Tuple[float, float]:
        """Retorna el rango de períodos (min, max)."""
        if not self.periods:
            return (0.0, 0.0)
        return (min(self.periods), max(self.periods))
    
    def get_dominant_modes(self, threshold: float = 0.05) -> List[int]:
        """Retorna modos con factor de participación > threshold."""
        return [i for i, factor in enumerate(self.participation_factors) 
                if abs(factor) > threshold]
    
    def get_cumulative_mass_participation(self) -> List[float]:
        """Retorna participación de masa acumulada."""
        cumulative = []
        total = 0.0
        for ratio in self.effective_mass_ratios:
            total += ratio
            cumulative.append(total)
        return cumulative


@dataclass
class DynamicResults:
    """Resultados específicos del análisis dinámico."""
    
    time_history: List[float]
    max_displacement: float
    max_acceleration: float
    max_velocity: float
    response_spectrum: Optional[Dict[float, float]]
    damping_ratio: float
    analysis_time: float
    converged_steps: int
    total_steps: int
    
    def get_peak_response_time(self) -> float:
        """Retorna el tiempo del pico de respuesta."""
        # Simplificado - en implementación real calcular desde time history
        return self.time_history[len(self.time_history)//2] if self.time_history else 0.0
    
    def get_convergence_ratio(self) -> float:
        """Retorna ratio de convergencia."""
        return self.converged_steps / self.total_steps if self.total_steps > 0 else 0.0
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Retorna resumen del análisis dinámico."""
        return {
            'max_displacement': self.max_displacement,
            'max_acceleration': self.max_acceleration,
            'max_velocity': self.max_velocity,
            'convergence_ratio': self.get_convergence_ratio(),
            'analysis_duration': self.analysis_time,
            'damping_ratio': self.damping_ratio
        }


@dataclass
class AnalysisResults:
    """Contenedor principal de resultados de análisis."""
    
    model_name: str
    static_results: Optional[StaticResults]
    modal_results: Optional[ModalResults]
    dynamic_results: Optional[DynamicResults]
    timestamp: str
    success: bool
    errors: List[str]
    total_analysis_time: float = 0.0
    
    def __post_init__(self):
        """Calcula tiempo total de análisis."""
        total_time = 0.0
        if self.static_results:
            total_time += self.static_results.analysis_time
        if self.modal_results:
            total_time += self.modal_results.analysis_time
        if self.dynamic_results:
            total_time += self.dynamic_results.analysis_time
        self.total_analysis_time = total_time
    
    def get_completed_analyses(self) -> List[str]:
        """Retorna lista de análisis completados exitosamente."""
        completed = []
        if self.static_results:
            completed.append('static')
        if self.modal_results:
            completed.append('modal')
        if self.dynamic_results:
            completed.append('dynamic')
        return completed
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Retorna resumen completo del análisis."""
        summary = {
            'model_name': self.model_name,
            'timestamp': self.timestamp,
            'success': self.success,
            'total_time': self.total_analysis_time,
            'completed_analyses': self.get_completed_analyses(),
            'error_count': len(self.errors)
        }
        
        # Agregar resultados específicos si existen
        if self.static_results:
            summary['static'] = {
                'max_displacement': self.static_results.max_displacement,
                'convergence': self.static_results.convergence_achieved
            }
        
        if self.modal_results:
            summary['modal'] = {
                'fundamental_period': self.modal_results.get_fundamental_period(),
                'num_modes': len(self.modal_results.periods)
            }
        
        if self.dynamic_results:
            summary['dynamic'] = {
                'max_displacement': self.dynamic_results.max_displacement,
                'convergence_ratio': self.dynamic_results.get_convergence_ratio()
            }
        
        return summary
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte resultados a diccionario para serialización."""
        return asdict(self)
    
    def save(self, file_path: str) -> None:
        """Guarda resultados en archivo JSON."""
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2, default=str)
    
    @classmethod
    def load(cls, file_path: str) -> 'AnalysisResults':
        """Carga resultados desde archivo JSON."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Reconstruir objetos anidados
        if data.get('static_results'):
            data['static_results'] = StaticResults(**data['static_results'])
        
        if data.get('modal_results'):
            data['modal_results'] = ModalResults(**data['modal_results'])
        
        if data.get('dynamic_results'):
            data['dynamic_results'] = DynamicResults(**data['dynamic_results'])
        
        return cls(**data)
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convierte resultados a DataFrame para análisis."""
        summary = self.get_analysis_summary()
        return pd.DataFrame([summary])
    
    def has_errors(self) -> bool:
        """Retorna True si hay errores."""
        return len(self.errors) > 0
    
    def get_error_summary(self) -> str:
        """Retorna resumen de errores."""
        if not self.has_errors():
            return "No errors"
        return f"{len(self.errors)} errors: {'; '.join(self.errors[:3])}"


def create_failed_results(model_name: str, errors: List[str]) -> AnalysisResults:
    """Función helper para crear resultados fallidos."""
    return AnalysisResults(
        model_name=model_name,
        static_results=None,
        modal_results=None,
        dynamic_results=None,
        timestamp=datetime.now().isoformat(),
        success=False,
        errors=errors
    )


def create_successful_results(model_name: str, 
                            static_results: Optional[StaticResults] = None,
                            modal_results: Optional[ModalResults] = None,
                            dynamic_results: Optional[DynamicResults] = None) -> AnalysisResults:
    """Función helper para crear resultados exitosos."""
    return AnalysisResults(
        model_name=model_name,
        static_results=static_results,
        modal_results=modal_results,
        dynamic_results=dynamic_results,
        timestamp=datetime.now().isoformat(),
        success=True,
        errors=[]
    )
