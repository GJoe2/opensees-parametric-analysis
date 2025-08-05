"""
Ejemplo enfocado en la creación y manejo de archivos JSON con ModelBuilder.

Este ejemplo demuestra todas las funcionalidades relacionadas con JSON
sin depender del AnalysisEngine.
"""

import os
import sys
import json
import glob

# Para desarrollo: agregar src al path 
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_dir)


def ejemplo_json_completo():
    """Ejemplo completo de trabajo con archivos JSON."""
    
    print("📄 Ejemplo: Trabajo Completo con Archivos JSON")
    print("=" * 50)
    
    try:
        # =========== IMPORTAR E INICIALIZAR ===========
        print("📦 Paso 1: Importando ModelBuilder...")
        from model_builder import ModelBuilder
        
        # Crear directorio de salida en la misma carpeta que el script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "json_ejemplos")
        
        builder = ModelBuilder(output_dir=output_dir)
        print(f"   ✅ ModelBuilder inicializado")
        print(f"   📁 Directorio de salida: {output_dir}")
        
        # =========== CREAR MODELO BÁSICO ===========
        print("\n🏗️ Paso 2: Creando modelo básico...")
        
        modelo = builder.create_model(
            L_B_ratio=1.5,
            B=10.0,
            nx=3,
            ny=2,
            enabled_analyses=['static', 'modal']
        )
        
        archivo_original = os.path.join(output_dir, f"{modelo.name}.json")
        print(f"   ✅ Modelo creado: {modelo.name}")
        print(f"   💾 Guardado automáticamente: {os.path.basename(archivo_original)}")
        
        # =========== INFORMACIÓN DEL MODELO ===========
        print("\n📊 Paso 3: Información del modelo...")
        
        # Obtener resumen
        resumen = builder.get_model_summary(modelo)
        print(f"   📐 Dimensiones: {resumen['dimensions']['L']}m x {resumen['dimensions']['B']}m")
        print(f"   🎯 Relación L/B: {resumen['dimensions']['aspect_ratio']:.1f}")
        print(f"   📏 Altura total: {resumen['dimensions']['height']}m")
        print(f"   📦 Área de planta: {resumen['dimensions']['footprint_area']} m²")
        print(f"   🔗 Nodos: {resumen['counts']['nodes']}")
        print(f"   📊 Elementos: {resumen['counts']['elements']}")
        print(f"   🏗️ Pisos: {resumen['mesh']['num_floors']}")
        print(f"   ⚡ Análisis habilitados: {resumen['analyses']['enabled']}")
        
        # =========== MÉTODOS DE GUARDADO ===========
        print("\n💾 Paso 4: Métodos de guardado...")
        
        # 1. Guardar con nombre personalizado
        archivo_personalizado = os.path.join(output_dir, "edificio_ejemplo.json")
        modelo.save(archivo_personalizado)
        print(f"   📁 Guardado personalizado: {os.path.basename(archivo_personalizado)}")
        
        # 2. Exportar como diccionario puro
        modelo_dict = modelo.to_dict()
        archivo_dict = os.path.join(output_dir, "modelo_como_diccionario.json")
        with open(archivo_dict, 'w', encoding='utf-8') as f:
            json.dump(modelo_dict, f, indent=2, ensure_ascii=False)
        print(f"   📋 Exportado como dict: {os.path.basename(archivo_dict)}")
        
        # 3. Guardar solo el resumen
        archivo_resumen = os.path.join(output_dir, "resumen_del_modelo.json")
        with open(archivo_resumen, 'w', encoding='utf-8') as f:
            json.dump(resumen, f, indent=2, ensure_ascii=False)
        print(f"   📊 Resumen guardado: {os.path.basename(archivo_resumen)}")
        
        # 4. Crear archivo de metadatos
        metadatos = {
            "fecha_creacion": "2025-08-04",
            "version_software": "1.0.0",
            "descripcion": "Modelo estructural de ejemplo",
            "autor": "Usuario OpenSees",
            "modelo_principal": modelo.name,
            "archivos_relacionados": [
                f"{modelo.name}.json",
                "edificio_ejemplo.json",
                "modelo_como_diccionario.json",
                "resumen_del_modelo.json"
            ]
        }
        
        archivo_metadatos = os.path.join(output_dir, "metadatos.json")
        with open(archivo_metadatos, 'w', encoding='utf-8') as f:
            json.dump(metadatos, f, indent=2, ensure_ascii=False)
        print(f"   🏷️ Metadatos guardados: {os.path.basename(archivo_metadatos)}")
        
        # =========== CREAR MÚLTIPLES MODELOS ===========
        print("\n📦 Paso 5: Creando múltiples modelos...")
        
        configuraciones = [
            {'L_B_ratio': 1.0, 'B': 8.0, 'nx': 2, 'ny': 2, 'nombre': 'Cuadrado_Pequeño'},
            {'L_B_ratio': 1.5, 'B': 12.0, 'nx': 4, 'ny': 3, 'nombre': 'Rectangular_Mediano'},
            {'L_B_ratio': 2.0, 'B': 15.0, 'nx': 5, 'ny': 3, 'nombre': 'Alargado_Grande'}
        ]
        
        modelos_creados = []
        for i, config in enumerate(configuraciones, 1):
            modelo_var = builder.create_model(
                L_B_ratio=config['L_B_ratio'],
                B=config['B'],
                nx=config['nx'],
                ny=config['ny'],
                enabled_analyses=['static']
            )
            modelos_creados.append(modelo_var)
            print(f"   📄 Modelo {i}: {modelo_var.name} ({config['nombre']})")
        
        # =========== ANALIZAR ARCHIVOS CREADOS ===========
        print("\n📁 Paso 6: Análisis de archivos creados...")
        
        archivos_json = glob.glob(os.path.join(output_dir, "*.json"))
        archivos_json.sort()
        
        print(f"   📂 Total de archivos JSON: {len(archivos_json)}")
        print("   📋 Lista de archivos:")
        
        tamaño_total = 0
        for archivo in archivos_json:
            tamaño = os.path.getsize(archivo)
            tamaño_total += tamaño
            nombre = os.path.basename(archivo)
            print(f"      📄 {nombre:<35} ({tamaño:>6,} bytes)")
        
        print(f"   📏 Tamaño total: {tamaño_total:,} bytes")
        
        # =========== INFORMACIÓN ADICIONAL ===========
        print("\n🔍 Paso 7: Información adicional...")
        
        # Analizar contenido de un archivo
        with open(archivo_original, 'r', encoding='utf-8') as f:
            contenido = json.load(f)
        
        print(f"   📊 Estructura del JSON principal:")
        for seccion in contenido.keys():
            if isinstance(contenido[seccion], dict):
                print(f"      🔸 {seccion}: {len(contenido[seccion])} elementos")
            elif isinstance(contenido[seccion], list):
                print(f"      🔸 {seccion}: {len(contenido[seccion])} elementos")
            else:
                print(f"      🔸 {seccion}: {type(contenido[seccion]).__name__}")
        
        # =========== RESUMEN FINAL ===========
        print("\n🎉 Paso 8: Resumen final...")
        print(f"   ✅ {len(modelos_creados) + 1} modelos estructurales creados")
        print(f"   ✅ {len(archivos_json)} archivos JSON generados")
        print(f"   ✅ Funcionalidades demostradas:")
        print(f"      • Creación automática de JSON")
        print(f"      • Guardado con nombres personalizados")
        print(f"      • Exportación como diccionario")
        print(f"      • Generación de resúmenes")
        print(f"      • Creación de metadatos")
        print(f"      • Análisis de archivos generados")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en ejemplo JSON: {e}")
        print(f"   Tipo: {type(e).__name__}")
        return False


def cleanup():
    """Limpia archivos generados."""
    import shutil
    
    # Obtener la ruta del directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_dir = os.path.join(script_dir, "json_ejemplos")
    
    if os.path.exists(json_dir):
        try:
            shutil.rmtree(json_dir)
            print(f"🧹 Limpiado: {json_dir}")
        except Exception as e:
            print(f"⚠️ Error al limpiar: {e}")


def main():
    """Función principal."""
    
    print("🚀 ModelBuilder - Ejemplo de Archivos JSON")
    print("=" * 50)
    
    # Ejecutar ejemplo
    exito = ejemplo_json_completo()
    
    # Mostrar resultado
    if exito:
        # Obtener ruta del directorio del script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_dir = os.path.join(script_dir, "json_ejemplos")
        
        print("\n" + "=" * 50)
        print("🎉 ¡EJEMPLO COMPLETADO EXITOSAMENTE!")
        print("   Se demostraron todas las funcionalidades de JSON del ModelBuilder.")
        print(f"   Los archivos fueron creados en: {json_dir}")
        
        # Preguntar si limpiar
        print("\n   Los archivos se mantendrán para que puedas revisarlos.")
        print("   Para limpiarlos, ejecuta cleanup() manualmente.")
        
    else:
        print("\n" + "=" * 50)
        print("❌ El ejemplo falló.")
        print("   Revisa las dependencias y la estructura del proyecto.")
    
    return exito


if __name__ == "__main__":
    main()
