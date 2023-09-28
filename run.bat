@echo off
SETLOCAL

REM Check if the -l flag is provided
set local_deploy=
set rebuild=
:check_args
if "%1" == "-l" (
    set local_deploy=1
    shift
    GOTO check_args
)
if "%1" == "--local" (
    set local_deploy=1
    shift
    GOTO check_args
)

REM Check if the -r or --rebuild flag is provided
if "%1" == "-r" (
    set rebuild=1
    shift
    GOTO check_args
)

if "%1" == "--rebuild" (
    set rebuild=1
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
    :: Check if rebuild flag is provided, delete existing package.tar
    if defined rebuild (
        echo Deleting existing Docker image...
        docker rmi labio-all 2>nul
        del dist\package.tar 2>nul
    )

    :: Check if dist/ folder exists with a .tar file
    if exist dist\package.tar (
        echo Found existing Docker image. Loading the image...
        docker load -i dist\package.tar
    ) else (
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
            :: Save the Docker image to dist/ folder
            mkdir dist 2>nul
            docker save -o dist\package.tar labio-all
            start /B cmd /k "docker run -p 5000:5000 labio-all"
            ping 127.0.0.1 -n 5 >nul
            GOTO TryMsEdge
        )
    )
)

:LOCAL_SETUP
:: Rest of your local setup code remains the same

:: Start Flask app in the background without opening a new window
start /B cmd /c "python app.py"

:: Delay to allow the server to start
ping 127.0.0.1 -n 5 >nul

:TryMsEdge
:: Try to open Microsoft Edge in InPrivate mode
start msedge -inprivate http://localhost:5000/
if %errorlevel% neq 0 GOTO TryChrome
:: If Edge opens successfully, exit
GOTO END 

:TryChrome
:: Try to open Google Chrome in incognito mode
start chrome --incognito http://localhost:5000/
if %errorlevel% neq 0 GOTO TryFirefox

:: If Chrome opens successfully, exit
GOTO END

:TryFirefox
:: Try to open Mozilla Firefox in private mode
start firefox -private http://localhost:5000/
if %errorlevel% neq 0 GOTO NoBrowsers

:: If Firefox opens successfully, exit
GOTO END

:NoBrowsers
ECHO No supported browsers found.
PAUSE
EXIT

:END
ENDLOCAL
