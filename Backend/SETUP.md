# Backend Web Server Setup



```bash
sudo apt install python3.10
python3.10 --version 
sudo apt install python3.10-venv

# Create Project and Activate Environment
python3.10 -m venv venv310
source venv310/bin/activate  

# To return to System Interpretor
deactivate

pip install -U  sentence-transformers
pip install pylint pydantic elasticsearch fastapi uvicorn gunicorn 

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

- Websockets

```python
- Implementing GLM

```python
# ... previous imports ...
from sklearn import linear_model

# ... previous code ...

@app.post("/train_glm")
async def train_glm():
    # ... implement GLM training ...

@app.post("/get_recommendations/{user_id}")
async def get_recommendations(user_id: int):
    # ... implement feature extraction, GLM prediction, and ES query for recommendations ...


```

```