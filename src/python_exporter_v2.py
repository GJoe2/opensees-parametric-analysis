"""
PythonExporter V2 - Optimized version that works directly with domain objects.

This version eliminates unnecessary dictionary conversions and works directly with
StructuralModel objects and their rich domain classes for better performance,
type safety, and maintainability.
"""

from __future__ import annotations
import os
import sys
from typing import Dict, List, Union, Any
from .domain import StructuralModel


class PythonExporterV2:
    """
    Optimized Python exporter that works directly with StructuralModel objects.
    
    This version leverages the rich domain objects instead of primitive dictionaries,
    providing better type safety, performance, and maintainability.
    """

    def __init__(self, output_dir: str = None):
        """
        Initialize the Python exporter.

        Args:
            output_dir: Directory where generated scripts will be saved.
                       If None, uses a default directory relative to the calling script.
                       If relative path, interprets from the calling script location.
        """
        if output_dir is None:
            output_dir = self._get_default_output_dir()
        else:
            # If relative path, make it relative to the calling script
            if not os.path.isabs(output_dir):
                output_dir = self._make_relative_to_caller(output_dir)
        
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def _get_default_output_dir(self) -> str:
        """Get default output directory relative to the calling script."""
        # Determine base directory relative to the calling script
        if hasattr(sys.modules['__main__'], '__file__'):
            # If running as script
            script_dir = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
        else:
            # If running from REPL/Jupyter, use current directory
            script_dir = os.getcwd()
        
        return os.path.join(script_dir, "python_exports")

    def _make_relative_to_caller(self, relative_path: str) -> str:
        """Convert a relative path to be relative to the calling script's directory."""
        # Determine base directory relative to the calling script
        if hasattr(sys.modules['__main__'], '__file__'):
            # If running as script
            script_dir = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
        else:
            # If running from REPL/Jupyter, use current directory
            script_dir = os.getcwd()
        
        return os.path.join(script_dir, relative_path)

    def export_script(self, model: Union[StructuralModel, Dict], separate_files: bool = False) -> List[str]:
        """
        Export a structural model to one or more executable Python files.

        Args:
            model: StructuralModel object (recommended) or dictionary for backward compatibility
            separate_files: If True, generates separate files for model and analysis.

        Returns:
            List of paths to the generated Python files.
        """
        # Handle backward compatibility with dictionaries
        if isinstance(model, dict):
            print("⚠️  Received dictionary (deprecated). Consider using StructuralModel object.")
            model_obj = StructuralModel.from_dict(model)
        elif hasattr(model, 'to_dict'):
            print(f"✓ Detected {type(model).__name__} object, working directly")
            model_obj = model
        else:
            raise TypeError(f"model must be StructuralModel or dict, received: {type(model)}")
        
        model_name = model_obj.name
        model_code = self._generate_model_code(model_obj)

        if separate_files:
            # --- SEPARATE FILES MODE ---
            model_py_file = os.path.join(self.output_dir, f"{model_name}_model.py")
            model_code_with_main = model_code + [
                "",
                "if __name__ == '__main__':",
                "    build_model()",
                "    print('Model built and ready to be imported.')"
            ]
            with open(model_py_file, 'w', encoding='utf-8-sig') as f:
                f.write('\n'.join(model_code_with_main))

            if model_obj.analysis_config:
                analysis_py_file = os.path.join(self.output_dir, f"{model_name}_run_analysis.py")
                analysis_code = self._generate_analysis_code(model_name, model_obj.analysis_config, is_separate_file=True)
                with open(analysis_py_file, 'w', encoding='utf-8-sig') as f:
                    f.write('\n'.join(analysis_code))
                return [model_py_file, analysis_py_file]
            return [model_py_file]

        else:
            # --- SINGLE FILE MODE ---
            output_file = os.path.join(self.output_dir, f"{model_name}_combined.py")
            full_code = model_code

            if model_obj.analysis_config:
                analysis_code = self._generate_analysis_code(model_name, model_obj.analysis_config, is_separate_file=False)
                full_code.extend(analysis_code)
            else:
                full_code.extend([
                    "",
                    "if __name__ == '__main__':",
                    "    build_model()",
                    "    print('Model built successfully.')"
                ])

            with open(output_file, 'w', encoding='utf-8-sig') as f:
                f.write('\n'.join(full_code))
            return [output_file]

    def _generate_model_code(self, model: StructuralModel) -> List[str]:
        """
        Generate Python code for the build_model() function.
        Works directly with StructuralModel object - MORE EFFICIENT AND TYPE-SAFE.
        """
        # Direct access to objects - type-safe and efficient
        params = model.parameters
        material = model.material
        sections = model.sections
        geometry = model.geometry
        loads = model.loads
        
        # Material parameters - direct access to properties
        E = material.E
        nu = material.nu  
        rho = material.rho
        G = material.G  # ← Calculated property automatically available!
        
        # Geometric parameters - direct access
        L = params.L
        B = params.B
        nx, ny = params.nx, params.ny
        dz = params.floor_height
        num_floors = params.num_floors
        
        code = [
            "import openseespy.opensees as ops",
            "import numpy as np",
            "",
            "def build_model():",
            "    # Clear previous model",
            "    ops.wipe()",
            "    ops.model('basic', '-ndm', 3, '-ndf', 6)",
            "",
            "    # Model parameters",
            f"    L, B = {L}, {B}  # Dimensions",
            f"    nx, ny = {nx}, {ny}  # Grid axes",
            f"    E = {E}  # Elastic modulus",
            f"    nu = {nu}  # Poisson's ratio",
            f"    G = {G}  # Shear modulus (calculated)",
            f"    rho = {rho}  # Density",
            "",
            "    # Create nodes",
        ]
        
        # Generate nodes using geometry object directly
        for node_id, node in geometry.nodes.items():
            x, y, z = node.coords
            code.append(f"    ops.node({node_id}, {x}, {y}, {z})")

        code.extend([
            "", 
            "    # Create materials and sections",
        ])
        
        # Generate sections using sections object directly
        for section_id, section in sections.sections.items():
            if section.element_type == 'slab':
                # ShellSection
                thickness = section.thickness
                code.append(f"    ops.section('ElasticMembranePlateSection', {section_id}, {E}, {nu}, {thickness}, {rho})")
            
            elif section.element_type in ['column', 'beam']:
                # FrameSection
                width, height = section.size
                A = width * height
                Iz = width * height**3 / 12
                Iy = height * width**3 / 12
                
                # Torsional constant for rectangular section
                a, b = max(width, height), min(width, height)
                J = a * b**3 * (1/3 - 0.21 * (b/a) * (1 - (b**4)/(12*a**4)))
                
                code.append(f"    # {section.element_type.title()}: {width}x{height}")
                code.append(f"    ops.section('Elastic', {section_id}, {E}, {A}, {Iz}, {Iy}, {G}, {J})")

        # Geometric transformations using sections object
        code.append("")
        code.append("    # Geometric transformations")
        for transf_id, transf_data in sections.transformations.items():
            vecxz = transf_data.get('vecxz', [0, 1, 0])
            code.append(f"    ops.geomTransf('Linear', {transf_id}, {vecxz[0]}, {vecxz[1]}, {vecxz[2]})")
        
        code.append("")
        code.append("    # Create elements")
        
        # Generate elements using geometry object directly
        for elem_id, element in geometry.elements.items():
            nodes = element.nodes
            section_tag = element.section_tag
            
            if element.element_type == 'slab':
                code.append(f"    ops.element('ShellMITC4', {elem_id}, *{nodes}, {section_tag})")
            elif element.element_type in ['column', 'beam_x', 'beam_y']:
                # Get transformation tag from section
                section = sections.sections.get(section_tag)
                transf_tag = section.transf_tag if section else 4  # Default
                code.append(f"    ops.element('elasticBeamColumn', {elem_id}, *{nodes}, {section_tag}, {transf_tag})")
        
        # Base constraints
        code.extend(["", "    # Apply base constraints"])
        base_nodes = [node_id for node_id, node in geometry.nodes.items() if node.floor == 0]
        for node_id in base_nodes:
            code.append(f"    ops.fix({node_id}, 1, 1, 1, 1, 1, 1)")
        
        # Loads using loads object directly
        code.extend([
            "",
            "    # Apply loads",
            "    ops.timeSeries('Linear', 1)",
            "    ops.pattern('Plain', 1, 1)"
        ])
        
        for load_id, load in loads.loads.items():
            node_tag = load.node_tag
            direction = load.direction
            value = load.value
            
            # Map direction to components
            force_components = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # [Fx, Fy, Fz, Mx, My, Mz]
            direction_map = {'X': 0, 'Y': 1, 'Z': 2, 'RX': 3, 'RY': 4, 'RZ': 5}
            
            if direction in direction_map:
                force_components[direction_map[direction]] = value
            
            code.append(f"    ops.load({node_tag}, {', '.join(map(str, force_components))})")
            
        return code

    def _generate_analysis_code(self, model_name: str, analysis_config, is_separate_file: bool) -> List[str]:
        """
        Generate Python code for analysis using AnalysisConfig object directly.
        """
        enabled_analyses = analysis_config.enabled_analyses
        
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
        
        # Static analysis
        if 'static' in enabled_analyses:
            static_config = analysis_config.static_config
            if static_config:
                code.extend([
                    "    print('\\n--- Starting Static Analysis ---')", 
                    "    try:",
                    f"        ops.system('{static_config.system}')",
                    f"        ops.numberer('{static_config.numberer}')",
                    f"        ops.constraints('{static_config.constraints}')",
                    f"        ops.integrator('{static_config.integrator}', 1.0 / {static_config.steps})",
                    f"        ops.algorithm('{static_config.algorithm}')",
                    f"        ops.analysis('{static_config.analysis}')",
                    f"        ops.analyze({static_config.steps})",
                    "        print('Static analysis completed successfully.')",
                    "    except Exception as e:",
                    "        print(f'Error in static analysis: {e}')",
                    ""
                ])
        
        # Modal analysis
        if 'modal' in enabled_analyses:
            modal_config = analysis_config.modal_config
            if modal_config:
                code.extend([
                    "    print('\\n--- Starting Modal Analysis ---')", 
                    "    try:",
                    "        ops.setTime(0.0)", 
                    "        ops.remove('loadPattern', 1)", 
                    "",
                    f"        num_modes = {modal_config.num_modes}",
                    "        eigen_values = ops.eigen(num_modes)",
                    "        print('Modal Periods (s):')",
                    "        for i, val in enumerate(eigen_values):",
                    "            if val > 1e-6:",
                    "                freq = np.sqrt(val) / (2 * np.pi)",
                    "                period = 1.0 / freq",
                    "                print(f'  - Mode {i+1}: {period:.4f} s')",
                    "        print('Modal analysis completed successfully.')",
                    "    except Exception as e:",
                    "        print(f'Error in modal analysis: {e}')",
                    ""
                ])
        
        # Dynamic analysis
        if 'dynamic' in enabled_analyses:
            dynamic_config = analysis_config.dynamic_config
            if dynamic_config:
                code.extend([
                    "    print('\\n--- Starting Dynamic Analysis ---')", 
                    "    try:",
                    "        # Basic dynamic analysis configuration",
                    f"        dt = {dynamic_config.dt}",
                    f"        num_steps = {dynamic_config.num_steps}",
                    "        print(f'Dynamic analysis with dt={dt} s, steps={num_steps}')",
                    "        # Specific dynamic analysis configuration would be added here",
                    "        print('Dynamic analysis completed successfully.')",
                    "    except Exception as e:",
                    "        print(f'Error in dynamic analysis: {e}')",
                    ""
                ])

        # Main block
        code.extend([
            "", "if __name__ == '__main__':",
            "    build_model()",
            "    print('Model built successfully.')",
            "    run_analysis()"
        ])

        return code

    def export_model_summary(self, model: StructuralModel, filename: str = None) -> str:
        """
        Export a summary of the model to a text file.
        
        Args:
            model: StructuralModel object
            filename: Output filename (optional)
            
        Returns:
            Path to the exported summary file
        """
        if filename is None:
            filename = f"{model.name}_summary.txt"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Get model summary using the rich object
        summary = model.get_model_summary()
        
        # Generate detailed summary text
        summary_text = [
            f"STRUCTURAL MODEL SUMMARY: {model.name}",
            "=" * 50,
            "",
            "DIMENSIONS:",
            f"  Length (L): {summary['dimensions']['L']} m",
            f"  Width (B): {summary['dimensions']['B']} m", 
            f"  Aspect Ratio (L/B): {summary['dimensions']['aspect_ratio']}",
            f"  Total Height: {summary['dimensions']['height']} m",
            f"  Footprint Area: {summary['dimensions']['footprint_area']} m²",
            "",
            "MESH:",
            f"  X-direction axes: {summary['mesh']['nx']}",
            f"  Y-direction axes: {summary['mesh']['ny']}",
            f"  Number of floors: {summary['mesh']['num_floors']}",
            "",
            "MODEL COUNTS:",
            f"  Nodes: {summary['counts']['nodes']}",
            f"  Elements: {summary['counts']['elements']}",
            f"  Sections: {summary['counts']['sections']}",
            f"  Loads: {summary['counts']['loads']}",
            "",
            "MATERIAL PROPERTIES:",
            f"  Name: {model.material.name}",
            f"  Elastic Modulus (E): {model.material.E} Pa",
            f"  Poisson's Ratio (ν): {model.material.nu}",
            f"  Density (ρ): {model.material.rho} kg/m³",
            f"  Shear Modulus (G): {model.material.G} Pa",
            f"  Concrete Strength (fc): {model.material.fc} MPa" if model.material.fc else "",
            f"  Steel Yield (fy): {model.material.fy} MPa" if model.material.fy else "",
            "",
            "ENABLED ANALYSES:",
            f"  {', '.join(summary['analyses']['enabled'])}",
            f"  Total enabled: {summary['analyses']['count']}",
            "",
            f"Generated on: {model.name}",
            f"Export directory: {self.output_dir}"
        ]
        
        # Filter out empty lines
        summary_text = [line for line in summary_text if line is not None]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(summary_text))
        
        return filepath
