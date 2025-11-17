# 📊 Comparador de Inventarios - Versión Web

Aplicación web para comparar inventarios entre archivos base y kardex Kernobi. Interfaz gráfica construida con **Flask** y **JavaScript moderno**.

## 🎯 Características

- ✅ **Interfaz Web Intuitiva**: Carga archivos directamente desde el navegador
- 📊 **Comparación Automática**: Compara movimientos de ingresos, salidas y kardex
- 📥 **Descarga de Resultados**: Genera un archivo Excel con los movimientos sobrantes
- 🚀 **Procesamiento Rápido**: Algoritmo optimizado de comparación
- 📱 **Responsive**: Funciona en computadoras y tablets
- 🎨 **Diseño Moderno**: Interfaz atractiva y fácil de usar

## 📋 Requisitos

- **Python 3.7** o superior
- **pip** (gestor de paquetes de Python)

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd comparacion_inventarios
```

### 2. Crear entorno virtual (recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 🎯 Uso

### Ejecutar la aplicación

```bash
python run.py
```

Luego abre tu navegador en: **http://localhost:5000**

### Pasos para comparar inventarios

1. **Selecciona el archivo de INGRESOS base** (Excel con hoja "Hoja1")
2. **Selecciona el archivo de SALIDAS base** (Excel con hoja "Hoja1")
3. **Selecciona el archivo KARDEX Kernobi** (Excel con hoja "Page 1")
4. **Ingresa el mes** a comparar (1-12)
5. **Haz clic en "Procesar Archivos"**
6. **Descarga el resultado** en Excel

## 📁 Estructura del Proyecto

```
comparacion_inventarios/
├── app/
│   ├── __init__.py              # Factory de la aplicación Flask
│   ├── routes.py                # Rutas y lógica de la API
│   ├── templates/
│   │   └── index.html           # Página principal
│   └── static/
│       ├── style.css            # Estilos CSS
│       └── script.js            # Lógica del navegador
├── uploads/                     # Carpeta temporal para archivos subidos
├── results/                     # Carpeta donde se guardan los resultados
├── comparar_inventarios.py      # Script original (CLI)
├── ItemMovimiento.py            # Clase de modelo
├── procesar_base.py             # Procesamiento de archivos base
├── procesar_kardex.py           # Procesamiento de kardex
├── metodos.py                   # Métodos de comparación
├── run.py                       # Archivo para ejecutar la app
├── requirements.txt             # Dependencias
└── README.md                    # Este archivo
```

## 🔧 Configuración

### Variables de entorno (opcional)

```bash
# Puerto de la aplicación (default: 5000)
set FLASK_PORT=5000

# Modo de desarrollo (default: development)
set FLASK_ENV=development
```

## 📦 Dependencias

| Paquete | Versión | Propósito |
|---------|---------|----------|
| **pandas** | >=2.0.0 | Lectura y procesamiento de Excel |
| **openpyxl** | >=3.1.0 | Lectura/escritura de archivos .xlsx |
| **unidecode** | >=1.4.0 | Manejo de caracteres especiales |
| **flask** | >=2.3.0 | Framework web |
| **werkzeug** | >=2.3.0 | Utilidades de WSGI |

## 📝 Formato de Archivos Esperados

### Archivo Base (Ingresos/Salidas)
- **Extensión**: .xlsx
- **Hoja requerida**: "Hoja1"
- **Columnas esperadas**:
  - Col 5: Fecha
  - Col 7: Operación
  - Col 11: Código
  - Col 12: Descripción
  - Col 13: Cantidad
  - Col 14: Unidad
  - Col 15: Costo Unitario
  - Col 16: Importe

### Archivo Kardex Kernobi
- **Extensión**: .xlsx
- **Hoja requerida**: "Page 1"
- **Columnas esperadas**:
  - Col 1: Código
  - Col 2: Descripción
  - Col 4: Fecha
  - Col 7: Operación
  - Col 8: Movimiento
  - Col 12: Unidad
  - Col 13: Cantidad
  - Col 14: Costo Unitario
  - Col 15: Importe

## 📊 Interpretación de Resultados

La aplicación genera un archivo Excel con 3 hojas:

1. **Ingresos**: Movimientos de ingresos del archivo base que no coincidieron
2. **Salidas**: Movimientos de salidas del archivo base que no coincidieron
3. **Kerno Sobrantes**: Movimientos del kardex Kernobi que no coincidieron

### Criterios de Coincidencia

Dos movimientos se consideran iguales si coinciden en:
- ✓ Fecha (dd/mm/yyyy)
- ✓ Descripción (sin acentos, sin mayúsculas/minúsculas)
- ✓ Cantidad
- ✓ Costo Unitario (2 decimales)
- ✓ Importe (2 decimales)

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"
```bash
pip install flask werkzeug
```

### Error: "No sheet named 'Hoja1'"
Verifica que el archivo Excel tenga la hoja con el nombre exacto (sensible a mayúsculas).

### Error: "File is not a valid Excel file"
Asegúrate de que los archivos son .xlsx válidos y no están corruptos.

### Puerto 5000 en uso
```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000
```

## 📈 Optimizaciones

- Carga asíncrona de archivos
- Procesamiento eficiente con listas de trabajo
- Eliminación automática de archivos temporales
- Interfaz responsive y moderna

## 🛠️ Desarrollo

### Estructura del código

- **Backend** (Python/Flask): Procesa datos, compara movimientos, genera Excel
- **Frontend** (HTML/CSS/JS): Interfaz de usuario, manejo de eventos, descarga de archivos

### Extensiones futuras

- [ ] Validación de archivos antes de procesar
- [ ] Mostrar vista previa de datos
- [ ] Historial de comparaciones
- [ ] Exportar a otros formatos (CSV, PDF)
- [ ] Autenticación de usuarios
- [ ] Base de datos para guardar histórico

## 📞 Soporte

Para reportar problemas o sugerencias, abre un issue en el repositorio.

## 📄 Licencia

Proyecto de uso interno.

## 👥 Versiones

- **v1.0** (Actual): Lanzamiento de versión web con Flask
- **v0.1**: Script CLI original en Python

---

**Desarrollado con ❤️ - 2025**
