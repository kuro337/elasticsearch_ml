# General Linear Model



```bash
sudo apt install python3.10
python3.10 --version 
sudo apt install python3.10-venv

# Create Project and Activate Environment
python3.10 -m venv glmenv310
source glmenv310/bin/activate  

# To return to System Interpretor
deactivate

pip install pandas scikit-learn pylint pydantic joblib 

# Check python-multipart

# To use packages from other Directory it should have a setup.py file
# To install SBERT in the Environment
pip install -e /home/chin/projects/Search/Elasticsearch/SBERT

# Setting up Linting
which pylint
# Ctrl + , -> pylint import strategy = from env

# Make sure .env file is set at Root with
# PYTHONPATH=/home/chin/projects/Search/Elasticsearch/SBERT/ml_app

# Also Set the Pylint Binary path 
# /home/chin/projects/Search/Elasticsearch/SBERT/myenv310/bin/pylint

# To make sure App runs with the correct Python Paths for Modules
export PYTHONPATH="/home/chin/projects/Search/Elasticsearch/SBERT:/home/chin/projects/Search/Elasticsearch/Backend"


# Run App
python3 sbert.py

```

- Setting up as a Module

```python
"""
Creating a Module for SBERT

pip install -e .

From other projects, you can now import SBERT like this:

pip install -e /path/to/SBERT 

/home/chin/projects/Search/Elasticsearch/SBERT

"""

from setuptools import setup, find_packages


setup(
    name="Stats",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pandas", "scikit-learn"],
)

# pip install .



```

