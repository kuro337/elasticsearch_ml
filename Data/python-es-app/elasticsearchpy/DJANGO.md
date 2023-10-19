# Django

- Overview of Creating a new Django App

```bash
- Overview of Creating a new Django App

SETUP
  - Setup Development Environment

  - Install Django

  - Create a New Django Project

  - Create a New Django App

APPLICATION

  - Create Services
    -Elasticsearch Service in App

  - Define Types for Data in models.py

  - Define Functions to handle Logic for Routes /route1 /route2
    -views.py

  - Set Routes to define active routes
    -urls.py -> Add Views (functions we defined) to it

PROJECT -

  - Add App URLSs 
    -> App.urls to urls.py

  - Add Application httpes to INSTALLED_APPS in 
    -settings.py

```

- Running App

```bash
python manage.py runserver

# Commands OLD
curl -X POST http://127.0.0.1:8000/httpes/create-index/ -H "Content-Type: application/json" -d '{"index_settings": {"your_setting": "value"}}'

curl -X POST http://127.0.0.1:8000/httpes/insert-data/ -H "Content-Type: application/json" -d '{"field1": "value1", "field2": 123}'

# Commands NEW

# Valid
curl -X POST http://127.0.0.1:8000/httpes/insert-data/ -H "Content-Type: application/json" -d '{"type": "user", "data": {"username": "johndoe", "email": "johndoe@example.com"}}'

curl -X POST http://127.0.0.1:8000/httpes/insert-data/ -H "Content-Type: application/json" -d '{"type": "session", "data": {"username": "a", "session_key": "sessionKey123"}}'

# Testing Req that provides too short of a String
curl -X POST http://127.0.0.1:8000/httpes/insert-data/ -H "Content-Type: application/json" -d '{"type": "post", "data": {"title": "Sample Post", "body": "This is a sample post.", "author": "johndoe"}}'

# Passing Invalid Entity
curl -X POST http://127.0.0.1:8000/httpes/insert-data/ -H "Content-Type: application/json" -d '{"type": "notexists", "data": {"username": "johndoe", "email": "johndoe@example.com"}}'

# Launching using gunicorn - 3 worker processes. 2-4 Workers per core recommended.

gunicorn --workers=3 elasticsearchpy.wsgi:application

# With explicit Port
gunicorn --workers=3 --bind=0.0.0.0:8080 elasticsearchpy.wsgi:application

```

- Create Service for ES

- services/elasticsearch_service.py

```py
from elasticsearch import Elasticsearch

class ElasticsearchService:
    def __init__(self, index_name):
        self.es = Elasticsearch()
        self.index_name = index_name

    def create_index(self, index_settings):
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name, body=index_settings)

    def insert_data(self, data):
        self.es.index(index=self.index_name, body=data)

```