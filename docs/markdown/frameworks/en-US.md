# Web Application with ML Backend and Vue.js Frontend using FastAPI

## Purpose of the Project
This Python script, `deploy.py`, serves as the main file for a web application. The application combines a Python Machine Learning (ML) backend and a Vue.js frontend, utilizing the FastAPI framework. The purpose of the project is to create an interactive web interface that leverages machine learning models to provide stress analysis and counseling services based on user-provided physiological data.

## Usage
The script can be executed with the following command-line options:
```bash
python3 deploy.py [-v|--verbose] [-q|--quiet]
```

## Global Parameters
- `DATA_DIR`: Path to the dataset directory (`'../datasets/swell/final'`).
- `TEST_DATA_NAME`: Name of the test data (`'test'`).
- `API_HOST`: Hostname for the API server (`'localhost'`).
- `API_PORT`: Port number for the API server (`8080`).
- `IS_VERBOSE`: Verbosity flag for logging (`True` by default).

## Logging Setup
The script sets up logging based on the verbosity level provided through command-line arguments (`-v` or `--verbose` for verbose, `-q` or `--quiet` for quiet).

## Dependency Installation
The script installs required dependencies using `pip` based on the contents of the `requirements.txt` file.

## Environment Setup
The environment is configured, including setting logging levels and adjusting Pandas display options.

## Greeting
A greeting function is defined to display the API Playground URL.

## Data Preparation
The script loads and prepares the dataset for machine learning. It extracts compressed data files, loads the data, and performs custom target encoding.

## Machine Learning Model Loading
The script loads a pre-trained machine learning model and associated experiment using the PyCaret library. The model and experiment are displayed using IPython if in verbose mode.

## API Implementation
The script implements FastAPI routes for stress analysis and counseling. It defines request and response schemas, routes, and functions for stress level prediction and counseling suggestions.

## OpenAI Integration
The script integrates with OpenAI's GPT-3.5-turbo for stress counseling. It defines a chat completion function based on user-provided stress statistics.

## API Server Configuration
FastAPI is configured with routes, including redirects and serving static files for the Vue.js frontend. The server is configured to run on `localhost:8080`.

## Running the Application
The script runs the API services using UVicorn, handling concurrency using asyncio and specifying server configurations.

## Conclusion
This script encapsulates the entire workflow of setting up a web application with machine learning capabilities for stress analysis and counseling. The user, by executing this script, initiates the deployment and operation of the web application on `localhost:8080`.
