@echo off
echo ==============================================
echo = Compiling Microservices for Donaton Project=
echo ==============================================

echo.
echo Building Auth Service...
cd auth-service
call mvnw.cmd clean install
cd ..

echo.
echo Building User Service...
cd user-service
call mvnw.cmd clean install
cd ..

echo.
echo Building Necesidades Service...
cd necesidades
call mvnw.cmd clean install
cd ..

echo.
echo Building Stock Service...
cd stock
call mvnw.cmd clean install
cd ..

echo.
echo Setting up Match Service (Python)...
cd match-service
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt
deactivate
cd ..

echo.
echo ===================================================
echo = Build completed! Jars are in target/ folders    =
echo = Match Service virtual environment is configured =
echo ===================================================
pause
