@echo off
set "JAVA_HOME=C:\Program Files\Java\jdk-26.0.1"
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
call mvnw.cmd clean install -DskipTests >nul 2>&1
cd ..

echo Compilando user-service...
cd user-service
call mvnw.cmd clean install -DskipTests >nul 2>&1
cd ..

echo Compilando necesidades...
cd necesidades
call mvnw.cmd clean install -DskipTests >nul 2>&1
cd ..

echo Compilando stock...
cd stock
call mvnw.cmd clean install -DskipTests >nul 2>&1
cd ..

echo Preparando match-service (Python)...
cd match-service
if not exist "venv" (
    python -m venv venv >nul 2>&1
)
venv\Scripts\python.exe -m pip install -r requirements.txt >nul 2>&1
cd ..

echo.
echo [3/4] INICIANDO SERVICIOS EN SEGUNDO PLANO...
echo Iniciando Auth (8081), User (8082), Necesidades (8083), Stock (8084) e IA (8000)...
start /B cmd /c "cd auth-service\target && java -jar auth-service-0.0.1-SNAPSHOT.jar"
start /B cmd /c "cd user-service\target && java -jar user-service-0.0.1-SNAPSHOT.jar"
start /B cmd /c "cd necesidades\target && java -jar necesidades-0.0.1-SNAPSHOT.jar"
start /B cmd /c "cd stock\target && java -jar stock-0.0.1-SNAPSHOT.jar"
start /B cmd /c "cd match-service && call venv\Scripts\activate.bat && python app.py"

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
