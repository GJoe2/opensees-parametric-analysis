"""
Suite de Tests Principal para OpenSees Model Builder
===================================================

Este archivo permite ejecutar todos los tests del paquete de manera organizada.
Incluye tests para todas las clases principales del sistema refactorizado.

Tests incluidos:
- TestModelBuilder: Funcionalidad del constructor de modelos
- TestAnalysisEngine: Motor de análisis refactorizado  
- TestVisualizationHelper: Helper de visualización con opstool
- TestAnalysisTypes: Clases de análisis específicos (Static, Modal, Dynamic)
- TestModelBuilderHelpers: Helpers de conveniencia para casos comunes
- TestParametricRunner: Runner de estudios paramétricos

Uso:
    python -m pytest tests/
    python tests/run_all_tests.py
    python -m unittest discover tests/

Autor: OpenSees Model Builder
Fecha: Agosto 2025
"""

import unittest
import sys
import os

# Agregar el directorio principal al path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Importar todos los módulos de test
from tests.test_model_builder import TestModelBuilder
from tests.test_analysis_engine import TestAnalysisEngine
from tests.test_visualization_helper import TestVisualizationHelper
from tests.test_analysis_types import TestBaseAnalysis, TestStaticAnalysis, TestModalAnalysis, TestDynamicAnalysis
from tests.test_utils import TestModelBuilderHelpers, TestGlobalConvenienceFunctions
from tests.test_parametric_runner import TestParametricRunner


def create_test_suite():
    """
    Crea la suite completa de tests organizados por categorías.
    
    Returns:
        unittest.TestSuite: Suite completa de tests
    """
    suite = unittest.TestSuite()
    
    # Tests de ModelBuilder (API principal)
    print("📦 Agregando tests de ModelBuilder...")
    suite.addTest(unittest.makeSuite(TestModelBuilder))
    
    # Tests de AnalysisEngine (motor refactorizado)
    print("⚙️  Agregando tests de AnalysisEngine...")
    suite.addTest(unittest.makeSuite(TestAnalysisEngine))
    
    # Tests de VisualizationHelper (visualización separada)
    print("📊 Agregando tests de VisualizationHelper...")
    suite.addTest(unittest.makeSuite(TestVisualizationHelper))
    
    # Tests de tipos de análisis específicos
    print("🔬 Agregando tests de Analysis Types...")
    suite.addTest(unittest.makeSuite(TestBaseAnalysis))
    suite.addTest(unittest.makeSuite(TestStaticAnalysis))
    suite.addTest(unittest.makeSuite(TestModalAnalysis))
    suite.addTest(unittest.makeSuite(TestDynamicAnalysis))
    
    # Tests de utilidades y helpers
    print("🛠️  Agregando tests de Utilities y Helpers...")
    suite.addTest(unittest.makeSuite(TestModelBuilderHelpers))
    suite.addTest(unittest.makeSuite(TestGlobalConvenienceFunctions))
    
    # Tests de ParametricRunner
    print("📈 Agregando tests de ParametricRunner...")
    suite.addTest(unittest.makeSuite(TestParametricRunner))
    
    return suite


def run_test_category(category_name, test_classes):
    """
    Ejecuta una categoría específica de tests.
    
    Args:
        category_name: Nombre de la categoría
        test_classes: Lista de clases de test
        
    Returns:
        unittest.TestResult: Resultado de los tests
    """
    print(f"\n{'='*60}")
    print(f"🧪 EJECUTANDO TESTS: {category_name}")
    print(f"{'='*60}")
    
    suite = unittest.TestSuite()
    for test_class in test_classes:
        suite.addTest(unittest.makeSuite(test_class))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


def run_all_tests():
    """
    Ejecuta todos los tests del proyecto.
    
    Returns:
        bool: True si todos los tests pasaron, False si hubo fallas
    """
    print("🚀 INICIANDO SUITE COMPLETA DE TESTS")
    print("=" * 80)
    
    # Crear y ejecutar la suite completa
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Mostrar resumen final
    print("\n" + "=" * 80)
    print("📋 RESUMEN FINAL DE TESTS")
    print("=" * 80)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallas: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    
    if result.failures:
        print(f"\n❌ FALLAS DETECTADAS ({len(result.failures)}):")
        for test, error in result.failures:
            print(f"   - {test}: {error.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\n🚨 ERRORES DETECTADOS ({len(result.errors)}):")
        for test, error in result.errors:
            print(f"   - {test}: {error.split('Exception:')[-1].strip()}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    
    if success:
        print(f"\n✅ TODOS LOS TESTS PASARON EXITOSAMENTE!")
    else:
        print(f"\n❌ ALGUNOS TESTS FALLARON. Revisar detalles arriba.")
    
    print("=" * 80)
    return success


def run_specific_category():
    """
    Permite ejecutar una categoría específica de tests de manera interactiva.
    """
    categories = {
        '1': ('ModelBuilder', [TestModelBuilder]),
        '2': ('AnalysisEngine', [TestAnalysisEngine]),
        '3': ('VisualizationHelper', [TestVisualizationHelper]),
        '4': ('Analysis Types', [TestBaseAnalysis, TestStaticAnalysis, TestModalAnalysis, TestDynamicAnalysis]),
        '5': ('Utilities & Helpers', [TestModelBuilderHelpers, TestGlobalConvenienceFunctions]),
        '6': ('ParametricRunner', [TestParametricRunner])
    }
    
    print("📂 CATEGORÍAS DE TESTS DISPONIBLES:")
    print("-" * 40)
    for key, (name, _) in categories.items():
        print(f"{key}. {name}")
    print("0. Todos los tests")
    
    choice = input("\n👆 Selecciona una categoría (0-6): ").strip()
    
    if choice == '0':
        return run_all_tests()
    elif choice in categories:
        category_name, test_classes = categories[choice]
        result = run_test_category(category_name, test_classes)
        return len(result.failures) == 0 and len(result.errors) == 0
    else:
        print("❌ Opción inválida.")
        return False


if __name__ == '__main__':
    """
    Punto de entrada principal para ejecutar tests.
    
    Modos de uso:
    - Sin argumentos: Menú interactivo
    - Con 'all': Ejecuta todos los tests
    - Con número de categoría: Ejecuta categoría específica
    """
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg == 'all':
            success = run_all_tests()
        elif arg.isdigit() and 1 <= int(arg) <= 6:
            # Ejecutar categoría específica
            categories = {
                '1': ('ModelBuilder', [TestModelBuilder]),
                '2': ('AnalysisEngine', [TestAnalysisEngine]),
                '3': ('VisualizationHelper', [TestVisualizationHelper]),
                '4': ('Analysis Types', [TestBaseAnalysis, TestStaticAnalysis, TestModalAnalysis, TestDynamicAnalysis]),
                '5': ('Utilities & Helpers', [TestModelBuilderHelpers, TestGlobalConvenienceFunctions]),
                '6': ('ParametricRunner', [TestParametricRunner])
            }
            category_name, test_classes = categories[arg]
            result = run_test_category(category_name, test_classes)
            success = len(result.failures) == 0 and len(result.errors) == 0
        else:
            print("❌ Argumento inválido. Uso: python run_all_tests.py [all|1-6]")
            success = False
    else:
        # Modo interactivo
        success = run_specific_category()
    
    # Retornar código de salida apropiado
    sys.exit(0 if success else 1)
