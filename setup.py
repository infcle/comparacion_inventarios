#!/usr/bin/env python
"""
Script de instalación y verificación de dependencias
"""
import sys
import subprocess
import os

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python_version():
    """Verifica que Python sea 3.7 o superior"""
    version = sys.version_info
    print_header("✓ VERIFICACIÓN DE PYTHON")
    print(f"  Versión Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("  ✗ ERROR: Se requiere Python 3.7 o superior")
        sys.exit(1)
    print("  ✓ Versión compatible")

def check_dependencies():
    """Verifica dependencias requeridas"""
    print_header("✓ VERIFICACIÓN DE DEPENDENCIAS")
    
    required = ['pandas', 'openpyxl', 'unidecode', 'flask', 'werkzeug']
    
    for package in required:
        try:
            __import__(package)
            print(f"  ✓ {package} instalado")
        except ImportError:
            print(f"  ✗ {package} NO instalado")
            return False
    
    return True

def install_dependencies():
    """Instala las dependencias del proyecto"""
    print_header("📦 INSTALANDO DEPENDENCIAS")
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', 
            '-r', 'requirements.txt', '--upgrade'
        ])
        print("\n  ✓ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError:
        print("\n  ✗ Error al instalar dependencias")
        return False

def check_folder_structure():
    """Verifica estructura de carpetas"""
    print_header("📁 VERIFICACIÓN DE ESTRUCTURA")
    
    required_folders = [
        'app',
        'app/templates',
        'app/static',
        'uploads',
        'results'
    ]
    
    required_files = [
        'run.py',
        'app/__init__.py',
        'app/routes.py',
        'app/templates/index.html',
        'app/static/style.css',
        'app/static/script.js',
        'requirements.txt'
    ]
    
    all_ok = True
    
    print("\n  Carpetas:")
    for folder in required_folders:
        if os.path.exists(folder):
            print(f"    ✓ {folder}")
        else:
            print(f"    ✗ {folder} - FALTA")
            all_ok = False
    
    print("\n  Archivos:")
    for file in required_files:
        if os.path.exists(file):
            print(f"    ✓ {file}")
        else:
            print(f"    ✗ {file} - FALTA")
            all_ok = False
    
    return all_ok

def test_imports():
    """Prueba que todos los módulos se importan correctamente"""
    print_header("🧪 PRUEBA DE IMPORTACIONES")
    
    try:
        print("  Importando módulos...")
        from app import create_app
        import procesar_base
        import procesar_kardex
        import metodos
        import ItemMovimiento
        
        print("  ✓ Flask app factory")
        print("  ✓ procesar_base")
        print("  ✓ procesar_kardex")
        print("  ✓ metodos")
        print("  ✓ ItemMovimiento")
        
        print("\n  Creando aplicación...")
        app = create_app()
        print("  ✓ Aplicación creada correctamente")
        
        return True
    except Exception as e:
        print(f"\n  ✗ Error: {str(e)}")
        return False

def main():
    """Función principal"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║   Comparador de Inventarios - Instalación v1.0    ║")
    print("╚════════════════════════════════════════════════════╝")
    
    # Verificar Python
    check_python_version()
    
    # Verificar estructura
    if not check_folder_structure():
        print("\n⚠️  ADVERTENCIA: Falta alguna estructura de carpetas")
        print("   Contacta con el equipo de desarrollo")
        return False
    
    # Instalar dependencias
    if not check_dependencies():
        print("\n📦 Instalando dependencias...")
        if not install_dependencies():
            print("\n✗ Error fatal: No se pueden instalar dependencias")
            return False
    else:
        print("\n  ✓ Todas las dependencias ya están instaladas")
    
    # Prueba de importaciones
    if not test_imports():
        print("\n✗ Error: No se pueden importar los módulos")
        return False
    
    # Éxito
    print_header("✅ INSTALACIÓN COMPLETADA")
    print("""
  🎉 ¡Todo está listo para comenzar!
  
  Para ejecutar la aplicación:
  
    python run.py
    
  Luego abre: http://localhost:5000
  
  Para usar el script rápido en Windows:
  
    iniciar.bat
    """)
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
