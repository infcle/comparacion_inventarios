# 🌐 Acceso Red Local - Comparador de Inventarios

## Cómo exponer la aplicación en tu red local

### Opción 1: Ejecutar directamente (Recomendado)

```bash
cd e:\Python\comparacion_inventarios
python run.py
```

La aplicación mostrará automáticamente:
- 📍 **URL Local**: `http://localhost:5000`
- 📍 **URL en Red**: `http://TU_IP:5000`

### Opción 2: Usar el script batch

Simplemente haz doble clic en:
```
run_network.bat
```

---

## 📱 Acceder desde otro dispositivo

### Desde otra computadora o móvil en la misma red:

1. **Obtén tu IP local ejecutando el servidor**:
   - La IP aparecerá en la consola cuando inicies `python run.py`
   - Ejemplo: `http://192.168.1.100:5000`

2. **Accede desde el navegador del otro dispositivo**:
   ```
   http://192.168.1.100:5000
   ```

### Encontrar tu IP manualmente:

**En Windows:**
```cmd
ipconfig
```
Busca "IPv4 Address" en la sección de tu conexión de red.

**En Linux/Mac:**
```bash
ifconfig
# o
hostname -I
```

---

## 🔧 Configuración del Firewall

Si no puedes acceder desde otros dispositivos:

### Windows Defender Firewall:

1. Ve a **Panel de Control → Firewall de Windows Defender**
2. Click en **Permitir una aplicación a través del Firewall**
3. Busca **Python** y asegúrate de que esté marcado para redes privadas
4. O crea una regla nueva:
   - Puerto: **5000**
   - Protocolo: **TCP**
   - Tipo: **Entrada**

### Alternativa (PowerShell como Admin):
```powershell
New-NetFirewallRule -DisplayName "Flask App 5000" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

---

## 🚀 Cambiar el puerto

Si el puerto 5000 está ocupado, puedes cambiar el puerto:

```cmd
set PORT=8080
python run.py
```

O en Linux/Mac:
```bash
export PORT=8080
python run.py
```

---

## ⚠️ Notas de Seguridad

- ✅ Esta configuración es segura **solo en redes locales privadas**
- ❌ **NO exponer en Internet** sin autenticación
- Para producción, usa un servidor como Gunicorn o Waitress:
  ```bash
  pip install waitress
  waitress-serve --port=5000 --host=0.0.0.0 app:create_app()
  ```

---

## 🆘 Troubleshooting

### No puedo acceder desde otro dispositivo:

1. **Verifica la IP del servidor**: Debe ser una IP privada (192.168.x.x, 10.x.x.x, etc.)
2. **Verifica que estén en la misma red**: Ambos dispositivos deben conectarse al mismo WiFi/Ethernet
3. **Desactiva VPN**: Las VPNs pueden bloquear la comunicación local
4. **Verifica el Firewall**: Windows podría bloquear Flask
5. **Prueba con localhost primero**: `http://localhost:5000`

### Error de conexión rechazada:

- La aplicación no está corriendo
- El puerto no es accesible desde fuera
- Firewall bloqueando la conexión

### Página en blanco o errores:

- Verifica que los archivos CSS/JS están cargando correctamente
- Abre la consola del navegador (F12) para ver errores
- Revisa los logs en la terminal del servidor

---

## 📊 Ejemplo de uso en red

**Máquina Servidor (tu PC):**
```
IP: 192.168.1.100
Puerto: 5000
URL: http://192.168.1.100:5000
```

**Máquina Cliente (otro PC/móvil):**
- Abre navegador
- Ingresa: `http://192.168.1.100:5000`
- ¡Listo! Accedes a la aplicación

---

## 📝 Configuración Persistente

Para cambios permanentes, edita el archivo `run.py`:

```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

Parámetros:
- `host='0.0.0.0'` - Accesible desde cualquier interfaz de red
- `port=5000` - Puerto (cambiar si está ocupado)
- `debug=True` - Modo desarrollo (recarga automática)

---

¡Ahora puedes compartir tu aplicación con otros en tu red! 🎉
