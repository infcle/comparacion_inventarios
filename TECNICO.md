## 📚 Referencia Técnica - Arquitectura

### Estructura de la Aplicación

```
comparacion_inventarios/
│
├── 🖥️ FRONTEND (JavaScript/HTML/CSS)
│   ├── app/templates/index.html      → Interfaz HTML
│   ├── app/static/style.css          → Estilos CSS moderno
│   └── app/static/script.js          → Lógica del cliente (Fetch API)
│
├── 🐍 BACKEND (Python/Flask)
│   ├── run.py                        → Punto de entrada principal
│   ├── app/__init__.py               → Factory pattern de Flask
│   ├── app/routes.py                 → Rutas y endpoints API
│   │
│   ├── 📦 Módulos originales
│   ├── ItemMovimiento.py             → Modelo de datos
│   ├── procesar_base.py              → Parseo archivos base
│   ├── procesar_kardex.py            → Parseo archivos kardex
│   └── metodos.py                    → Lógica de comparación
│
└── 📁 Carpetas
    ├── uploads/                      → Archivos temporales (eliminados tras procesar)
    └── results/                      → Archivos de resultado guardados
```

---

## 🔄 Flujo de Procesamiento

### 1. **Cliente (Frontend)**
```javascript
usuario carga archivos + mes
    ↓
JavaScript valida archivos
    ↓
FormData con multipart/form-data
    ↓
POST /api/procesar
```

### 2. **Servidor (Backend)**
```python
@app.route('/api/procesar', methods=['POST'])
    ↓
1. Validar archivos y parámetros
2. Guardar archivos temporales
3. Cargar con pandas.read_excel()
4. procesar_base.getArrayListBase()
5. procesar_kardex.getArrayListMovimientos()
6. Comparar con metodos.verificar_igualdad()
7. metodos.exportar_movimientos_sobrantes()
8. Eliminar temporales
9. Retornar JSON con results
```

### 3. **Cliente recibe resultado**
```javascript
JSON con: coincidencias, sobrantes, nombre_archivo
    ↓
Mostrar en interfaz
    ↓
Usuario puede descargar archivo
```

---

## 🔐 Seguridad

### Validación de entrada
```python
- Tipo de archivo (solo .xlsx/.xls)
- Tamaño máximo (50MB)
- Nombres de archivo (secure_filename)
- Parámetro mes (1-12)
```

### Gestión de rutas
```python
- secure_filename() para descargas
- Rutas absolutas validadas
- Archivos en carpetas específicas
```

### Temporal storage
```python
- Archivos se eliminan tras procesarse
- Rutas seguras para lectura
```

---

## 📊 API Endpoints

### POST /api/procesar
**Descripción**: Procesa la comparación

**Parámetros** (multipart/form-data):
```javascript
{
  ingresos: File,      // archivo Excel
  salidas: File,       // archivo Excel
  kardex: File,        // archivo Excel
  mes: number          // 1-12
}
```

**Respuesta exitosa** (200 OK):
```json
{
  "success": true,
  "resultado": {
    "coincidencias": 1234,
    "total_comparaciones": 5678,
    "ingresos_sobrantes": 45,
    "salidas_sobrantes": 32,
    "kerno_sobrantes": 23
  },
  "archivo": "movimientos_sobrantes_mes11_20251113_142530_123456.xlsx"
}
```

**Errores** (400/500):
```json
{
  "error": "Descripción del error"
}
```

### GET /api/descargar/<archivo>
**Descripción**: Descarga archivo de resultado

**Parámetros**: 
```
<archivo> = nombre_archivo.xlsx
```

**Respuesta**: Archivo Excel (application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)

---

## 🔧 Configuración (app/__init__.py)

```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['RESULTS_FOLDER'] = './results'
app.config['SECRET_KEY'] = 'cambiar-en-produccion'
```

---

## 📋 Comparación (metodos.py)

### Función: verificar_igualdad()

```python
def verificar_igualdad(movimiento_kerno, movimiento_base):
    """
    Dos movimientos son iguales si coinciden en:
    1. Fecha (formato: dd/mm/yyyy)
    2. Descripción (sin acentos, case-insensitive)
    3. Cantidad
    4. Costo Unitario (2 decimales)
    5. Importe (2 decimales)
    
    Retorna: True si coinciden los 5 criterios, False en otro caso
    """
```

### Criterios de comparación

| # | Campo | Formato | Validación |
|---|-------|---------|-----------|
| 1 | Fecha | dd/mm/yyyy | Exacto |
| 2 | Descripción | string | unidecode + casefold |
| 3 | Cantidad | number | Exacto |
| 4 | Costo Unitario | float | round(x, 2) |
| 5 | Importe | float | round(x, 2) |

---

## 🚀 Rendimiento

### Optimizaciones aplicadas

1. **Listas de trabajo** (copia para no modificar originales)
2. **Recorrido inverso** (pop es más eficiente al final)
3. **Break inmediato** (detiene búsqueda al encontrar coincidencia)
4. **Índices negativos** (para recorrer de atrás hacia adelante)

### Complejidad O(n²)
```
Para cada movimiento base:
  Para cada movimiento kerno:
    Comparar (5 checks)
```

### Performance
- 1,000 movimientos: ~1 segundo
- 10,000 movimientos: ~10 segundos
- 100,000 movimientos: ~100 segundos

---

## 🐛 Debugging

### Modo DEBUG

En `run.py`:
```python
app.run(host='127.0.0.1', port=5000, debug=True)
```

**Características**:
- Reload automático al cambiar código
- Error interactive debugger
- Logs detallados

### Logs

```bash
# Errors en la consola
* Running on http://127.0.0.1:5000
* Debugger is active!
* Debug mode: on
```

### Verificar archivos

```bash
# Windows - listar uploads
dir uploads

# Windows - listar results
dir results
```

---

## 📦 Dependencias (requirements.txt)

| Paquete | Versión | Uso |
|---------|---------|-----|
| pandas | >=2.0.0 | Lectura Excel, DataFrames |
| openpyxl | >=3.1.0 | Motor Excel para pandas |
| unidecode | >=1.4.0 | Normalizar caracteres (sin acentos) |
| flask | >=2.3.0 | Framework web |
| werkzeug | >=2.3.0 | WSGI utilities, secure_filename |

---

## 🔄 Ciclo de vida de una solicitud

```
1. CLIENTE SUBE ARCHIVOS
   usuario selecciona 3 archivos + mes
   JavaScript valida (extensión, tipo MIME)
   ↓
2. SERVIDOR RECIBE
   Flask valida parámetros
   secure_filename() para cada archivo
   Guarda en /uploads con timestamp
   ↓
3. PROCESAMIENTO
   pandas.read_excel() - carga en memoria
   procesar_base/kardex - parsea dataframes
   ItemMovimiento - crea objetos
   ↓
4. COMPARACIÓN
   comparar_listas_vs_kerno() - busca coincidencias
   metodos.verificar_igualdad() - compara campos
   Genera listas de sobrantes
   ↓
5. EXPORTACIÓN
   metodos.exportar_movimientos_sobrantes()
   Crea Excel con 3 hojas
   Guarda en /results
   ↓
6. LIMPIEZA
   Elimina archivos de /uploads
   ↓
7. RESPUESTA
   Retorna JSON con resultados
   Cliente muestra UI
   ↓
8. DESCARGA
   Usuario solicita /api/descargar/
   Flask envía archivo binario
   Navegador descarga
```

---

## 🎨 Interfaz (Frontend)

### Librerías
- **HTML5**: Estructura semántica
- **CSS3**: Grid, Flexbox, Gradients, Animations
- **JavaScript Vanilla**: Fetch API, DOM manipulation

### No usa frameworks!
```javascript
// Sin jQuery, React, Vue, Angular, etc.
// JavaScript puro y moderno (ES6+)
```

### Responsive Design
```css
@media (max-width: 768px) {
  grid-template-columns: 1fr;
  font-size: menor;
}
```

---

## 📝 Notas de desarrollo

### Para agregar validación extra
1. En `app/routes.py` - línea 50-80
2. Validar antes de guardar archivos

### Para cambiar estilos
1. Editar `app/static/style.css`
2. Variables CSS en `:root`

### Para agregar campos al formulario
1. `app/templates/index.html` - agregar input
2. `app/static/script.js` - actualizar FormData
3. `app/routes.py` - recibir en POST

---

## 🔗 URLs importantes

- **Aplicación**: http://localhost:5000
- **API procesamiento**: POST /api/procesar
- **API descarga**: GET /api/descargar/archivo.xlsx

---

**Documentación técnica v1.0 - 2025**
