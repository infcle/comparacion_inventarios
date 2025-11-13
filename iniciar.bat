@echo off
REM Script para instalar dependencias e iniciar la aplicación
REM Compatibilidad: Windows CMD

echo.
echo ===============================================
echo Comparador de Inventarios - Configuracion
echo ===============================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado o no está en el PATH
    echo Descargalo desde https://www.python.org/
    pause
    exit /b 1
)

echo [+] Python encontrado
python --version

REM Crear venv si no existe
if not exist venv (
    echo.
    echo [*] Creando entorno virtual...
    python -m venv venv
    echo [+] Entorno virtual creado
)

REM Activar venv
echo.
echo [*] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error al activar el entorno virtual
    pause
    exit /b 1
)
echo [+] Entorno virtual activado

REM Instalar dependencias
echo.
echo [*] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error al instalar dependencias
    pause
    exit /b 1
)
echo [+] Dependencias instaladas

REM Iniciar la aplicación
echo.
echo ===============================================
echo [+] Iniciando aplicación...
echo ===============================================
echo.
echo Abre tu navegador en: http://localhost:5000
echo Presiona Ctrl+C para detener la aplicación
echo.
python run.py

pause
