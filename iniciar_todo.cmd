@echo off
set "JAVA_HOME="
FOR /D %%i IN ("C:\Program Files\Java\jdk*") DO set "JAVA_HOME=%%i"
if "%JAVA_HOME%"=="" (
    echo [ADVERTENCIA] No se encontro un JDK en C:\Program Files\Java\jdk*. El build podria fallar.
) else (
    echo Usando JAVA_HOME detectado: %JAVA_HOME%
)
cd /d "%~dp0"
echo =======================================================
echo =        SISTEMA DONATON - DEPLOY AUTOMATIZADO        =
echo =======================================================

echo.
echo [1/4] CERRANDO PROCESOS PREVIOS...
taskkill /F /IM java.exe >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo.
echo [2/4] COMPILANDO MICROSERVICIOS...
echo Compilando auth-service...
cd auth-service
call mvnw.cmd clean install -DskipTests
if errorlevel 1 ( echo ERROR COMPILANDO AUTH-SERVICE && pause && exit /b 1 )
cd ..

echo Compilando user-service...
cd user-service
call mvnw.cmd clean install -DskipTests
if errorlevel 1 ( echo ERROR COMPILANDO USER-SERVICE && pause && exit /b 1 )
cd ..

echo Compilando necesidades...
cd necesidades
call mvnw.cmd clean install -DskipTests
if errorlevel 1 ( echo ERROR COMPILANDO NECESIDADES && pause && exit /b 1 )
cd ..

echo Compilando stock...
cd stock
call mvnw.cmd clean install -DskipTests
if errorlevel 1 ( echo ERROR COMPILANDO STOCK && pause && exit /b 1 )
cd ..

echo Preparando match-service (Python)...
cd match-service
if not exist "venv" (
    python -m venv venv
)
venv\Scripts\python.exe -m pip install -r requirements.txt
cd ..

echo.
echo [3/4] INICIANDO SERVICIOS EN SEGUNDO PLANO...
if "%JAVA_HOME%"=="" (
    set "JAVA_CMD=java"
) else (
    set "JAVA_CMD="%JAVA_HOME%\bin\java.exe""
)

echo Usando ejecutable Java: %JAVA_CMD%
echo Iniciando Auth (8081), User (8082), Necesidades (8083), Stock (8084) e IA (8000)...
start "Auth-Service" cmd /k "cd auth-service\target && %JAVA_CMD% -jar auth-service-0.0.1-SNAPSHOT.jar"
start "User-Service" cmd /k "cd user-service\target && %JAVA_CMD% -jar user-service-0.0.1-SNAPSHOT.jar"
start "Necesidades-Service" cmd /k "cd necesidades\target && %JAVA_CMD% -jar necesidades-0.0.1-SNAPSHOT.jar"
start "Stock-Service" cmd /k "cd stock\target && %JAVA_CMD% -jar stock-0.0.1-SNAPSHOT.jar"
start "Match-IA" cmd /k "cd match-service && call venv\Scripts\activate.bat && python app.py"

echo.
echo Esperando 30 segundos para que todos los servicios inicien y se creen las tablas en BD...
timeout /t 30 /nobreak

echo.
echo [4/4] POBLANDO BASE DE DATOS (SEEDER)...
match-service\venv\Scripts\python.exe seed_db.py

echo.
echo =======================================================
echo = ECOSISTEMA COMPLETAMENTE OPERATIVO Y CON DATOS      =
echo =======================================================
echo.
echo Accesos directos a Swagger:
echo [Auth]        http://localhost:8081/swagger-ui/index.html
echo [User]        http://localhost:8082/swagger-ui/index.html
echo [Necesidades] http://localhost:8083/swagger-ui/index.html
echo [Stock]       http://localhost:8084/swagger-ui/index.html
echo [Match IA]    http://localhost:8000/docs
echo.
echo Para detener todos los servicios de emergencia, puedes cerrar esta consola o presionar CTRL+C.
pause
