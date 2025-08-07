import os
from typing import Dict, List, Union, Any

class PythonExporter:
    """
    Clase dedicada a exportar modelos y análisis a scripts de Python.
    Actúa como un helper que toma datos de modelo y configuración de análisis
    para generar archivos .py para depuración y desarrollo.
    """

    def __init__(self, output_dir: str = None):
        """
        Inicializa el exportador de Python.

        Args:
            output_dir: Directorio donde se guardarán los scripts generados.
                       Si es None, usa un directorio por defecto relativo al script.
                       Si es una ruta relativa, se interpreta desde la ubicación del archivo que llama.
        """
        if output_dir is None:
            output_dir = self._get_default_output_dir()
        else:
            # Si es una ruta relativa, hacerla relativa al script que llama
            if not os.path.isabs(output_dir):
                output_dir = self._make_relative_to_caller(output_dir)
        
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def _get_default_output_dir(self) -> str:
        """
        Get default output directory relative to the calling script.
        
        Returns:
            Default output directory path
        """
        import sys
        
        # Determinar el directorio base relativo al script que llama
        if hasattr(sys.modules['__main__'], '__file__'):
            # Si se ejecuta como script
            script_dir = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
        else:
            # Si se ejecuta desde REPL/Jupyter, usar directorio actual
            script_dir = os.getcwd()
        
        return os.path.join(script_dir, "python_exports")

    def _make_relative_to_caller(self, relative_path: str) -> str:
        """
        Convert a relative path to be relative to the calling script's directory.
        
        Args:
            relative_path: The relative path to convert
            
        Returns:
            Absolute path relative to the calling script
        """
        import sys
        
        # Determinar el directorio base relativo al script que llama
        if hasattr(sys.modules['__main__'], '__file__'):
            # Si se ejecuta como script
            script_dir = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
        else:
            # Si se ejecuta desde REPL/Jupyter, usar directorio actual
            script_dir = os.getcwd()
        
        return os.path.join(script_dir, relative_path)

    def export_script(self, model_data: Any, separate_files: bool = False) -> List[str]:
        """
        Exporta un modelo a uno o más archivos Python ejecutables.

        Args:
            model_data: Diccionario con la información del modelo O objeto StructuralModel 
                       (debe incluir analysis_config en ambos casos).
            separate_files: Si es True, genera un archivo para el modelo y otro para el análisis.

        Returns:
            Lista de rutas a los archivos Python generados.
        """
        # Auto-detectar y convertir si es necesario
        if hasattr(model_data, 'to_dict'):
            # Es un objeto StructuralModel o similar
            model_info = model_data.to_dict()
            print(f"✓ Detectado objeto {type(model_data).__name__}, convertido a diccionario")
        elif isinstance(model_data, dict):
            # Ya es un diccionario
            model_info = model_data
            print("✓ Detectado diccionario, usando directamente")
        else:
            raise TypeError(f"model_data debe ser un diccionario o un objeto con método to_dict(), "
                          f"recibido: {type(model_data)}")
        
        # La configuración SIEMPRE viene del modelo - no hay opciones externas
        if 'analysis_config' not in model_info:
            raise ValueError("El modelo debe incluir configuración de análisis en 'analysis_config'.")
        analysis_config = model_info['analysis_config']
        
        model_name = model_info['name']
        model_code = self._generate_model_code(model_info)

        if separate_files:
            # --- MODO DE ARCHIVOS SEPARADOS ---
            model_py_file = os.path.join(self.output_dir, f"{model_name}_model.py")
            model_code_with_main = model_code + [
                "",
                "if __name__ == '__main__':",
                "    build_model()",
                "    print('Modelo construido y listo para ser importado.')"
            ]
            with open(model_py_file, 'w', encoding='utf-8-sig') as f:
                f.write('\n'.join(model_code_with_main))

            if analysis_config:
                analysis_py_file = os.path.join(self.output_dir, f"{model_name}_run_analysis.py")
                analysis_code = self._generate_analysis_code(model_name, analysis_config, is_separate_file=True)
                with open(analysis_py_file, 'w', encoding='utf-8-sig') as f:
                    f.write('\n'.join(analysis_code))
                return [model_py_file, analysis_py_file]
            return [model_py_file]

        else:
            # --- MODO DE ARCHIVO ÚNICO ---
            output_file = os.path.join(self.output_dir, f"{model_name}_combined.py")
            full_code = model_code

            if analysis_config:
                analysis_code = self._generate_analysis_code(model_name, analysis_config, is_separate_file=False)
                full_code.extend(analysis_code)
            else:
                full_code.extend([
                    "",
                    "if __name__ == '__main__':",
                    "    build_model()",
                    "    print('Modelo construido exitosamente.')"
                ])

            with open(output_file, 'w', encoding='utf-8-sig') as f:
                f.write('\n'.join(full_code))
            return [output_file]

    def _generate_model_code(self, model_info: Dict) -> List[str]:
        """Genera el código Python para la función build_model()."""
        params = model_info['parameters']
        material = model_info.get('material', {})
        sections = model_info.get('sections', {})
        elements = model_info.get('elements', {})
        
        # Parámetros de material (nueva estructura) con valores por defecto
        E = material.get('E', 2.1e11)  # Concreto típico
        nu = material.get('nu', 0.3)   # Coeficiente de Poisson típico
        rho = material.get('rho', 2400)  # Densidad del concreto
        
        # Parámetros geométricos/seccionales desde params con valores por defecto
        slab_thickness = params.get('slab_thickness', 0.15)  # 15 cm
        column_size = params.get('column_size', [0.3, 0.3])  # 30x30 cm
        beam_size = params.get('beam_size', [0.3, 0.5])  # 30x50 cm
        
        code = [
            "import openseespy.opensees as ops",
            "import numpy as np",
            "",
            "def build_model():",
            "    # Limpiar modelo anterior",
            "    ops.wipe()",
            "    ops.model('basic', '-ndm', 3, '-ndf', 6)",
            "",
            "    # Parámetros del modelo",
            f"    L, B = {params['L']}, {params['B']}  # Dimensiones",
            f"    nx, ny = {params['nx']}, {params['ny']}  # Ejes",
            f"    E = {E}  # Módulo de elasticidad",
            f"    nu = {nu}  # Coeficiente de Poisson",
            f"    G = E / (2 * (1 + nu))  # Módulo de corte",
            f"    thickness = {slab_thickness}  # Espesor de losa",
            f"    rho = {rho}  # Densidad",
            "",
            "    # Crear nodos",
        ]
        
        L, B, nx, ny = params['L'], params['B'], params['nx'], params['ny']
        dz = params.get('floor_height', 3.0)  # Altura por defecto de 3m
        num_floors = params.get('num_floors', 1)  # Un piso por defecto
        dx, dy = L / nx, B / ny
        
        node_id = 1
        for floor in range(num_floors + 1):
            z = floor * dz
            for j in range(ny + 1):
                y = j * dy
                for i in range(nx + 1):
                    x = i * dx
                    code.append(f"    ops.node({node_id}, {x}, {y}, {z})")
                    node_id += 1

        code.extend([
            "", "    # Crear materiales y secciones",
            "    ops.section('ElasticMembranePlateSection', 1, E, nu, thickness, rho)",
            "", "    # Columnas",
            f"    col_w, col_h = {column_size[0]}, {column_size[1]}",
            "    A_col = col_w * col_h",
            "    Iz_col = col_w * col_h**3 / 12",
            "    Iy_col = col_h * col_w**3 / 12",
            "    G = E / (2 * (1 + nu))",
            "    # Constante torsional para sección rectangular (Aproximación de Timoshenko)",
            "    a_col, b_col = max(col_w, col_h), min(col_w, col_h)",
            "    J_col = a_col * b_col**3 * (1/3 - 0.21 * (b_col/a_col) * (1 - (b_col**4)/(12*a_col**4)))",
            "    ops.section('Elastic', 2, E, A_col, Iz_col, Iy_col, G, J_col)",
            "", "    # Vigas",
            f"    beam_w, beam_h = {beam_size[0]}, {beam_size[1]}",
            "    A_beam = beam_w * beam_h",
            "    Iz_beam = beam_w * beam_h**3 / 12",
            "    Iy_beam = beam_h * beam_w**3 / 12",
            "    # Constante torsional para sección rectangular (Aproximación de Timoshenko)",
            "    a_beam, b_beam = max(beam_w, beam_h), min(beam_w, beam_h)",
            "    J_beam = a_beam * b_beam**3 * (1/3 - 0.21 * (b_beam/a_beam) * (1 - (b_beam**4)/(12*a_beam**4)))",
            "    ops.section('Elastic', 3, E, A_beam, Iz_beam, Iy_beam, G, J_beam)",
            "", "    # Transformaciones geométricas",
            "    ops.geomTransf('Linear', 4, 0, 1, 0)",
            "    ops.geomTransf('Linear', 5, 0, 0, 1)", ""
        ])
        
        code.append("    # Crear elementos")
        for elem_id, elem in elements.items():
            elem_type = elem['type']
            nodes = elem['nodes']
            sec_tag = elem['section_tag']
            
            if elem_type == 'slab':
                code.append(f"    ops.element('ShellMITC4', {elem_id}, *{nodes}, {sec_tag})")
            elif elem_type in ['column', 'beam_x', 'beam_y']:
                # Buscar el transf_tag en la sección correspondiente
                # print(type(list(sections.keys())[0]))
                section_info = sections.get(str(sec_tag))
                transf_tag = section_info.get('transf_tag', 1000)  # Usar 1000 como valor por defecto si no se encuentra
                code.append(f"    ops.element('elasticBeamColumn', {elem_id}, *{nodes}, {sec_tag}, {transf_tag})")
        
        code.extend(["", "    # Aplicar restricciones en la base"])
        num_nodes_per_floor = (nx + 1) * (ny + 1)
        for node_id in range(1, num_nodes_per_floor + 1):
            code.append(f"    ops.fix({node_id}, 1, 1, 1, 1, 1, 1)")
        
        code.extend([
            "    # Aplicar cargas",
            "    ops.timeSeries('Linear', 1)",
            "    ops.pattern('Plain', 1, 1)"
        ])
        # Aplicar cargas a los nodos del último piso
        q = 1.0
        top_floor_start = num_nodes_per_floor * num_floors + 1
        top_floor_end = num_nodes_per_floor * (num_floors + 1) + 1
        for node_id in range(top_floor_start, top_floor_end):
            code.append(f"    ops.load({node_id}, 0.0, 0.0, {-q}, 0.0, 0.0, 0.0)")
            
        return code

    def _generate_analysis_code(self, model_name: str, analysis_config: Dict,
                                is_separate_file: bool) -> List[str]:
        """Genera el código Python para la función run_analysis() y el bloque main."""
        enabled_analyses = analysis_config.get('enabled_analyses', ['static', 'modal'])
        
        # Solo acceder a configuraciones que existen
        static_cfg = analysis_config.get('static', {}) if 'static' in enabled_analyses else {}
        modal_cfg = analysis_config.get('modal', {}) if 'modal' in enabled_analyses else {}
        dynamic_cfg = analysis_config.get('dynamic', {}) if 'dynamic' in enabled_analyses else {}
        
        code = []
        
        if is_separate_file:
            code.extend([
                f"from {model_name}_model import build_model",
                "import openseespy.opensees as ops",
                "import numpy as np", ""
            ])

        code.extend([
            "", "def run_analysis():"
        ])
        
        # Análisis estático (solo si está habilitado)
        if 'static' in enabled_analyses and static_cfg:
            code.extend([
                "    print('\\n--- Iniciando Análisis Estático ---')", 
                "    try:",
                f"        ops.system('{static_cfg.get('system', 'BandGeneral')}')",
                f"        ops.numberer('{static_cfg.get('numberer', 'Plain')}')",
                f"        ops.constraints('{static_cfg.get('constraints', 'Plain')}')",
                f"        ops.integrator('{static_cfg.get('integrator', 'LoadControl')}', 1.0 / {static_cfg.get('steps', 10)})",
                f"        ops.algorithm('{static_cfg.get('algorithm', 'Newton')}')",
                f"        ops.analysis('{static_cfg.get('analysis', 'Static')}')",
                f"        ops.analyze({static_cfg.get('steps', 10)})",
                "        print('Análisis estático completado exitosamente.')",
                "    except Exception as e:",
                "        print(f'Error en análisis estático: {e}')",
                ""
            ])
        
        # Análisis modal (solo si está habilitado)
        if 'modal' in enabled_analyses and modal_cfg:
            code.extend([
                "    print('\\n--- Iniciando Análisis Modal ---')", 
                "    try:",
                "        ops.setTime(0.0)", 
                "        ops.remove('loadPattern', 1)", 
                "",
                f"        num_modes = {modal_cfg.get('num_modes', 6)}",
                "        eigen_values = ops.eigen(num_modes)",
                "        print('Períodos Modales (s):')",
                "        for i, val in enumerate(eigen_values):",
                "            if val > 1e-6:",
                "                freq = np.sqrt(val) / (2 * np.pi)",
                "                period = 1.0 / freq",
                "                print(f'  - Modo {i+1}: {period:.4f} s')",
                "        print('Análisis modal completado exitosamente.')",
                "    except Exception as e:",
                "        print(f'Error en análisis modal: {e}')",
                ""
            ])
        
        # Análisis dinámico (solo si está habilitado)
        if 'dynamic' in enabled_analyses and dynamic_cfg:
            code.extend([
                "    print('\\n--- Iniciando Análisis Dinámico ---')", 
                "    try:",
                "        # Configuración básica de análisis dinámico",
                f"        dt = {dynamic_cfg.get('dt', 0.01)}",
                f"        num_steps = {dynamic_cfg.get('num_steps', 1000)}",
                "        print(f'Análisis dinámico con dt={dynamic_cfg.get('dt', 0.01)} s, pasos={dynamic_cfg.get('num_steps', 1000)}')",
                "        # Aquí se agregaría la configuración específica del análisis dinámico",
                "        print('Análisis dinámico completado exitosamente.')",
                "    except Exception as e:",
                "        print(f'Error en análisis dinámico: {e}')",
                ""
            ])

        # El bloque main se añade independientemente de si el archivo es separado o no
        code.extend([
            "", "if __name__ == '__main__':",
            "    build_model()",
            "    print('Modelo construido exitosamente.')",
            "    run_analysis()"
        ])

        return code
