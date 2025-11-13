# Comparación de Inventarios

Proyecto Python para comparar inventarios entre un archivo base y un archivo kardex de Kernobi. El script procesa archivos Excel y compara los movimientos de inventario basándose en fechas y otros criterios.

## 📋 Descripción

Este proyecto permite:
- Procesar archivos Excel de inventarios
- Comparar movimientos entre un archivo base y un archivo kardex
- Identificar diferencias y coincidencias entre ambos archivos

## 🚀 Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## 📦 Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd comparacion_inventarios
```

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
```

3. Activar el entorno virtual:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

4. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## 🎯 Uso

1. Asegúrate de tener activado el entorno virtual
2. Ejecuta el script principal:
```bash
python comparar_inventarios.py
```

3. El script te pedirá las rutas de los archivos:
   - Ruta del archivo base (debe contener una hoja llamada "Hoja1")
   - Ruta del archivo kardex de Kernobi (debe contener una hoja llamada "Page 1")

## 📁 Estructura del Proyecto

```
comparacion_inventarios/
├── comparar_inventarios.py  # Script principal
├── ItemMovimiento.py         # Clase para representar movimientos de inventario
├── procesar_base.py          # Módulo para procesar el archivo base
├── procesar_kardex.py        # Módulo para procesar el archivo kardex
├── requirements.txt          # Dependencias del proyecto
├── README.md                 # Este archivo
└── .gitignore               # Archivos ignorados por Git
```

## 🔧 Dependencias

- **pandas**: Para manejo de datos y lectura de archivos Excel
- **openpyxl**: Para leer y escribir archivos Excel (.xlsx)

## 📝 Formato de Archivos

### Archivo Base
- Debe ser un archivo Excel (.xlsx)
- Debe contener una hoja llamada "Hoja1"
- Columnas esperadas:
  - Columna 12: Descripción
  - Columna 13: Cantidad
  - Columna 14: Unidad
  - Columna 15: Costo Unitario
  - Columna 16: Importe
  - Columna 5: Fecha

### Archivo Kardex
- Debe ser un archivo Excel (.xlsx)
- Debe contener una hoja llamada "Page 1"
- Columnas esperadas:
  - Columna 2: Descripción
  - Columna 12: Unidad
  - Columna 13: Cantidad
  - Columna 14: Costo Unitario
  - Columna 15: Importe
  - Columna 4: Fecha

## 🛠️ Desarrollo

El proyecto está estructurado en módulos:
- `ItemMovimiento`: Clase que representa un movimiento de inventario con sus atributos
- `procesar_base`: Funciones para procesar el archivo base
- `procesar_kardex`: Funciones para procesar el archivo kardex
- `comparar_inventarios`: Script principal que orquesta la comparación

## 📄 Licencia

Este proyecto es de uso interno.

## 👥 Contribuciones

Para contribuir al proyecto, por favor:
1. Crea una rama para tu feature
2. Realiza tus cambios
3. Envía un pull request

## 📞 Soporte

Para preguntas o problemas, por favor abre un issue en el repositorio.

