"""
Ejemplo 05: Exportación y Scripts Python
========================================

Este ejemplo muestra cómo exportar modelos como scripts Python independientes
que pueden ejecutarse sin el framework completo.

Caso de uso: Distribución de modelos específicos para análisis externos
"""

from src.model_builder import ModelBuilder
from src.python_exporter import PythonExporter
import os

def main():
    """Ejemplo de exportación de scripts Python"""
    
    print("=== Ejemplo 05: Exportación y Scripts Python ===")
    
    # Configurar componentes
    builder = ModelBuilder(output_dir="models")
    exporter = PythonExporter(output_dir="exported_scripts")
    
    # === CREAR MODELOS PARA EXPORTAR ===
    print("\n📦 Creando modelos para exportación...")
    
    # Modelo 1: Edificio pequeño con visualización
    print("\n1️⃣ Modelo pequeño con visualización")
    model_small = builder.create_model(
        L_B_ratio=1.5, B=8.0, nx=3, ny=3,
        model_name="edificio_pequeno",
        enabled_analyses=['static', 'modal'],
        analysis_params={
            'static': {'steps': 15},
            'modal': {'num_modes': 6},
            'visualization': {
                'enabled': True,
                'static_deformed': True,
                'modal_shapes': True,
                'max_modes': 6,
                'deform_scale': 150
            }
        }
    )
    print(f"   ✅ Creado: {model_small['name']}")
    
    # Modelo 2: Edificio grande solo numérico
    print("\n2️⃣ Modelo grande solo numérico")
    model_large = builder.create_model(
        L_B_ratio=2.5, B=20.0, nx=6, ny=4,
        model_name="edificio_grande",
        enabled_analyses=['static', 'modal'],
        analysis_params={
            'static': {'steps': 20, 'algorithm': 'Newton'},
            'modal': {'num_modes': 12},
            'visualization': {'enabled': False}  # Sin visualización
        }
    )
    print(f"   ✅ Creado: {model_large['name']}")
    
    # Modelo 3: Análisis dinámico completo
    print("\n3️⃣ Modelo con análisis dinámico")
    model_dynamic = builder.create_model(
        L_B_ratio=2.0, B=15.0, nx=5, ny=3,
        model_name="edificio_dinamico",
        enabled_analyses=['static', 'modal', 'dynamic'],
        analysis_params={
            'static': {'steps': 15},
            'modal': {'num_modes': 10},
            'dynamic': {
                'dt': 0.01,
                'num_steps': 1500,
                'damping_ratio': 0.05
            },
            'visualization': {'enabled': False}
        }
    )
    print(f"   ✅ Creado: {model_dynamic['name']}")
    
    # === EXPORTACIÓN DE SCRIPTS ===
    print("\n" + "="*50)
    print("🚀 EXPORTANDO SCRIPTS PYTHON")
    print("="*50)
    
    # Exportación 1: Script unificado (todo en un archivo)
    print("\n1️⃣ Exportación UNIFICADA (un solo archivo)")
    
    script_path_small = exporter.export_script(
        model_small,
        separate_files=False,  # Todo en un archivo
        include_visualization=True,
        script_name="edificio_pequeno_unificado"
    )
    
    if script_path_small:
        print(f"   ✅ Script exportado: {script_path_small}")
        print(f"   📁 Tamaño: {os.path.getsize(script_path_small)} bytes")
    
    # Exportación 2: Scripts separados (modular)
    print("\n2️⃣ Exportación MODULAR (archivos separados)")
    
    script_paths_large = exporter.export_script(
        model_large,
        separate_files=True,   # Archivos separados
        include_visualization=False,
        script_name="edificio_grande_modular"
    )
    
    if script_paths_large:
        print(f"   ✅ Scripts exportados:")
        if isinstance(script_paths_large, list):
            for path in script_paths_large:
                print(f"      - {os.path.basename(path)}")
        else:
            print(f"      - {os.path.basename(script_paths_large)}")
    
    # Exportación 3: Con configuración personalizada
    print("\n3️⃣ Exportación PERSONALIZADA")
    
    script_path_dynamic = exporter.export_script(
        model_dynamic,
        separate_files=False,
        include_analysis_config=True,  # Incluir configuración completa
        include_imports=True,          # Incluir todas las importaciones
        script_name="edificio_dinamico_completo"
    )
    
    if script_path_dynamic:
        print(f"   ✅ Script exportado: {script_path_dynamic}")
    
    # === EXPORTACIÓN EN LOTE ===
    print("\n4️⃣ Exportación EN LOTE")
    
    # Crear algunos modelos adicionales rápidamente
    models_for_batch = []
    
    for ratio in [1.0, 1.5, 2.0]:
        model = builder.create_model(
            L_B_ratio=ratio, B=10.0, nx=4, ny=3,
            model_name=f"lote_LB_{ratio:.1f}",
            enabled_analyses=['static'],
            analysis_params={'visualization': {'enabled': False}}
        )
        models_for_batch.append(model)
    
    print(f"   Creados {len(models_for_batch)} modelos para lote")
    
    # Exportar todos los modelos del lote
    batch_results = exporter.batch_export(
        models_dir="models",
        file_pattern="lote_*.json",  # Solo archivos del lote
        separate_files=False,
        output_subdir="batch_export"
    )
    
    print(f"   ✅ Exportación en lote: {len(batch_results)} scripts generados")
    
    # === VERIFICACIÓN DE SCRIPTS EXPORTADOS ===
    print("\n" + "="*50)
    print("🔍 VERIFICACIÓN DE SCRIPTS EXPORTADOS")
    print("="*50)
    
    # Listar todos los archivos exportados
    export_dir = "exported_scripts"
    if os.path.exists(export_dir):
        exported_files = [f for f in os.listdir(export_dir) if f.endswith('.py')]
        
        print(f"📁 Directorio de exportación: {export_dir}/")
        print(f"📄 Archivos generados: {len(exported_files)}")
        
        total_size = 0
        for file in exported_files:
            file_path = os.path.join(export_dir, file)
            file_size = os.path.getsize(file_path)
            total_size += file_size
            print(f"   - {file} ({file_size} bytes)")
        
        print(f"💾 Tamaño total: {total_size} bytes")
    
    # === INSTRUCCIONES DE USO ===
    print("\n" + "="*50)
    print("📖 INSTRUCCIONES DE USO DE SCRIPTS EXPORTADOS")
    print("="*50)
    
    print("""
📋 CÓMO USAR LOS SCRIPTS EXPORTADOS:

1️⃣ SCRIPTS UNIFICADOS (un archivo):
   python edificio_pequeno_unificado.py
   
   ✅ Ventajas:
   - Fácil de distribuir (un solo archivo)
   - No requiere estructura de directorios
   - Independiente del framework
   
   ⚠️  Consideraciones:
   - Requiere OpenSees y opstool instalados
   - Archivos más grandes

2️⃣ SCRIPTS MODULARES (archivos separados):
   python edificio_grande_modular.py
   
   ✅ Ventajas:
   - Código más organizado
   - Reutilización de funciones
   - Fácil mantenimiento
   
   ⚠️  Consideraciones:
   - Mantener estructura de archivos
   - Múltiples archivos para distribuir

3️⃣ PERSONALIZACIÓN:
   - Editar parámetros directamente en el script
   - Modificar configuración de análisis
   - Adaptar a necesidades específicas

4️⃣ DISTRIBUCIÓN:
   - Enviar scripts por email
   - Incluir en repositorios
   - Usar en clusters de cálculo
   """)
    
    # === RECOMENDACIONES ===
    print("\n💡 RECOMENDACIONES:")
    print("- Para modelos únicos: Exportación unificada")
    print("- Para series de modelos: Exportación modular")
    print("- Para distribución: Incluir requirements.txt")
    print("- Para clusters: Scripts sin visualización")
    print("- Para enseñanza: Scripts con comentarios detallados")
    
    print(f"\n✅ Ejemplo completado!")
    print(f"📁 Scripts disponibles en: {export_dir}/")

if __name__ == "__main__":
    main()
