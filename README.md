
## ALL Web API

This repository contains a simple Flask-based API with SQLite as the database.

### Prerequisites

- Docker (optional)
- Python 3 (if not using Docker)

### Setup and Running the API

#### Using Docker (Preferred)

Both `run.sh` (for Unix-like systems) and `run.bat` (for Windows) will first check if Docker is installed:

1. If Docker is detected, the scripts will build a Docker image and run the Flask app inside a container.
2. Access the API at `http://127.0.0.1:5000/`.

#### Without Docker

If Docker is not installed, the scripts will set up and run the Flask app locally:

1. They'll check if Python 3 is installed.
2. Set up a virtual environment (if not already set up).
3. Install the required Python packages.
4. Run the Flask app.
5. Access the API at `http://127.0.0.1:5000/`.

### Running the Scripts

#### On Unix-like systems:

```bash
chmod +x run.sh
./run.sh
```

#### On Windows:

Double-click on `run.bat` or run it from the command prompt.
