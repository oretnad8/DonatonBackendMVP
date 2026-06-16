@echo off
echo ==============================================
echo = Compiling Microservices for Donaton Project=
echo ==============================================

echo.
echo Building Auth Service...
cd auth-service
call mvnw.cmd clean install -DskipTests
cd ..

:: Pausa de 3 segundos para evitar error 429 (Too Many Requests) de Maven Central
timeout /t 3 /nobreak >nul

echo.
echo Building User Service...
cd user-service
call mvnw.cmd clean install -DskipTests
cd ..

timeout /t 3 /nobreak >nul

echo.
echo Building Necesidades Service...
cd necesidades
call mvnw.cmd clean install -DskipTests
cd ..

timeout /t 3 /nobreak >nul

echo.
echo Building Stock Service...
cd stock
call mvnw.cmd clean install -DskipTests
cd ..

echo.
echo Setting up Match Service (Python)...
cd match-service
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)
echo Instalando dependencias de Python (FastAPI, etc)...
call venv\Scripts\python.exe -m pip install -r requirements.txt

echo Creando script de inicio para Match Service...
echo @echo off > run_match.cmd
echo echo Iniciando Match Service con entorno virtual... >> run_match.cmd
echo call venv\Scripts\activate.bat >> run_match.cmd
echo python app.py >> run_match.cmd
echo pause >> run_match.cmd

cd ..

echo.
echo ===================================================
echo = Build completed! Jars are in target/ folders    =
echo = Match Service virtual environment is configured =
echo ===================================================
echo Para ejecutar el servidor Python, ve a la carpeta match-service y ejecuta run_match.cmd
pause
