@echo off
SETLOCAL

REM Check if the -l flag is provided
set local_deploy=
:check_args
if "%1" == "-l" (
    set local_deploy=1
    shift
    GOTO check_args
)

REM Delete the existing virtual environment
echo Deleting existing virtual environment...
if exist venv rmdir /s /q venv

REM Remove any __pycache__ directories and .pyc files
echo Cleaning project directory...
if exist __pycache__ rmdir /s /q __pycache__
del /s /q *.pyc

:: Check if -l flag is provided, skip Docker section if it is
if not defined local_deploy (
    :: Check if docker is installed
    WHERE docker >nul 2>nul
    IF %ERRORLEVEL% NEQ 0 (
        echo Docker is not installed or not added to PATH. Setting up and running the Flask app locally...
        GOTO LOCAL_SETUP
    )

    :: Check if Docker Daemon is running by executing a simple docker command
    docker info >nul 2>nul
    IF %ERRORLEVEL% NEQ 0 (
        echo Docker Daemon is not running. Starting local setup...
        GOTO LOCAL_SETUP
    )

    echo Docker is installed and running. Building and running the Flask app inside a Docker container...
    SET DOCKER_BUILDKIT=1
    docker build -t labio-all . && (
        docker run -p 5000:5000 labio-all
        GOTO END
    )
)

:LOCAL_SETUP
:: Check if Python is installed
WHERE python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not added to PATH. Please install Python and try again.
    GOTO END
)

:: Check if virtual environment exists, if not create one
IF NOT EXIST "venv" (
    python -m venv venv
)

:: Activate virtual environment
CALL venv\Scripts\activate

:: Install requirements
pip install -r requirements.txt

:: Run Flask app
python app.py

:END
ENDLOCAL

