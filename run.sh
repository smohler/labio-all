#!/bin/bash

# Function to check if a command exists
command_exists() {
    type "$1" &> /dev/null ;
}

# Check if Docker is installed
if command_exists docker; then
    echo "Docker is installed. Building and running the Flask app inside a Docker container..."
    docker build -t labio-all .
    docker run -p 5000:5000 labio-all
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

    # Run Flask app
    python api/app.py
fi
