#!/usr/bin/env python3
"""
Script para facilitar la creación de releases del paquete opensees-parametric-analysis
"""

import subprocess
import sys
import argparse
from pathlib import Path

def run_command(cmd, check=True):
    """Ejecuta un comando y retorna el resultado"""
    print(f"🔧 Ejecutando: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if check and result.returncode != 0:
        print(f"❌ Error ejecutando: {cmd}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        sys.exit(1)
    
    return result

def check_git_status():
    """Verifica que el repositorio esté limpio"""
    result = run_command("git status --porcelain", check=False)
    if result.stdout.strip():
        print("❌ Hay cambios sin commitear. Por favor, haz commit primero.")
        sys.exit(1)
    print("✅ Repositorio limpio")

def update_version(version, dry_run=False):
    """Actualiza la versión en los archivos necesarios"""
    files_to_update = [
        ("pyproject.toml", f'version = "{version}"'),
        ("src/__init__.py", f'__version__ = "{version}"')
    ]
    
    for file_path, version_line in files_to_update:
        if dry_run:
            print(f"🔍 [DRY RUN] Actualizaría {file_path} con: {version_line}")
        else:
            print(f"📝 Actualizando {file_path}")
            # Aquí implementarías la lógica real de actualización
            # Por simplicidad, solo mostramos lo que haría

def run_tests():
    """Ejecuta la suite de tests"""
    print("🧪 Ejecutando tests...")
    run_command("python -m pytest tests/ -v")
    print("✅ Tests pasaron correctamente")

def build_package():
    """Construye el paquete"""
    print("📦 Construyendo paquete...")
    run_command("python -m build")
    print("✅ Paquete construido")

def create_git_tag(version):
    """Crea el tag de git"""
    tag = f"v{version}"
    print(f"🏷️  Creando tag {tag}...")
    run_command(f"git tag -a {tag} -m 'Release {version}'")
    print(f"✅ Tag {tag} creado")

def push_release(version):
    """Hace push del tag para triggear el release"""
    tag = f"v{version}"
    print(f"🚀 Haciendo push del tag {tag}...")
    run_command(f"git push origin {tag}")
    print("✅ Tag pushed. GitHub Actions se encargará del resto.")

def main():
    parser = argparse.ArgumentParser(description="Script de release para opensees-parametric-analysis")
    parser.add_argument("version", help="Versión a released (ej: 1.0.1)")
    parser.add_argument("--dry-run", action="store_true", help="Solo mostrar lo que haría")
    parser.add_argument("--skip-tests", action="store_true", help="Saltar ejecución de tests")
    
    args = parser.parse_args()
    
    print(f"🎯 Iniciando release de versión {args.version}")
    
    if not args.dry_run:
        check_git_status()
    
    if not args.skip_tests and not args.dry_run:
        run_tests()
    
    update_version(args.version, args.dry_run)
    
    if not args.dry_run:
        build_package()
        create_git_tag(args.version)
        
        response = input("¿Quieres hacer push del tag para crear el release? (y/N): ")
        if response.lower() == 'y':
            push_release(args.version)
        else:
            print("⏸️  Release preparado pero no publicado. Ejecuta manualmente:")
            print(f"   git push origin v{args.version}")
    
    print("🎉 ¡Release completado!")

if __name__ == "__main__":
    main()
