"""
Helper para manejo de visualizaciones con opstool.
Separa la lógica de visualización del motor de análisis principal.
"""

import os
from typing import Dict, List, Optional
import opstool as opst
import opstool.vis.plotly as opsvis


class VisualizationHelper:
    """
    Clase helper para manejo de visualizaciones con opstool.
    Encapsula toda la lógica específica de opstool y generación de archivos.
    """
    
    def __init__(self, results_dir: str = "results", odb_tag: int = 1):
        """
        Inicializa el helper de visualización.
        
        Args:
            results_dir: Directorio donde guardar archivos
            odb_tag: Tag para la base de datos ODB
        """
        self.results_dir = results_dir
        self.odb_tag = odb_tag
        self._odb = None
        
    def create_odb_if_needed(self) -> bool:
        """
        Crea ODB solo si es necesario para visualizaciones.
        
        Returns:
            True si se creó exitosamente, False en caso contrario
        """
        if self._odb is not None:
            return True
            
        try:
            self._odb = opst.post.CreateODB(
                odb_tag=self.odb_tag,
                project_gauss_to_nodes="extrapolate"
            )
            print(f"   📊 ODB creado (tag={self.odb_tag})")
            return True
        except Exception as e:
            print(f"   ⚠️  Error creando ODB: {e}")
            return False
    
    def capture_response_step(self) -> bool:
        """
        Captura un paso de respuesta si hay ODB disponible.
        
        Returns:
            True si se capturó exitosamente, False en caso contrario
        """
        if self._odb is None:
            return False
            
        try:
            self._odb.fetch_response_step()
            return True
        except Exception as e:
            print(f"   ⚠️  Error capturando respuesta: {e}")
            return False
    
    def save_responses(self) -> bool:
        """
        Guarda las respuestas capturadas.
        
        Returns:
            True si se guardó exitosamente, False en caso contrario
        """
        if self._odb is None:
            return False
            
        try:
            self._odb.save_response_step()
            return True
        except Exception as e:
            print(f"   ⚠️  Error guardando respuestas: {e}")
            return False
    
    def create_modal_odb_if_needed(self) -> bool:
        """
        Crea ODB específico para análisis modal.
        
        Returns:
            True si se creó exitosamente, False en caso contrario
        """
        try:
            modal_odb = opst.post.CreateModeShapeODB(
                odb_tag=self.odb_tag,
                mode_tags="all"
            )
            print(f"   📊 ODB modal creado (tag={self.odb_tag})")
            return True
        except Exception as e:
            print(f"   ⚠️  Error creando ODB modal: {e}")
            return False
    
    def generate_static_visualization(self, model_name: str, viz_config: Dict) -> List[str]:
        """
        Genera visualización de respuesta estática.
        
        Args:
            model_name: Nombre del modelo
            viz_config: Configuración de visualización
            
        Returns:
            Lista de archivos generados
        """
        generated_files = []
        
        if not viz_config.get('static_deformed', False):
            return generated_files
            
        try:
            print(f"   📊 Creando visualización de respuesta estática...")
            export_format = viz_config.get('export_format', 'html')
            
            if export_format == 'html':
                static_file = os.path.join(
                    self.results_dir, 
                    f"{model_name}_static_deformed.html"
                )
                
                opsvis.plot_deformed_shape(
                    odb_tag=self.odb_tag,
                    deform_scale=viz_config.get('deform_scale', 100),
                    show_nodes=viz_config.get('show_nodes', True),
                    line_width=viz_config.get('line_width', 2),
                    save_html=static_file
                )
                
                generated_files.append(static_file)
                print(f"   ✅ Deformada estática: {os.path.basename(static_file)}")
                
        except Exception as e:
            print(f"   ❌ Error en visualización estática: {e}")
            
        return generated_files
    
    def generate_modal_visualizations(self, model_name: str, viz_config: Dict, 
                                    periods: List[float]) -> List[str]:
        """
        Genera visualizaciones de formas modales.
        
        Args:
            model_name: Nombre del modelo
            viz_config: Configuración de visualización
            periods: Lista de periodos modales
            
        Returns:
            Lista de archivos generados
        """
        generated_files = []
        
        if not viz_config.get('modal_shapes', False):
            return generated_files
            
        try:
            print(f"   📊 Creando visualizaciones de formas modales...")
            export_format = viz_config.get('export_format', 'html')
            max_modes = min(len(periods), viz_config.get('max_modes', 6))
            
            if export_format == 'html':
                for mode_num in range(1, max_modes + 1):
                    period = periods[mode_num - 1] if mode_num - 1 < len(periods) else 0
                    mode_file = os.path.join(
                        self.results_dir,
                        f"{model_name}_mode_{mode_num}_T{period:.4f}s.html"
                    )
                    
                    opsvis.plot_eigen_animation(
                        mode_tag=mode_num,
                        odb_tag=self.odb_tag,
                        scale=viz_config.get('deform_scale', 0.5),
                        show_fig=False,
                        save_html=mode_file
                    )
                    
                    generated_files.append(mode_file)
                
                print(f"   ✅ {len(generated_files)} visualizaciones modales generadas")
                
        except Exception as e:
            print(f"   ❌ Error en visualizaciones modales: {e}")
            
        return generated_files
    
    def generate_undeformed_visualization(self, model_name: str, viz_config: Dict) -> List[str]:
        """
        Genera visualización del modelo no deformado.
        
        Args:
            model_name: Nombre del modelo
            viz_config: Configuración de visualización
            
        Returns:
            Lista de archivos generados
        """
        generated_files = []
        
        if not viz_config.get('undeformed', False):
            return generated_files
            
        try:
            print(f"   📊 Creando visualización del modelo no deformado...")
            export_format = viz_config.get('export_format', 'html')
            
            if export_format == 'html':
                import opsvis as opsv
                
                undeformed_file = os.path.join(
                    self.results_dir, 
                    f"{model_name}_undeformed.html"
                )
                
                fig = opsv.plot_model(
                    show_nodes=viz_config.get('show_nodes', True),
                    show_elements=viz_config.get('show_elements', True),
                    node_labels=viz_config.get('node_labels', False),
                    element_labels=viz_config.get('element_labels', False)
                )
                
                fig.write_html(undeformed_file)
                generated_files.append(undeformed_file)
                print(f"   ✅ Modelo no deformado: {os.path.basename(undeformed_file)}")
                
        except Exception as e:
            print(f"   ❌ Error en visualización no deformada: {e}")
            
        return generated_files
    
    def has_odb(self) -> bool:
        """Verifica si hay ODB disponible."""
        return self._odb is not None
    
    def cleanup(self):
        """Limpia recursos."""
        self._odb = None
