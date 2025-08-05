"""
AnalysisEngine - Motor de análisis refactorizado.

Este motor de análisis sigue los principios de Single Responsibility y 
trabaja con objetos de dominio tipados en lugar de diccionarios.
Responsabilidad única: Ejecutar análisis OpenSees.
"""

import os
import time
from typing import Union
from datetime import datetime

from .domain.structural_model import StructuralModel
from .domain.analysis_results import AnalysisResults
# from .utils.analysis_types import StaticAnalysis, ModalAnalysis, DynamicAnalysis
# ✅ REMOVIDO: VisualizationHelper - ahora es postprocesamiento


class AnalysisEngine:
    """Motor de análisis puro - solo ejecuta análisis OpenSees."""
    
    def __init__(self):
        """Inicializa el motor de análisis."""
        # Sin dependencias de directorios, archivos o visualización
        pass
    
    def analyze_model(self, model: Union[StructuralModel, str]) -> AnalysisResults:
        """
        Analiza un modelo estructural y devuelve resultados.
        Acepta tanto objetos StructuralModel como archivos JSON con detección automática.
        
        Args:
            model: Modelo estructural (objeto StructuralModel) o ruta a archivo JSON
            
        Returns:
            Resultados del análisis tipados
        """
        start_time = time.time()
        
        try:
            # 1. Normalizar entrada a StructuralModel
            structural_model = self._normalize_input(model)
            
            # 2. Construir modelo en OpenSees (delegado al modelo)
            build_info = structural_model.build_opensees_model()
            
            if not build_info.get('model_built', False):
                raise RuntimeError(f"Failed to build model in OpenSees: {build_info.get('error', 'Unknown error')}")
            
            # 3. Ejecutar análisis según configuración usando clases especializadas
            static_results, modal_results, dynamic_results = self._execute_analyses(structural_model)
            
            # 4. Construir y devolver resultados tipados
            total_time = time.time() - start_time
            
            return AnalysisResults(
                model_name=structural_model.name,
                static_results=static_results,
                modal_results=modal_results,
                dynamic_results=dynamic_results,
                timestamp=datetime.now().isoformat(),
                success=True,
                errors=[],
                total_analysis_time=total_time
            )
            
        except Exception as e:
            # Manejo robusto de errores
            model_name = self._extract_model_name(model)
            total_time = time.time() - start_time
            
            return AnalysisResults(
                model_name=model_name,
                static_results=None,
                modal_results=None,
                dynamic_results=None,
                timestamp=datetime.now().isoformat(),
                success=False,
                errors=[str(e)],
                total_analysis_time=total_time
            )
    
    def _normalize_input(self, model: Union[StructuralModel, str]) -> StructuralModel:
        """Convierte entrada a StructuralModel, independientemente del tipo."""
        if isinstance(model, StructuralModel):
            return model
        elif isinstance(model, str):
            return StructuralModel.load(model)
        else:
            raise ValueError(f"Tipo de modelo no soportado: {type(model)}")
    
    def _extract_model_name(self, model: Union[StructuralModel, str]) -> str:
        """Extrae nombre del modelo para manejo de errores."""
        try:
            if isinstance(model, StructuralModel):
                return model.name
            elif isinstance(model, str):
                return os.path.basename(model).replace('.json', '')
            else:
                return "UNKNOWN_MODEL"
        except:
            return "UNKNOWN_MODEL"
    
    def _execute_analyses(self, model: StructuralModel) -> tuple:
        """
        Ejecuta los análisis habilitados - ANÁLISIS PURO SIN VISUALIZACIÓN.
        
        Args:
            model: Modelo estructural tipado
            
        Returns:
            Tupla con (static_results, modal_results, dynamic_results)
        """
        enabled = model.analysis_config.enabled_analyses
        
        print(f"🔢 Ejecutando análisis numérico puro para modelo: {model.name}")
        print(f"   Análisis habilitados: {enabled}")
        
        # Inicializar resultados
        static_results = None
        modal_results = None
        dynamic_results = None
        
        # Análisis estático - PURO
        if 'static' in enabled:
            print("  🔧 Ejecutando análisis estático...")
            try:
                # static_analysis = StaticAnalysis(model)
                # static_results = static_analysis.run()  # ✅ SIN viz_helper
                static_results = None  # Placeholder temporal
                print("    ⚠️ Análisis estático temporalmente deshabilitado")
            except Exception as e:
                print(f"    ❌ Error en análisis estático: {str(e)}")
        
        # Análisis modal - PURO
        if 'modal' in enabled:
            print("  🔧 Ejecutando análisis modal...")
            try:
                # modal_analysis = ModalAnalysis(model)
                # modal_results = modal_analysis.run()  # ✅ SIN viz_helper
                modal_results = None  # Placeholder temporal
                print("    ⚠️ Análisis modal temporalmente deshabilitado")
            except Exception as e:
                print(f"    ❌ Error en análisis modal: {str(e)}")
        
        # Análisis dinámico - PURO
        if 'dynamic' in enabled:
            print("  🔧 Ejecutando análisis dinámico...")
            try:
                # dynamic_analysis = DynamicAnalysis(model)
                # dynamic_results = dynamic_analysis.run()  # ✅ SIN viz_helper
                dynamic_results = None  # Placeholder temporal
                print("    ⚠️ Análisis dinámico temporalmente deshabilitado")
            except Exception as e:
                print(f"    ❌ Error en análisis dinámico: {str(e)}")
        
        print(f"✅ Análisis numérico completado para: {model.name}")
        
        return static_results, modal_results, dynamic_results
