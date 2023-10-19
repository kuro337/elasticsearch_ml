# Setup Python Env

```bash
sudo apt install python3.12
python3.12 --version 
which python3.12 
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
sudo update-alternatives --config python3

python3 --version
```

## Virtual Environments

```bash
sudo apt install python3.12-venv

# Create env - myenv folder contains Python interpreetor and a Fresh Env
python3 -m venv myenv

# Activating Interpreter for Environment 
source myenv/bin/activate

# To return to System Interpretor
deactivate

```

# Elasticsearch OOP Pydantic

using Python I want to create an OOP Program that runs a web server - that has routes setup to insert data and create indexes for an Elasticsearch server. I want to use pydantic and use gunicorn and django so that this server runs and can process multiple reqs at once 

- Setting up Python App

```bash
# Activate virtual Env
source myenv/bin/activate
which pip # Should show path to Virtual Env app/myenv/bin/pip 

# Set VSCode interpreter to Virtual Env Python Runtime
which python # /home/chin/projects/Search/Elasticsearch/Data/python-es-app/myenv/bin/python
# Set Path Ctrl+Shift+P -> Python:Select Interpreter -> Enter Path

pip install django elasticsearch-dsl pydantic gunicorn mock

django-admin --version

django-admin startproject elasticsearchpy
cd elasticsearchpy

# Create a new python app
python manage.py startapp httpes

```

- Building Image and Deploying

```bash
# Create Requirements.txt and move to where the Project is

# Activate the VirtualEnv and Capture Deps to Requirements.txt
source myenv/bin/activate  
pip freeze > requirements.txt  


```

- Create Image

```bash
docker build -t elasticsearchpy .
docker run --name es -d -p 8000:8000 elasticsearchpy 
docker stop es && docker rm es

curl -X POST http://localhost:8000/httpes/create-index/ -H "Content-Type: application/json" -d '{"index_settings": {"your_setting": "value"}}'

curl -X POST http://localhost:8000/httpes/insert-data/ -H "Content-Type: application/json" -d '{"field1": "value1", "field2": 123}'
```

```Dockerfile
# Use an official Python runtime as the base image
FROM python:3.12.0-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY ./elasticsearchpy/requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./elasticsearchpy /app

# Specify the command to run on container start
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "elasticsearchpy.wsgi:application"]
```

- Kube

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: django-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: django
  template:
    metadata:
      labels:
        app: django
    spec:
      containers:
      - name: django
        image: ghcr.io/kuro337/elasticsearchpy:latest
        ports:
        - containerPort: 8000
      imagePullSecrets:
        - name: ghcr-secret  
```