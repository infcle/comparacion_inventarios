# 🚀 Guía Rápida - Comparador de Inventarios

## ⚡ Inicio Rápido (5 minutos)

### Opción 1: Usar el script de inicio (Recomendado - Windows)

1. **Abre el explorador de archivos** y ve a la carpeta del proyecto
2. **Haz doble clic** en `iniciar.bat`
3. La aplicación se abrirá automáticamente en `http://localhost:5000`

### Opción 2: Inicio manual

```bash
# 1. Abre cmd en la carpeta del proyecto

# 2. Crear entorno virtual (primera vez)
python -m venv venv

# 3. Activar entorno
venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar la aplicación
python run.py
```

## 🎯 Cómo usar la aplicación

### Paso 1️⃣: Preparar tus archivos
- Asegúrate de tener 3 archivos Excel (.xlsx):
  - `base_ingresos.xlsx` (hoja: "Hoja1")
  - `base_salidas.xlsx` (hoja: "Hoja1")
  - `kardex.xlsx` (hoja: "Page 1")

### Paso 2️⃣: Cargar los archivos
1. Abre la interfaz web en `http://localhost:5000`
2. Haz clic en cada campo para seleccionar los archivos
3. Ingresa el **mes** (1-12) que deseas comparar

### Paso 3️⃣: Procesar
- Haz clic en **"🚀 Procesar Archivos"**
- Espera a que se complete (normalmente 1-2 segundos)

### Paso 4️⃣: Descargar resultados
- Verás los **resultados** en la pantalla:
  - ✅ Coincidencias encontradas
  - ➕ Ingresos sobrantes
  - ➖ Salidas sobrantes
  - ⚠️ Kardex sobrantes
- Haz clic en **"⬇️ Descargar Archivo Excel"**

## 📊 Interpretación de resultados

El archivo descargado tiene 3 hojas:

| Hoja | Contenido |
|------|-----------|
| **Ingresos** | Movimientos de ingresos del archivo base que NO coincidieron |
| **Salidas** | Movimientos de salidas del archivo base que NO coincidieron |
| **Kerno Sobrantes** | Movimientos del kardex Kernobi que NO coincidieron |

## 🔍 ¿Qué significa "coincidencia"?

Dos movimientos son iguales si coinciden en:
- 📅 **Fecha** (día/mes/año)
- 📝 **Descripción** (sin importar acentos o mayúsculas)
- 🔢 **Cantidad**
- 💵 **Costo Unitario**
- 💰 **Importe Total**

## ❓ Preguntas frecuentes

### ❌ Error: "Falta archivo de ingresos"
**Solución**: Asegúrate de seleccionar todos los 3 archivos

### ❌ Error: "No se ha podido resolver la importación 'flask'"
**Solución**: Ejecuta `pip install flask werkzeug`

### ❌ Error: "No sheet named 'Hoja1'"
**Solución**: Verifica que el archivo Excel tenga una hoja exactamente llamada "Hoja1"

### ❌ El puerto 5000 está en uso
**Solución**: Cambia el puerto en `run.py` (línea: `port = 5000`)

### ❓ ¿Cómo cambio el puerto?
Abre `run.py` y cambia:
```python
port = int(os.environ.get('PORT', 5000))  # Cambia 5000 por otro puerto
```

## 📱 Acceso desde otra computadora

Si quieres acceder desde otra computadora en la red:

1. Abre `run.py` y cambia:
```python
app.run(host='127.0.0.1', port=port, debug=debug)
# A:
app.run(host='0.0.0.0', port=port, debug=debug)
```

2. Encuentra tu IP:
```bash
ipconfig
# Busca "Dirección IPv4" bajo "Adaptador de Ethernet"
```

3. Accede desde otra PC: `http://tu-ip:5000`

## 🛠️ Archivos importantes

| Archivo | Propósito |
|---------|-----------|
| `run.py` | Script principal para ejecutar la app |
| `iniciar.bat` | Batch para Windows (inicio rápido) |
| `app/__init__.py` | Configuración de Flask |
| `app/routes.py` | Lógica de la API |
| `app/templates/index.html` | Interfaz del usuario |
| `app/static/style.css` | Estilos CSS |
| `app/static/script.js` | Lógica del navegador |

## 📞 Soporte

- **Error desconocido**: Revisa la terminal donde ejecutaste `run.py`
- **Archivo no se descarga**: Verifica que tu navegador permite descargas automáticas
- **¿Más ayuda?**: Consulta `README_WEB.md` para más detalles

---

**¡Listo para usar! 🎉**
