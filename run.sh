#!/bin/bash

# Function to check if a command exists
command_exists() {
    type "$1" &> /dev/null ;
}

# Check if Docker is installed
if command_exists docker; then
    echo "Docker is installed. Building and running the Flask app inside a Docker container..."
    docker build -t labio-all .
    docker run -p 5000:5000 labio-all &
else
    echo "Docker is not installed. Setting up and running the Flask app locally..."

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
    python api/app.py &

    # Delay to allow the server to start
    sleep 5
fi

# Try to open Safari
if command_exists open && [ -e /Applications/Safari.app ]; then
    open -a Safari http://localhost:5000/
    exit 0
fi

# Try to open Google Chrome in incognito mode
if command_exists google-chrome; then
    google-chrome --incognito http://localhost:5000/ &
    exit 0
fi

# Try to open Mozilla Firefox in private mode
if command_exists firefox; then
    firefox --private-window http://localhost:5000/ &
    exit 0
fi

# If neither browser is found, print a message
echo "No supported browsers found."

