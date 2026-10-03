@echo off
cd /d "%~dp0"
py -3.13 -m venv .venv
if errorlevel 1 goto falha
if exist wheelhouse (
 .venv\Scripts\python.exe -m pip install --no-index --find-links=wheelhouse -r requirements-windows.lock
) else (
 .venv\Scripts\python.exe -m pip install -r requirements-windows.lock
)
if errorlevel 1 goto falha
echo Instalacao concluida. Execute INICIAR-WINDOWS.bat.
pause
exit /b 0
:falha
echo Falha. Instale Python 3.13 de 64 bits e consulte LEIA-ME-WINDOWS.md.
pause
exit /b 1
