import os
import json
from typing import Dict, List, Tuple
import numpy as np

class ModelBuilder:
    """
    Clase constructora de modelos para análisis paramétrico.
    Genera archivos de modelos OpenSees para diferentes combinaciones de parámetros.
    """
    
    def __init__(self, output_dir: str = "models"):
        """
        Inicializa el constructor de modelos.
        
        Args:
            output_dir: Directorio donde se guardarán los modelos
        """
        self.output_dir = output_dir
        self.ensure_output_dir()
        
        # Parámetros fijos del modelo
        self.fixed_params = {
            'column_size': (0.40, 0.40),  # 40x40 cm
            'beam_size': (0.25, 0.40),    # 25x40 cm
            'slab_thickness': 0.10,       # 10 cm
            'num_floors': 2,              # 2 pisos
            'floor_height': 3.0,          # 3 m por piso
            'E': 15000 * 210**0.5 * 0.001 / 0.01**2,  # Módulo de elasticidad en tonf/m²
            'nu': 0.2,                    # Coeficiente de Poisson
            'rho': (2.4 * 1.0 / 1.0**3) / 9.81  # Densidad en tonf·s²/m⁴
        }
    
    def ensure_output_dir(self):
        """Asegura que el directorio de salida existe."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_model_name(self, L_B_ratio: float, B: float, nx: int, ny: int) -> str:
        """
        Genera nombre codificado para el modelo.
        
        Args:
            L_B_ratio: Relación L/B (aspecto)
            B: Ancho de la estructura en metros
            nx: Número de ejes en dirección X
            ny: Número de ejes en dirección Y
            
        Returns:
            Nombre codificado del modelo (ej: F01_45_10_1224)
        """
        # Convertir L/B ratio a formato de 2 dígitos (ej: 1.5 -> 15)
        aspect_code = int(L_B_ratio * 10)
        
        # Convertir B a formato de 2 dígitos (ej: 10.0 -> 10)
        B_code = int(B)
        
        # Combinar nx y ny en formato de 4 dígitos (ej: nx=12, ny=24 -> 1224)
        grid_code = nx * 100 + ny
        
        return f"F01_{aspect_code:02d}_{B_code:02d}_{grid_code:04d}"
    
    def calculate_dimensions(self, L_B_ratio: float, B: float) -> Tuple[float, float]:
        """
        Calcula las dimensiones L y B basadas en la relación L/B.
        
        Args:
            L_B_ratio: Relación L/B
            B: Ancho de la estructura en metros
            
        Returns:
            Tupla con (L, B) en metros
        """
        L = B * L_B_ratio
        return L, B
    
    def create_model(self, L_B_ratio: float, B: float, nx: int, ny: int, 
                    model_name: str = None, 
                    enabled_analyses: List[str] = None,
                    analysis_params: Dict = None) -> Dict:
        """
        Crea un modelo OpenSees y lo guarda en archivo.
        
        Args:
            L_B_ratio: Relación L/B
            B: Ancho de la estructura en metros
            nx: Número de ejes en dirección X
            ny: Número de ejes en dirección Y
            model_name: Nombre del modelo (opcional)
            enabled_analyses: Lista de análisis a habilitar ['static', 'modal', 'dynamic']
                            Si es None, usa ['static', 'modal'] por defecto
            analysis_params: Diccionario con parámetros personalizados para análisis
                           Ej: {'modal': {'num_modes': 10}, 'dynamic': {'dt': 0.005}}
            
        Returns:
            Diccionario con información del modelo creado
        """
        if model_name is None:
            model_name = self.generate_model_name(L_B_ratio, B, nx, ny)
        
        # Configuración por defecto de análisis habilitados
        if enabled_analyses is None:
            enabled_analyses = ['static', 'modal']
        
        # Parámetros por defecto para cada tipo de análisis
        if analysis_params is None:
            analysis_params = {}
        
        # Calcular dimensiones
        L, B = self.calculate_dimensions(L_B_ratio, B)
        
        # Crear nodos
        node_data = self._create_nodes(L, B, nx, ny)
        
        # Crear elementos
        element_data = self._create_elements(nx, ny)
        
        # Crear cargas
        load_data = self._create_loads(node_data)
        
        # Definir secciones y transformaciones
        sections = {
            '1': { # Losa
                'type': 'ElasticMembranePlateSection',
                'thickness': self.fixed_params['slab_thickness']
            },
            '2': { # Columna
                'type': 'Elastic',
                'element_type': 'column',
                'size': self.fixed_params['column_size'],
                'transf_tag': 4  # Tag de la transformación geométrica para columnas
            },
            '3': { # Viga
                'type': 'Elastic',
                'element_type': 'beam',
                'size': self.fixed_params['beam_size'],
                'transf_tag': 5  # Tag de la transformación geométrica para vigas
            }
        }

        transformations = {
            '4': {'type': 'Linear', 'vecxz': [0, 1, 0]}, # Para columnas
            '5': {'type': 'Linear', 'vecxz': [0, 0, 1]}  # Para vigas
        }
        
        # Definir configuración de análisis dinámica basada en enabled_analyses
        analysis_config = {'enabled_analyses': enabled_analyses}
        
        # Configuración global de visualización
        viz_params = analysis_params.get('visualization', {})
        analysis_config['visualization'] = {
            'enabled': viz_params.get('enabled', False),  # Por defecto NO visualizar
            'static_deformed': viz_params.get('static_deformed', False),  # Deformada estática
            'modal_shapes': viz_params.get('modal_shapes', False),  # Formas modales
            'deform_scale': viz_params.get('deform_scale', 100),  # Factor de escala
            'save_html': viz_params.get('save_html', True),  # Guardar como HTML
            'show_nodes': viz_params.get('show_nodes', True),  # Mostrar nodos
            'line_width': viz_params.get('line_width', 2)  # Grosor de líneas
        }
        
        # Configuración estática (si está habilitada)
        if 'static' in enabled_analyses:
            static_params = analysis_params.get('static', {})
            analysis_config['static'] = {
                'system': static_params.get('system', 'BandGeneral'),
                'numberer': static_params.get('numberer', 'RCM'),
                'constraints': static_params.get('constraints', 'Plain'),
                'integrator': static_params.get('integrator', 'LoadControl'),
                'algorithm': static_params.get('algorithm', 'Linear'),
                'analysis': static_params.get('analysis', 'Static'),
                'steps': static_params.get('steps', 10)
            }
        
        # Configuración modal (si está habilitada)
        if 'modal' in enabled_analyses:
            modal_params = analysis_params.get('modal', {})
            analysis_config['modal'] = {
                'system': modal_params.get('system', 'BandGeneral'),
                'numberer': modal_params.get('numberer', 'RCM'),
                'constraints': modal_params.get('constraints', 'Plain'),
                'integrator': modal_params.get('integrator', 'LoadControl'),
                'algorithm': modal_params.get('algorithm', 'Linear'),
                'analysis': modal_params.get('analysis', 'Static'),
                'num_modes': modal_params.get('num_modes', 6)
            }
        
        # Configuración dinámica (si está habilitada)
        if 'dynamic' in enabled_analyses:
            dynamic_params = analysis_params.get('dynamic', {})
            analysis_config['dynamic'] = {
                'system': dynamic_params.get('system', 'BandGeneral'),
                'numberer': dynamic_params.get('numberer', 'RCM'),
                'constraints': dynamic_params.get('constraints', 'Plain'),
                'integrator': dynamic_params.get('integrator', 'Newmark'),
                'algorithm': dynamic_params.get('algorithm', 'Newton'),
                'analysis': dynamic_params.get('analysis', 'Transient'),
                'dt': dynamic_params.get('dt', 0.01),
                'num_steps': dynamic_params.get('num_steps', 1000)
            }
        
        # Guardar modelo en archivo
        model_file = os.path.join(self.output_dir, f"{model_name}.json")
        model_info = {
            'name': model_name,
            'parameters': {
                'L_B_ratio': L_B_ratio,
                'nx': nx,
                'ny': ny,
                'L': L,
                'B': B,
                **self.fixed_params
            },
            'sections': sections,
            'transformations': transformations,
            'nodes': node_data,
            'elements': element_data,
            'loads': load_data,
            'analysis_config': analysis_config,
            'file_path': model_file
        }
        
        with open(model_file, 'w') as f:
            json.dump(model_info, f, indent=2)
        
        return model_info
    
    def _create_nodes(self, L: float, B: float, nx: int, ny: int) -> Dict:
        """Crea los nodos del modelo."""
        node_data = {}
        node_tag = 1
        
        # Espaciado entre ejes
        dx = L / nx
        dy = B / ny
        dz = self.fixed_params['floor_height']
        
        # Crear nodos para cada piso
        for floor in range(self.fixed_params['num_floors'] + 1):
            z = floor * dz
            for j in range(ny + 1):
                for i in range(nx + 1):
                    x = i * dx
                    y = j * dy
                    node_data[node_tag] = {
                        'coords': [x, y, z],
                        'floor': floor,
                        'grid_pos': [i, j]
                    }
                    node_tag += 1
        
        return node_data
    
    def _create_elements(self, nx: int, ny: int) -> Dict:
        """Crea los elementos del modelo."""
        element_data = {}
        elem_tag = 1

        # Crear elementos de losa (ShellMITC4) en cada nivel de piso (excepto la base)
        # El bucle inicia en 1 para crear losas en el piso 1, 2, etc.
        for floor in range(1, self.fixed_params['num_floors'] + 1):
            base_node = floor * (nx + 1) * (ny + 1)
            for j in range(ny):
                for i in range(nx):
                    # Nodos del elemento de losa
                    n1 = base_node + j * (nx + 1) + i + 1
                    n2 = base_node + j * (nx + 1) + i + 2
                    n3 = base_node + (j + 1) * (nx + 1) + i + 2
                    n4 = base_node + (j + 1) * (nx + 1) + i + 1
                    
                    element_data[elem_tag] = {
                        'type': 'slab',
                        'nodes': [n1, n2, n3, n4],
                        'floor': floor,
                        'section_tag': 1
                    }
                    elem_tag += 1
        
        # Crear elementos de columna (elasticBeamColumn)
        for j in range(ny + 1):
            for i in range(nx + 1):
                for floor in range(self.fixed_params['num_floors']):
                    # Nodos de la columna
                    n1 = floor * (nx + 1) * (ny + 1) + j * (nx + 1) + i + 1
                    n2 = (floor + 1) * (nx + 1) * (ny + 1) + j * (nx + 1) + i + 1
                    
                    element_data[elem_tag] = {
                        'type': 'column',
                        'nodes': [n1, n2],
                        'floor': floor,
                        'section_tag': 2
                    }
                    elem_tag += 1
        
        # Crear elementos de viga (elasticBeamColumn) en cada nivel de piso (excepto la base)
        # El bucle inicia en 1 para crear vigas en el piso 1, 2, etc.
        for floor in range(1, self.fixed_params['num_floors'] + 1):
            base_node = floor * (nx + 1) * (ny + 1)
            
            # Vigas en dirección X
            for j in range(ny + 1):
                for i in range(nx):
                    n1 = base_node + j * (nx + 1) + i + 1
                    n2 = base_node + j * (nx + 1) + i + 2
                    
                    element_data[elem_tag] = {
                        'type': 'beam_x',
                        'nodes': [n1, n2],
                        'floor': floor,
                        'section_tag': 3
                    }
                    elem_tag += 1
            
            # Vigas en dirección Y
            for j in range(ny):
                for i in range(nx + 1):
                    n1 = base_node + j * (nx + 1) + i + 1
                    n2 = base_node + (j + 1) * (nx + 1) + i + 1
                    
                    element_data[elem_tag] = {
                        'type': 'beam_y',
                        'nodes': [n1, n2],
                        'floor': floor,
                        'section_tag': 3
                    }
                    elem_tag += 1
        
        return element_data
    
    def _create_loads(self, node_data: Dict) -> Dict:
        """Crea las cargas del modelo."""
        load_data = {}
        
        # Carga distribuida en losa (1 tonf/m²)
        q = 1.0  # tonf/m²
        
        try:
            # Aplicar carga en nodos del último piso
            for node_tag, node_info in node_data.items():
                if node_info['floor'] == self.fixed_params['num_floors']:
                    # Carga vertical en cada nodo
                    load_data[node_tag] = {
                        'type': 'distributed_load',
                        'value': -q,
                        'direction': 'Z'
                    }
        except Exception as e:
            print(f"Error aplicando carga al nodo {node_tag}: {str(e)}")
            raise
        
        return load_data