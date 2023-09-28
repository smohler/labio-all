
#!/bin/bash

# Function to check if a command exists
command_exists() {
    type "$1" &> /dev/null ;
}

# Variables for flags
local_deploy=0
rebuild=0

# Check for flags
for arg in "$@"; do
    case $arg in
        -l|--local)
        local_deploy=1
        shift
        ;;
        -r|--rebuild)
        rebuild=1
        shift
        ;;
    esac
done

# Delete the existing virtual environment
echo "Deleting existing virtual environment..."
if [ -d "venv" ]; then
    rm -rf venv
fi

# Remove any __pycache__ directories and .pyc files
echo "Cleaning project directory..."
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -type f -delete

# If -l flag is not provided, try Docker setup
if [ "$local_deploy" -eq 0 ]; then
    # Check if rebuild flag is provided
    if [ "$rebuild" -eq 1 ]; then
        echo "Deleting existing Docker image..."
        docker rmi labio-all 2> /dev/null
        rm -f dist/package.tar 2> /dev/null
    fi

    # Check if dist/ folder exists with a .tar file
    if [ -f "dist/package.tar" ]; then
        echo "Found existing Docker image. Loading the image..."
        docker load -i dist/package.tar
    else
        # Check if Docker is installed and running
        if command_exists docker && docker info &> /dev/null; then
            echo "Docker is installed and running. Building and running the Flask app inside a Docker container..."
            docker build -t labio-all . && (
                mkdir -p dist
                docker save -o dist/package.tar labio-all
                docker run -p 5001:5001 labio-all &
                sleep 5
            )
        else
            echo "Docker is not installed or Docker Daemon is not running. Setting up and running the Flask app locally..."
            local_deploy=1
        fi
    fi
fi

# Local setup
if [ "$local_deploy" -eq 1 ]; then
    # Check if Python is installed
    if ! command_exists python3; then
        echo "Error: Python3 is not installed. Please install Python3 and try again."
        exit 1
    fi

    # Check if virtual environment exists, if not create one
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi

    # Activate virtual environment
    source venv/bin/activate

    # Install requirements
    pip install -r requirements.txt

    # Start Flask app in the background
    python app.py &
    sleep 5
fi

# Try to open browsers in the order: Google Chrome, Mozilla Firefox, Safari
if command_exists google-chrome; then
    google-chrome --incognito http://localhost:5001/ &
elif command_exists firefox; then
    firefox --private-window http://localhost:5001/ &
elif command_exists open && [ -e /Applications/Safari.app ]; then
    open -a Safari http://localhost:5001/
else
    echo "No supported browsers found."
fi
