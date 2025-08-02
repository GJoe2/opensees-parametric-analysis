"""
Análisis específicos para OpenSees.
Separa cada tipo de análisis en su propia clase para mejor mantenimiento.
"""

import openseespy.opensees as ops
import numpy as np
from typing import Dict, List
from .visualization_helper import VisualizationHelper


class BaseAnalysis:
    """Clase base para todos los análisis."""
    
    def __init__(self, model_data: Dict):
        """
        Inicializa el análisis base.
        
        Args:
            model_data: Datos del modelo cargado
        """
        self.model_data = model_data
        self.model_name = model_data['name']
        
    def setup_opensees_analysis(self, config: Dict):
        """
        Configura OpenSees para el análisis.
        
        Args:
            config: Configuración del análisis
        """
        ops.system(config['system'])
        ops.numberer(config['numberer'])
        ops.constraints(config['constraints'])
        ops.algorithm(config['algorithm'])
        ops.analysis(config['analysis'])
        
    def get_max_displacement(self) -> float:
        """Obtiene el desplazamiento máximo del modelo."""
        max_disp = 0.0
        
        for node_tag, node_info in self.model_data['nodes'].items():
            if node_info['floor'] > 0:  # Solo nodos superiores a la base
                disp = ops.nodeDisp(int(node_tag))
                disp_magnitude = np.sqrt(disp[0]**2 + disp[1]**2 + disp[2]**2)
                max_disp = max(max_disp, disp_magnitude)
        
        return max_disp


class StaticAnalysis(BaseAnalysis):
    """Análisis estático."""
    
    def run(self, viz_helper: VisualizationHelper = None) -> Dict:
        """
        Ejecuta el análisis estático.
        
        Args:
            viz_helper: Helper de visualización (opcional)
            
        Returns:
            Diccionario con resultados del análisis
        """
        results = {'success': False, 'skipped': False}
        
        try:
            config = self.model_data['analysis_config']['static']
            viz_config = self.model_data['analysis_config'].get('visualization', {})
            
            # Configurar análisis
            self.setup_opensees_analysis(config)
            ops.integrator(config['integrator'], 1.0 / config['steps'])
            
            # Crear ODB solo si necesitamos visualización
            odb_available = False
            if viz_helper and viz_config.get('enabled', False) and viz_config.get('static_deformed', False):
                odb_available = viz_helper.create_odb_if_needed()
            
            # Ejecutar análisis
            analysis_success = self._execute_analysis_steps(config['steps'], viz_helper if odb_available else None)
            
            # Guardar respuestas si hay ODB
            if odb_available and analysis_success and viz_helper:
                viz_helper.save_responses()
            
            if analysis_success:
                max_disp = self.get_max_displacement()
                results.update({
                    'success': True,
                    'max_displacement': max_disp,
                    'responses_available': odb_available
                })
                print(f"   ✅ Análisis estático completado - Desplazamiento máx: {max_disp:.6f} m")
            else:
                results.update({
                    'success': False,
                    'error': 'Analysis failed to converge',
                    'responses_available': False
                })
                
        except Exception as e:
            print(f"Error en análisis estático para {self.model_name}: {e}")
            results['error'] = str(e)
            
        return results
    
    def _execute_analysis_steps(self, num_steps: int, viz_helper: VisualizationHelper = None) -> bool:
        """
        Ejecuta los pasos del análisis estático.
        
        Args:
            num_steps: Número de pasos
            viz_helper: Helper de visualización (opcional)
            
        Returns:
            True si el análisis fue exitoso
        """
        for step in range(num_steps):
            try:
                ops.analyze(1)
                
                # Capturar respuesta solo si hay visualización
                if viz_helper:
                    viz_helper.capture_response_step()
                    
            except Exception as e:
                print(f"   ❌ Error en paso {step} del análisis: {e}")
                return False
                
        return True


class ModalAnalysis(BaseAnalysis):
    """Análisis modal."""
    
    def run(self, viz_helper: VisualizationHelper = None) -> Dict:
        """
        Ejecuta el análisis modal.
        
        Args:
            viz_helper: Helper de visualización (opcional)
            
        Returns:
            Diccionario con resultados del análisis
        """
        results = {'success': False, 'skipped': False}
        
        try:
            # Reiniciar estado para análisis modal
            ops.setTime(0.0)
            ops.remove('loadPattern', 1)  # Quitar cargas para análisis modal
            
            config = self.model_data['analysis_config']['modal']
            viz_config = self.model_data['analysis_config'].get('visualization', {})
            num_modes = config['num_modes']
            
            # Crear ODB modal solo si necesitamos visualización
            modal_odb_available = False
            if viz_helper and viz_config.get('enabled', False) and viz_config.get('modal_shapes', False):
                modal_odb_available = viz_helper.create_modal_odb_if_needed()
            
            # Ejecutar análisis de valores propios
            eigen_values = ops.eigen(num_modes)
            
            # Procesar resultados
            frequencies, periods = self._process_eigen_results(eigen_values)
            
            results.update({
                'success': True,
                'frequencies': frequencies,
                'periods': periods,
                'eigen_values': eigen_values if isinstance(eigen_values, list) else eigen_values.tolist(),
                'fundamental_period': periods[0] if periods else None,
                'odb_available': modal_odb_available
            })
            
            period_text = f"{periods[0]:.4f} s" if periods else "N/A"
            print(f"   ✅ Análisis modal completado - Periodo fundamental: {period_text}")
            
        except Exception as e:
            print(f"Error en análisis modal para {self.model_name}: {e}")
            results['error'] = str(e)
            
        return results
    
    def _process_eigen_results(self, eigen_values) -> tuple:
        """
        Procesa los valores propios para obtener frecuencias y periodos.
        
        Args:
            eigen_values: Valores propios del análisis
            
        Returns:
            Tupla con (frecuencias, periodos)
        """
        frequencies = []
        periods = []
        
        for val in eigen_values:
            if val > 1e-6:
                freq = np.sqrt(val) / (2 * np.pi)
                frequencies.append(freq)
                periods.append(1.0 / freq)
                
        return frequencies, periods


class DynamicAnalysis(BaseAnalysis):
    """Análisis dinámico."""
    
    def run(self, viz_helper: VisualizationHelper = None) -> Dict:
        """
        Ejecuta el análisis dinámico.
        
        Args:
            viz_helper: Helper de visualización (opcional)
            
        Returns:
            Diccionario con resultados del análisis
        """
        results = {'success': False, 'skipped': False}
        
        try:
            config = self.model_data['analysis_config']['dynamic']
            
            # Configurar análisis dinámico
            self.setup_opensees_analysis(config)
            
            # Configurar integrador específico para dinámico
            if config['integrator'] == 'Newmark':
                ops.integrator('Newmark', 0.5, 0.25)
            else:
                ops.integrator(config['integrator'])
            
            dt = config['dt']
            num_steps = config['num_steps']
            
            # Ejecutar análisis dinámico
            analysis_success = self._execute_dynamic_analysis(dt, num_steps, viz_helper)
            
            if analysis_success:
                max_disp = self.get_max_displacement()
                results.update({
                    'success': True,
                    'max_displacement': max_disp,
                    'time_steps': num_steps,
                    'dt': dt,
                    'total_time': dt * num_steps
                })
                print(f"   ✅ Análisis dinámico completado - Desplazamiento máx: {max_disp:.6f} m")
            else:
                results.update({
                    'success': False,
                    'error': 'Dynamic analysis failed to converge'
                })
                
        except Exception as e:
            print(f"Error en análisis dinámico para {self.model_name}: {e}")
            results['error'] = str(e)
            
        return results
    
    def _execute_dynamic_analysis(self, dt: float, num_steps: int, 
                                 viz_helper: VisualizationHelper = None) -> bool:
        """
        Ejecuta los pasos del análisis dinámico.
        
        Args:
            dt: Paso de tiempo
            num_steps: Número de pasos
            viz_helper: Helper de visualización (opcional)
            
        Returns:
            True si el análisis fue exitoso
        """
        try:
            # Para análisis dinámico, usualmente se ejecuta en bloques más grandes
            # para mejorar la performance
            block_size = min(100, num_steps)
            
            for start_step in range(0, num_steps, block_size):
                steps_to_run = min(block_size, num_steps - start_step)
                ops.analyze(steps_to_run, dt)
                
                # Capturar respuesta periódicamente si hay visualización
                if viz_helper and start_step % (block_size * 5) == 0:
                    viz_helper.capture_response_step()
                    
            return True
            
        except Exception as e:
            print(f"   ❌ Error en análisis dinámico: {e}")
            return False
