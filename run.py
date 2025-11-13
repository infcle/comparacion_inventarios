#!/usr/bin/env python
"""
Script principal para ejecutar la aplicación Flask.
"""
import os
import sys
from app import create_app

# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    # Ejecutar la aplicación
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    print("\n" + "="*60)
    print("🚀 Comparador de Inventarios - Flask App")
    print("="*60)
    print(f"📍 URL: http://localhost:{port}")
    print(f"🔧 Modo: {'DEBUG' if debug else 'PRODUCCIÓN'}")
    print("="*60 + "\n")
    
    app.run(host='127.0.0.1', port=port, debug=debug)
