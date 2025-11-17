
@echo off
REM Script rápido para mostrar la IP local y cómo acceder

echo.
echo ======================================
echo  Tu IP Local
echo ======================================
echo.

for /f "tokens=2 delims=:" %%a in ('ipconfig ^| find "IPv4"') do (
    echo %%a
)

echo.
echo ======================================
echo  Cómo acceder desde otro dispositivo:
echo ======================================
echo.
echo 1. Copia la IP de arriba
echo 2. En el otro dispositivo, abre el navegador
echo 3. Ingresa: http://[IP_COPIADA]:5000
echo.
echo Ejemplo: http://192.168.1.100:5000
echo.
pause
