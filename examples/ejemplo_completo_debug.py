"""
Ejemplo simple usando ModelBuilder + AnalysisEngine con generación de JSON para debug.

Este ejemplo demuestra el flujo completo: crear modelo → analizar → guardar resultados,
con archivos JSON para facilitar el debug del modelo y los resultados.
"""

import os
import sys
import json
from datetime import datetime

# Para desarrollo: agregar src al path 
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_dir)


def ejemplo_completo_con_debug():
    """Ejemplo completo: ModelBuilder + AnalysisEngine + JSON debug."""
    
    print("🔬 Ejemplo: ModelBuilder + AnalysisEngine + Debug JSON")
    print("=" * 60)
    
    try:
        # =========== IMPORTAR COMPONENTES ===========
        print("📦 Paso 1: Importando componentes...")
        from model_builder import ModelBuilder
        from analysis_engine import AnalysisEngine
        
        # Crear directorio de debug
        script_dir = os.path.dirname(os.path.abspath(__file__))
        debug_dir = os.path.join(script_dir, "debug_modelo")
        os.makedirs(debug_dir, exist_ok=True)
        
        print(f"   ✅ Componentes importados")
        print(f"   📁 Directorio debug: {debug_dir}")
        
        # =========== CREAR MODELO SIMPLE ===========
        print("\n🏗️ Paso 2: Creando modelo estructural...")
        
        builder = ModelBuilder(output_dir=debug_dir)
        
        # Modelo simple para evitar problemas de OpenSees
        modelo = builder.create_model(
            L_B_ratio=1.0,
            B=6.0,
            nx=2,
            ny=2,
            enabled_analyses=['static', 'modal']
        )
        
        print(f"   ✅ Modelo creado: {modelo.name}")
        print(f"   📊 Nodos: {len(modelo.geometry.nodes)}")
        print(f"   📊 Elementos: {len(modelo.geometry.elements)}")
        print(f"   🔧 Análisis habilitados: {modelo.analysis_config.enabled_analyses}")
        
        # =========== GUARDAR MODELO JSON ===========
        print("\n💾 Paso 3: Guardando modelo en JSON...")
        
        # Archivo principal del modelo
        archivo_modelo = os.path.join(debug_dir, f"modelo_{modelo.name}.json")
        modelo.save(archivo_modelo)
        print(f"   📄 Modelo guardado: {os.path.basename(archivo_modelo)}")
        
        # Resumen del modelo para debug
        resumen = builder.get_model_summary(modelo)
        archivo_resumen = os.path.join(debug_dir, f"resumen_{modelo.name}.json")
        with open(archivo_resumen, 'w', encoding='utf-8') as f:
            json.dump(resumen, f, indent=2, ensure_ascii=False)
        print(f"   📊 Resumen guardado: {os.path.basename(archivo_resumen)}")
        
        # Información detallada para debug
        debug_info = {
            "timestamp": datetime.now().isoformat(),
            "modelo_info": {
                "nombre": modelo.name,
                "total_nodos": len(modelo.geometry.nodes),
                "total_elementos": len(modelo.geometry.elements),
                "dimensiones": {
                    "L": resumen['dimensions']['L'],
                    "B": resumen['dimensions']['B'],
                    "altura": resumen['dimensions']['height']
                }
            },
            "configuracion_analisis": {
                "static_config": {
                    "system": modelo.analysis_config.static_config.system,
                    "algorithm": modelo.analysis_config.static_config.algorithm,
                    "integrator": modelo.analysis_config.static_config.integrator,
                    "steps": modelo.analysis_config.static_config.steps
                },
                "modal_config": {
                    "num_modes": modelo.analysis_config.modal_config.num_modes,
                    "frequency_range": [0, 100]
                }
            },
            "nodos_muestra": {},
            "elementos_muestra": {}
        }
        
        # Agregar muestra de nodos (primeros 5)
        for i, (node_id, node) in enumerate(list(modelo.geometry.nodes.items())[:5]):
            debug_info["nodos_muestra"][str(node_id)] = {
                "coords": node.coords,
                "floor": node.floor
            }
        
        # Agregar muestra de elementos (primeros 5)
        for i, (elem_id, elem) in enumerate(list(modelo.geometry.elements.items())[:5]):
            debug_info["elementos_muestra"][str(elem_id)] = {
                "nodes": elem.nodes,
                "type": elem.element_type
            }
        
        archivo_debug = os.path.join(debug_dir, f"debug_info_{modelo.name}.json")
        with open(archivo_debug, 'w', encoding='utf-8') as f:
            json.dump(debug_info, f, indent=2, ensure_ascii=False)
        print(f"   🔍 Debug info guardado: {os.path.basename(archivo_debug)}")
        
        # =========== EJECUTAR ANÁLISIS ===========
        print("\n🚀 Paso 4: Ejecutando análisis...")
        
        engine = AnalysisEngine()
        
        print(f"   🔧 Iniciando análisis del modelo {modelo.name}...")
        resultados = engine.analyze_model(modelo)
        
        if resultados.success:
            print("   ✅ Análisis completado exitosamente")
            
            if resultados.static_results:
                print(f"   📏 Desplazamiento máximo: {resultados.static_results.max_displacement:.6f} m")
                print(f"   ⏱️ Tiempo análisis estático: {resultados.static_results.analysis_time:.3f} s")
                print(f"   🔄 Convergencia: {'Sí' if resultados.static_results.convergence_achieved else 'No'}")
            
            if resultados.modal_results:
                print(f"   🎵 Períodos modales: {len(resultados.modal_results.periods)} modos")
                if resultados.modal_results.periods:
                    print(f"   📊 Primer período: {resultados.modal_results.periods[0]:.3f} s")
            
            print(f"   ⏱️ Tiempo total análisis: {resultados.total_analysis_time:.3f} s")
            
        else:
            print("   ❌ Análisis falló")
            print(f"   🔍 Errores: {resultados.errors}")
        
        # =========== GUARDAR RESULTADOS ===========
        print("\n💾 Paso 5: Guardando resultados...")
        
        # Convertir resultados a diccionario para JSON
        resultados_dict = {
            "timestamp": resultados.timestamp,
            "model_name": resultados.model_name,
            "success": resultados.success,
            "total_analysis_time": resultados.total_analysis_time,
            "errors": resultados.errors
        }
        
        # Agregar resultados estáticos si existen
        if resultados.static_results:
            resultados_dict["static_results"] = {
                "max_displacement": resultados.static_results.max_displacement,
                "max_stress": resultados.static_results.max_stress,
                "convergence_achieved": resultados.static_results.convergence_achieved,
                "num_iterations": resultados.static_results.num_iterations,
                "analysis_time": resultados.static_results.analysis_time
            }
        
        # Agregar resultados modales si existen
        if resultados.modal_results:
            resultados_dict["modal_results"] = {
                "periods": resultados.modal_results.periods,
                "frequencies": resultados.modal_results.frequencies,
                "analysis_time": resultados.modal_results.analysis_time
            }
        
        archivo_resultados = os.path.join(debug_dir, f"resultados_{modelo.name}.json")
        with open(archivo_resultados, 'w', encoding='utf-8') as f:
            json.dump(resultados_dict, f, indent=2, ensure_ascii=False)
        print(f"   📊 Resultados guardados: {os.path.basename(archivo_resultados)}")
        
        # =========== CREAR REPORTE CONSOLIDADO ===========
        print("\n📋 Paso 6: Creando reporte consolidado...")
        
        reporte = {
            "proyecto": {
                "nombre": "Ejemplo ModelBuilder + AnalysisEngine",
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "version": "1.0.0"
            },
            "modelo": {
                "archivo": f"modelo_{modelo.name}.json",
                "nombre": modelo.name,
                "resumen": resumen,
                "configuracion": debug_info["configuracion_analisis"]
            },
            "analisis": {
                "archivo_resultados": f"resultados_{modelo.name}.json",
                "exitoso": resultados.success,
                "tiempo_total": resultados.total_analysis_time,
                "errores": resultados.errors
            },
            "archivos_generados": [
                f"modelo_{modelo.name}.json",
                f"resumen_{modelo.name}.json",
                f"debug_info_{modelo.name}.json",
                f"resultados_{modelo.name}.json",
                "reporte_consolidado.json"
            ],
            "estadisticas": {
                "nodos": len(modelo.geometry.nodes),
                "elementos": len(modelo.geometry.elements),
                "analisis_habilitados": modelo.analysis_config.enabled_analyses,
                "tiempo_creacion_modelo": "< 1s",
                "tiempo_analisis": f"{resultados.total_analysis_time:.3f}s"
            }
        }
        
        if resultados.success and resultados.static_results:
            reporte["resultados_principales"] = {
                "desplazamiento_maximo": f"{resultados.static_results.max_displacement:.6f} m",
                "convergencia": resultados.static_results.convergence_achieved
            }
            
            if resultados.modal_results and resultados.modal_results.periods:
                reporte["resultados_principales"]["primer_periodo"] = f"{resultados.modal_results.periods[0]:.3f} s"
        
        archivo_reporte = os.path.join(debug_dir, "reporte_consolidado.json")
        with open(archivo_reporte, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        print(f"   📋 Reporte consolidado: {os.path.basename(archivo_reporte)}")
        
        # =========== RESUMEN FINAL ===========
        print("\n🎉 Paso 7: Resumen final...")
        
        archivos_creados = [f for f in os.listdir(debug_dir) if f.endswith('.json')]
        tamaño_total = sum(os.path.getsize(os.path.join(debug_dir, f)) for f in archivos_creados)
        
        print(f"   ✅ Ejemplo completado exitosamente")
        print(f"   📁 Archivos creados: {len(archivos_creados)}")
        print(f"   📏 Tamaño total: {tamaño_total:,} bytes")
        print(f"   📊 Análisis: {'Exitoso' if resultados.success else 'Falló'}")
        
        print(f"\n   📂 Archivos en {debug_dir}:")
        for archivo in sorted(archivos_creados):
            tamaño = os.path.getsize(os.path.join(debug_dir, archivo))
            print(f"      📄 {archivo:<30} ({tamaño:>6,} bytes)")
        
        return resultados.success, debug_dir
        
    except Exception as e:
        print(f"❌ Error en ejemplo: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def mostrar_contenido_debug(debug_dir):
    """Muestra contenido de archivos debug para verificación."""
    
    if not debug_dir or not os.path.exists(debug_dir):
        print("❌ Directorio debug no existe")
        return
    
    print(f"\n🔍 CONTENIDO DEBUG: {debug_dir}")
    print("=" * 60)
    
    archivos_json = [f for f in os.listdir(debug_dir) if f.endswith('.json')]
    
    for archivo in sorted(archivos_json):
        ruta = os.path.join(debug_dir, archivo)
        print(f"\n📄 {archivo}:")
        print("-" * 40)
        
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido = json.load(f)
            
            if archivo.startswith('modelo_'):
                print(f"   📊 Modelo: {contenido.get('name', 'N/A')}")
                print(f"   🔗 Nodos: {len(contenido.get('geometry', {}).get('nodes', {}))}")
                print(f"   📦 Elementos: {len(contenido.get('geometry', {}).get('elements', {}))}")
                
            elif archivo.startswith('resultados_'):
                print(f"   ✅ Éxito: {contenido.get('success', False)}")
                print(f"   ⏱️ Tiempo: {contenido.get('total_analysis_time', 0):.3f}s")
                if contenido.get('static_results'):
                    print(f"   📏 Despl. máx: {contenido['static_results'].get('max_displacement', 0):.6f}m")
                
            elif archivo.startswith('debug_info_'):
                print(f"   🔍 Timestamp: {contenido.get('timestamp', 'N/A')}")
                print(f"   📐 Dimensiones: {contenido.get('modelo_info', {}).get('dimensiones', {})}")
                
            elif archivo == 'reporte_consolidado.json':
                print(f"   📋 Proyecto: {contenido.get('proyecto', {}).get('nombre', 'N/A')}")
                print(f"   📊 Archivos: {len(contenido.get('archivos_generados', []))}")
                
            else:
                print(f"   📄 Claves principales: {list(contenido.keys())}")
                
        except Exception as e:
            print(f"   ❌ Error leyendo archivo: {e}")


def main():
    """Función principal."""
    
    print("🚀 Ejemplo Completo: ModelBuilder + AnalysisEngine + Debug")
    print("=" * 60)
    
    # Ejecutar ejemplo
    exito, debug_dir = ejemplo_completo_con_debug()
    
    if exito:
        print("\n" + "=" * 60)
        print("🎉 ¡EJEMPLO COMPLETADO EXITOSAMENTE!")
        print("   Se demostró el flujo completo: modelo → análisis → JSON debug")
        
        # Mostrar contenido debug
        mostrar_contenido_debug(debug_dir)
        
        print(f"\n📁 Todos los archivos están en: {debug_dir}")
        print("   Úsalos para debug del modelo y verificación de resultados.")
        
    else:
        print("\n" + "=" * 60)
        print("❌ El ejemplo falló.")
        print("   Revisa los errores arriba para identificar el problema.")
    
    return exito


if __name__ == "__main__":
    main()
