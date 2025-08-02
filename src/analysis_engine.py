import os
import json
import openseespy.opensees as ops
import pandas as pd
from typing import Dict, List, Optional
from tqdm import tqdm

from .utils.analysis_types import StaticAnalysis, ModalAnalysis, DynamicAnalysis
from .utils.visualization_helper import VisualizationHelper


class AnalysisEngine:
    """
    Motor de análisis refactorizado - código minimalista y reutilizable.
    Separa claramente análisis numérico de visualización.
    """
    
    def __init__(self, models_dir: str = "models", results_dir: str = "results"):
        """
        Inicializa el motor de análisis.
        
        Args:
            models_dir: Directorio donde están los modelos
            results_dir: Directorio donde se guardarán los resultados
        """
        self.models_dir = models_dir
        self.results_dir = results_dir
        self.ensure_results_dir()
    
    def ensure_results_dir(self):
        """Asegura que el directorio de resultados existe."""
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
    
    def load_model_from_file(self, model_file: str) -> Dict:
        """Carga un modelo desde archivo JSON."""
        with open(model_file, 'r') as f:
            model_data = json.load(f)
        return model_data
    
    def build_model_in_opensees(self, model_data: Dict):
        """Construye el modelo en OpenSees desde los datos cargados."""
        try:
            # Limpiar modelo anterior
            ops.wipe()
            ops.model('basic', '-ndm', 3, '-ndf', 6)
            
            # Crear nodos
            for node_tag, node_info in model_data['nodes'].items():
                x, y, z = node_info['coords']
                ops.node(int(node_tag), x, y, z)
            
            # Crear materiales y secciones
            self._create_sections_and_transforms(model_data)
            
            # Crear elementos
            self._create_elements(model_data)
            
            # Aplicar condiciones de frontera
            self._apply_boundary_conditions(model_data)
            
            # Definir patrón de carga
            ops.timeSeries('Linear', 1)
            ops.pattern('Plain', 1, 1)
            
            # Crear cargas
            self._apply_loads(model_data)
                    
        except Exception as e:
            print(f"Error construyendo modelo en OpenSees: {str(e)}")
            raise
    
    def analyze_model(self, model_file: str) -> Dict:
        """
        Analiza un modelo completo según su configuración.
        
        Args:
            model_file: Ruta al archivo del modelo
            
        Returns:
            Diccionario con todos los resultados
        """
        # Cargar modelo
        model_data = self.load_model_from_file(model_file)
        model_name = model_data['name']
        
        # Validar configuración
        if 'analysis_config' not in model_data:
            raise ValueError(f"El modelo {model_name} no tiene configuración de análisis.")
        
        analysis_config = model_data['analysis_config']
        enabled_analyses = analysis_config.get('enabled_analyses', ['static', 'modal'])
        
        print(f"Analizando modelo: {model_name}")
        print(f"Análisis habilitados: {enabled_analyses}")

        # Construir modelo en OpenSees
        self.build_model_in_opensees(model_data)

        # Configurar helper de visualización si es necesario
        viz_helper = self._setup_visualization_helper(analysis_config)

        # Ejecutar análisis según configuración
        results = self._run_analyses(model_data, enabled_analyses, viz_helper)
        
        # Construir y guardar resultados finales
        analysis_results = self._build_final_results(model_data, results)
        self._save_results(analysis_results, model_name)
        
        # Generar visualizaciones si están habilitadas
        self._generate_visualizations(model_data, analysis_results, viz_helper)
        
        return analysis_results
    
    def _setup_visualization_helper(self, analysis_config: Dict) -> Optional[VisualizationHelper]:
        """Configura helper de visualización si es necesario."""
        viz_config = analysis_config.get('visualization', {})
        
        if not viz_config.get('enabled', False):
            return None
            
        return VisualizationHelper(results_dir=self.results_dir, odb_tag=1)
    
    def _run_analyses(self, model_data: Dict, enabled_analyses: List[str], 
                     viz_helper: Optional[VisualizationHelper]) -> Dict:
        """Ejecuta los análisis habilitados."""
        results = {}
        
        # Análisis estático
        if 'static' in enabled_analyses:
            static_analysis = StaticAnalysis(model_data)
            results['static_analysis'] = static_analysis.run(viz_helper)
        else:
            results['static_analysis'] = {'success': False, 'skipped': True}

        # Análisis modal
        if 'modal' in enabled_analyses:
            modal_analysis = ModalAnalysis(model_data)
            results['modal_analysis'] = modal_analysis.run(viz_helper)
        else:
            results['modal_analysis'] = {'success': False, 'skipped': True}
            
        # Análisis dinámico
        if 'dynamic' in enabled_analyses:
            dynamic_analysis = DynamicAnalysis(model_data)
            results['dynamic_analysis'] = dynamic_analysis.run(viz_helper)
        else:
            results['dynamic_analysis'] = {'success': False, 'skipped': True}
        
        return results
    
    def _build_final_results(self, model_data: Dict, analysis_results: Dict) -> Dict:
        """Construye el diccionario final de resultados."""
        return {
            'model_name': model_data['name'],
            'model_parameters': model_data['parameters'],
            'analysis_config_used': model_data['analysis_config'],
            **analysis_results,  # static_analysis, modal_analysis, dynamic_analysis
            'timestamp': pd.Timestamp.now().isoformat()
        }
    
    def _save_results(self, analysis_results: Dict, model_name: str):
        """Guarda los resultados en archivo JSON."""
        results_file = os.path.join(self.results_dir, f"{model_name}_results.json")
        with open(results_file, 'w') as f:
            json.dump(analysis_results, f, indent=2, default=str)
    
    def _generate_visualizations(self, model_data: Dict, analysis_results: Dict, 
                               viz_helper: Optional[VisualizationHelper]):
        """Genera visualizaciones si están habilitadas."""
        if viz_helper is None:
            print("   ⏭️  Visualización deshabilitada")
            return
        
        viz_config = model_data['analysis_config'].get('visualization', {})
        model_name = model_data['name']
        generated_files = []
        
        # Visualización estática
        if analysis_results.get('static_analysis', {}).get('success', False):
            static_files = viz_helper.generate_static_visualization(model_name, viz_config)
            generated_files.extend(static_files)
        
        # Visualizaciones modales
        modal_results = analysis_results.get('modal_analysis', {})
        if modal_results.get('success', False):
            periods = modal_results.get('periods', [])
            modal_files = viz_helper.generate_modal_visualizations(model_name, viz_config, periods)
            generated_files.extend(modal_files)
        
        # Modelo no deformado
        undeformed_files = viz_helper.generate_undeformed_visualization(model_name, viz_config)
        generated_files.extend(undeformed_files)
        
        # Agregar archivos a resultados
        analysis_results['visualization_files'] = generated_files
        print(f"   📋 Total de archivos de visualización: {len(generated_files)}")
        
        # Limpiar recursos
        viz_helper.cleanup()
    
    # --- Métodos de construcción del modelo (sin cambios significativos) ---
    
    def _create_sections_and_transforms(self, model_data: Dict):
        """Crea secciones y transformaciones geométricas."""
        params = model_data['parameters']
        E = params['E']
        nu = params['nu']
        G = E / (2 * (1 + nu))

        # Crear secciones
        for sec_tag, sec_info in model_data['sections'].items():
            tag = int(sec_tag)
            if sec_info['type'] == 'ElasticMembranePlateSection':
                thickness = sec_info['thickness']
                rho = params['rho']
                ops.section('ElasticMembranePlateSection', tag, E, nu, thickness, rho)
            
            elif sec_info['type'] == 'Elastic':
                size = sec_info['size']
                w, h = size[0], size[1]
                A = w * h
                Iz = w * h**3 / 12
                Iy = h * w**3 / 12
                a, b = max(w, h), min(w, h)
                J = a * b**3 * (1/3 - 0.21 * (b/a) * (1 - (b**4)/(12*a**4)))
                ops.section('Elastic', tag, E, A, Iz, Iy, G, J)

        # Crear transformaciones geométricas
        for transf_tag, transf_info in model_data['transformations'].items():
            tag = int(transf_tag)
            if transf_info['type'] == 'Linear':
                vecxz = transf_info['vecxz']
                ops.geomTransf('Linear', tag, *vecxz)
    
    def _create_elements(self, model_data: Dict):
        """Crea elementos del modelo."""
        for elem_tag, elem_info in model_data['elements'].items():
            nodes = [int(n) for n in elem_info['nodes']]
            elem_type = elem_info['type']
            
            if elem_type == 'slab':
                section_tag = elem_info['section_tag']
                ops.element('ShellMITC4', int(elem_tag), *nodes, section_tag)
            elif elem_type in ['column', 'beam_x', 'beam_y']:
                section_tag = elem_info['section_tag']
                section_info = model_data['sections'][str(section_tag)]
                transf_tag = section_info['transf_tag']
                ops.element('elasticBeamColumn', int(elem_tag), *nodes, int(section_tag), int(transf_tag))
    
    def _apply_boundary_conditions(self, model_data: Dict):
        """Aplica condiciones de frontera."""
        for node_tag, node_info in model_data['nodes'].items():
            if node_info['floor'] == 0:  # Nodos de la base
                ops.fix(int(node_tag), 1, 1, 1, 1, 1, 1)
    
    def _apply_loads(self, model_data: Dict):
        """Aplica cargas al modelo."""
        for node_tag, load_info in model_data['loads'].items():
            if load_info['direction'] == 'Z':
                ops.load(int(node_tag), 0.0, 0.0, float(load_info['value']), 0.0, 0.0, 0.0)
    
    # --- Métodos de conveniencia ---
    
    def analyze_multiple_models(self, model_files: List[str]) -> List[Dict]:
        """Analiza múltiples modelos."""
        results = []
        
        for model_file in tqdm(model_files, desc="Analizando modelos"):
            try:
                result = self.analyze_model(model_file)
                results.append(result)
            except Exception as e:
                print(f"Error analizando {model_file}: {e}")
        
        return results
    
    def get_model_files(self) -> List[str]:
        """Obtiene lista de archivos de modelos en el directorio."""
        model_files = []
        if os.path.exists(self.models_dir):
            for file in os.listdir(self.models_dir):
                if file.endswith('.json'):
                    model_files.append(os.path.join(self.models_dir, file))
        return model_files
