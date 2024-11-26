# data_engineer_assignment

## Description

This project involves setting up a Python application using Docker. It uses libraries such as `transformers`, `torch`, `pandas`, and others to perform specific tasks. The goal is to set up a clean environment for running the project efficiently.

## Structure
The repository is structured as follows:
1) **data_api.py**: The python file downloads the clinical_data from the clinicaltrials.gov API, it retrieves all studies that have been last updated between 20 and 21 October 2024. (A “last update” date is available per study.) The query parameters can be adjusted/added as per requirements. The **output** .json files are stored in './rawdata'.
   
2) **map_schema.py**: The python file maps the downloaded studies from 'data_api.py' to extract relevant key names (fields) from the input file ('./rawdata/all_studies.json -> combined .json file from all the downloaded studies from step 1.).
**Note**: The data structures format of the downloaded .json files is saved and store in a .csv file ("./datastruct/Protocolsection.csv"). It enables faster search of relevant keys in the .json files. The **output** is a .csv file ("./inclusion_criteria_dict.csv"). 

3) **extract_diseases.py**: The python file uses the pre-trained BioBERT transformer and NER pipeline (https://huggingface.co/dslim/bert-base-NER) to extract diseases from the ("./inclusion_criteria_dict.csv"). The transformer parameters/models can be customized. It only requires the input data to be specified in a dataframe consisting of labels ('IDs') and sentences ('merged') columns. Therefore, any data in this format can be used for extracting disease names from the data.

4) **run_scripts.py**: Python file which runs steps 1-3.

5) ./rawdata: folder where all the .json files are downloaded from API

6) ./datastruct/: folder containing the .json datastructures for accessing specific keys

7) Other misc files include .ipynb for development, and error logs

## Prerequisites

Before running the application, ensure you have the following installed on your machine:

- **Python** (version 3.11 is recommended)
- **Docker** (for running image)
- **Git** (to clone the repository)
- **Conda** (optional)

## Manual installation and execution

You can set up the project either using `pip` and `requirements.txt` or with `conda` using the `environment.yml` file.

### Option 1: Using `requirements.txt` (for `pip`)

1. Clone the repository:

   ```bash
   git clone https://github.com/Bhawnadixit/data_engineer_assignment.git
   cd data_engineer_assignment
   ```

2. Create and activate a virtual environment (optional, but recommended):

   ```bash
   python3 -m venv venv  # Create a virtual environment
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```
   ```bash
   python run_scripts.py
   ```
4. Now your environment is set up, and you can run the application by simply running "python run_scripts.py" in your current git directory.


### Option 2: Using `environment.yml` (for `conda`)

1. Clone the repository:

   ```bash
   git clone https://github.com/Bhawnadixit/data_engineer_assignment.git
   cd data_engineer_assignment
   ```

2. Create a conda environment from the `environment.yml` file:

   ```bash
   conda env create -f environment.yml
   ```

3. Activate the conda environment:

   ```bash
   conda activate assign_bd  # Replace 'assign_bd' with the environment name from the yml file
   ```
   ```bash
   python run_scripts.py
   ```

4. Your environment is now set up. You can now run the application by simply running "python run_scripts.py" in your current git directory.

## Running the Application with Docker

If you prefer to run the application within a Docker container (highly recommended for consistent environments across different machines), follow these steps.

### Prerequisites

Ensure that you have **Docker** installed on your system. If not, you can download and install it from [Docker's official website](https://www.docker.com/get-started).

### Steps to Build and Run the Docker Container

Build the Docker image from the Dockerfile.
