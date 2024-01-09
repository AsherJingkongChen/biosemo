## Project Summary

### Project composition
- **Front End (FE):** Web interface built with Vue.js.
- **Backend (BE):** A Python backend built using the FastAPI framework and integrating machine learning (ML) models.
- **Machine Learning (ML):** Use the PyCaret library for model training and deployment.
- **Utils:** Stores Python modules for heart rate variability (HRV) feature extraction.

## Project file structure

### Main file

- **analyze.ipynb:** Jupyter Notebook for data analysis.

- **preprocess.ipynb:** Jupyter Notebook for data preprocessing.

- **deploy.py:** Main deployment script, configures FastAPI and model deployment.

- **requirements.txt:** Stores the list of dependent packages for the project.

- **logs.log:** Log file that records events and errors when the application is running.

- **utils/:** Directory that stores various tools and auxiliary functions.

### Tool Module

- **hrv_feature_extraction.py:** Python module for extracting features from heart rate data.

## User operations

### Machine Learning (ML)
- Use **analyze.ipynb** for data analysis.
- Use **preprocess.ipynb** to preprocess data.
- Deploy machine learning models through **deploy.py**.

### Front End (FE)
- Use Vue.js to build web interfaces.

### Backend (BE)
- Build Python backend using FastAPI framework.

### DevOps
- Manage project dependency packages through **requirements.txt**.

## Data process

1. **Data Analysis:**
    - Use **analyze.ipynb** to analyze the data.

2. **Data preprocessing:**
    - Use **preprocess.ipynb** for data preprocessing.

3. **Machine learning model training:**
    - Use **deploy.py** to train and deploy machine learning models.

4. **Web interface construction:**
    - Build web interfaces using Vue.js.

5. **Application Deployment and Running:**
    - Deploy FastAPI backend application to run the entire system.

## In conclusion
This project uses machine learning, front-end, and back-end integration to build a web application that includes data analysis and machine learning functions. Users can execute data processes, train models, and deploy applications by operating corresponding files and scripts.
