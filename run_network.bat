@echo off
REM Script para ejecutar la aplicación en modo red local
REM La aplicación será accesible desde otras máquinas en la misma red

cls
echo.
echo =====================================================
echo  Comparador de Inventarios - Modo Red Local
echo =====================================================
echo.

REM Cambiar al directorio del proyecto
cd /d "%~dp0"

REM Verificar si existe el entorno virtual
if not exist "venv\Scripts\activate.bat" (
    echo.
    echo ERROR: Entorno virtual no encontrado.
    echo Por favor, crea primero el entorno con: python -m venv venv
    echo.
    pause
    exit /b 1
)

REM Activar el entorno virtual
call venv\Scripts\activate.bat

REM Ejecutar la aplicación
echo.
echo Iniciando la aplicación Flask...
echo.
python run.py

pause
