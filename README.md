# Comparación de Inventarios

Proyecto Python para comparar inventarios entre archivos base y un kardex de Kernobi. Además incluye una interfaz web ligera con Flask que permite cargar los archivos desde el navegador, definir el mes y la tolerancia, y descargar el resultado.

## 📋 Resumen rápido

Esta repo contiene dos modos de uso:

- Modo consola: scripts originales que procesan archivos desde la línea de comandos.
- Modo web: aplicación Flask en la carpeta `app/` que permite subir archivos desde un navegador y descargar resultados.

## 📚 Documentación

Enlaces rápidos a la documentación y guías del proyecto:

- **Guía rápida (QuickStart):** [GUIA_RAPIDA.md](GUIA_RAPIDA.md) — pasos breves para ejecutar la aplicación y ejemplos de uso.
- **Interfaz web / UI:** [README_WEB.md](README_WEB.md) — detalles sobre la aplicación Flask, templates, endpoints y comportamiento del front-end.
- **Acceso en red:** [ACCESO_RED.md](ACCESO_RED.md) — cómo exponer la app en la red local, reglas de firewall y comandos útiles.
- **Inicio / Introducción:** [INICIO.md](INICIO.md) — información inicial y contexto (revisar si debe fusionarse con el README principal).
- **Notas técnicas:** [TECNICO.md](TECNICO.md) — detalles para desarrolladores, supuestos, y puntos de integración.

Si alguno de estos archivos está desactualizado, puedo fusionar su contenido en este `README.md` o moverlos a una carpeta `docs/`.

## 🚀 Requisitos

- Python 3.8 o superior
- pip

Instala dependencias:

```cmd
cd e:\Python\comparacion_inventarios
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 📁 Estructura del proyecto (actual)

```estructura
comparacion_inventarios/
├── ACCESO_RED.md            # Instrucciones para exponer la app en red local
├── app/                     # Aplicación Flask (UI web)
│   ├── __init__.py          # Factory de la app
│   ├── routes.py            # Rutas y lógica de subida/procesado/descarga
│   ├── static/              # CSS y JS para la interfaz
│   │   ├── style.css
│   │   └── script.js
│   └── templates/           # Templates Jinja2
│       └── index.html
├── metodos.py               # Funciones de verificación, exportación y utilidades
├── procesar_base.py         # Lógica para procesar archivo base
├── procesar_kardex.py       # Lógica para procesar kardex
├── ItemMovimiento.py        # Clase que representa un movimiento
├── comparar_inventarios.py  # Script original (modo consola)
├── run.py                   # Script para arrancar la app Flask (muestra IP de red)
├── run_network.bat          # Helper Windows para ejecutar la app en red local
├── mostrar_ip.bat           # Helper para mostrar IP local
├── requirements.txt         # Dependencias
├── results/                 # Carpeta donde la app guarda resultados (.xlsx)
├── uploads/                 # Carpeta para uploads temporales
└── README.md                # Este archivo
```

> Nota: puede haber archivos adicionales en la raíz (docs, guías rápidas, .bat, etc.).

## 🖥️ Modo web (Flask)

La interfaz web está en `app/`. Para ejecutarla en tu máquina y permitir acceso desde otros equipos en la misma red:

```cmd
cd e:\Python\comparacion_inventarios
venv\Scripts\activate
python run.py
```

La consola mostrará la `URL Local` y la `URL en Red` (por ejemplo `http://192.168.1.100:5000`). Comparte la `URL en Red` con otros dispositivos de la misma red.

Si prefieres, ejecuta `run_network.bat` para activar el venv y arrancar la app automáticamente.

## ⚙️ Endpoints principales (app Flask)

- `/` : Página principal con formulario para subir los 3 archivos y seleccionar el mes y la tolerancia.
- `POST /api/procesar` : Endpoint que recibe los archivos y el parámetro `mes` y `tolerancia`, procesa y devuelve el nombre del archivo resultado.
- `GET  /api/descargar/<nombre_archivo>` : Descarga el archivo de resultados desde `results/`.

## 🔧 Parámetros en la UI

- `mes`: enviado como número (1-12). En el frontend se muestra como select con nombres de meses.
- `tolerancia`: porcentaje (0-100) que se usa para comparar costo unitario e importe.

## 📝 Formato de archivos

- Archivo Base: Excel (.xlsx) con hoja `Hoja1` (columnas esperadas según implementación original).
- Archivo Kardex: Excel (.xlsx) con hoja `Page 1`.

La comparación se realiza por fecha, descripción (normalizada), cantidad, costo unitario e importe (aplicando tolerancia para costo/importe).

## 💡 Acceso en red y Firewall

- Si no puedes acceder desde otros dispositivos, revisa el firewall de Windows y crea una regla para permitir el puerto (por defecto `5000`). También existe `ACCESO_RED.md` con pasos y `mostrar_ip.bat` para facilitar.

## 🛠️ Desarrollo

- Para depuración local usa `FLASK_ENV=development` o ejecuta `python run.py` con `debug=True` activado en `run.py`.

## 📄 Licencia

Uso interno.

## 👥 Contribuciones

- Usar ramas por feature y enviar PRs.

## 📞 Soporte

- Abrir un issue en el repositorio con logs y pasos para reproducir.
