
## **A**wesome **Lab** **L**IMS

This repository contains a simple Flask-based API with SQLite as the database [TODO].

### Prerequisites

- Docker (optional)
- Python 3 (if not using Docker)

### Setup and Running the API

Both `run.sh` (for Mac and Unix-like systems) and `run.bat` (for Windows) are provided to automate the setup and running process. These scripts will:

1. Check if Docker is installed.
    - If Docker is detected, they will build a Docker image and run the Flask app inside a container.
    - If Docker is not installed, they will:
        1. Check if Python 3 is installed.
        2. Set up a virtual environment (if not already set up).
        3. Install the required Python packages.
        4. Run the Flask app.
2. Once the Flask app is running, you can access the API at `http://127.0.0.1:5001/`.

### Running the Scripts
This repo has provide to getting started run script for both Mac and Windows users.

#### For Mac and Unix-like systems:

```bash
chmod +x run.sh
./run.sh
```

#### For Windows:
Open a cmd prompt in the root of the cloned repository. From here you just have to type run.
```cmd
C:\labio-all>run
```
You can also open the folder in the file browswer and click the run.bat file.
