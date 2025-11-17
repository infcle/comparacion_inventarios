#!/usr/bin/env python
"""
Script principal para ejecutar la aplicación Flask.
Expone la aplicación en la red local.
"""
import os
import sys
import socket
from app import create_app

# Función para obtener la IP local
def obtener_ip_local():
    """Obtiene la dirección IP local de la máquina."""
    try:
        # Crear un socket para conectar a un servidor externo
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    # Ejecutar la aplicación
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    # Obtener IP local
    ip_local = obtener_ip_local()
    
    print("\n" + "="*70)
    print("🚀 Comparador de Inventarios - Flask App")
    print("="*70)
    print(f"📍 URL Local:     http://localhost:{port}")
    print(f"📍 URL en Red:    http://{ip_local}:{port}")
    print(f"🔧 Modo:          {'DEBUG' if debug else 'PRODUCCIÓN'}")
    print("="*70)
    print("\n💡 Comparte esta URL con otros en tu red:")
    print(f"   http://{ip_local}:{port}\n")
    print("="*70 + "\n")
    
    # Ejecutar en todas las interfaces (0.0.0.0)
    app.run(host='0.0.0.0', port=port, debug=debug)
