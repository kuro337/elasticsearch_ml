# FastAPI GUnicorn Python Web Server


- Setup

```bash
python -m venv venv
source venv/bin/activate  

pip install fastapi uvicorn elasticsearch pydantic gunicorn python-json-logger

# Start App Server and ES Cluster

cd elasticsearch_py
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

# Make sure VM Limit is set appropriately
sudo sysctl -w vm.max_map_count=262144

cd Cluster/
docker-compose up -d
docker-compose down

http://localhost:5601 # Kibana - user:elastic pw:password -> Cluster/.env

```

- Testing Server

```bash
curl -X POST "http://localhost:8000/create-index/test_index"

curl -X POST "http://localhost:8000/create-index/test_index/badreq"

curl -X POST "http://localhost:8000/test_index/insert" -H "Content-Type: application/json" -d '{"type": "user", "data": {"name": "Alice", "age": 25, "email": "alice@example.com"}}'

# Invalid
curl -X POST "http://localhost:8000/test_index/insert" -H "Content-Type: application/json" -d '{"type": "user", "data": {"name": "Incomplete", "age": "notAnInteger"}}'

# Unknown Type
curl -X POST "http://localhost:8000/test_index/insert" -H "Content-Type: application/json" -d '{"type": "unknownType", "data": {"key": "value"}}'


# Create Index
curl -X POST "http://localhost:8000/create-index/users" -H "Content-Type: application/json" -d'
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "name": {
        "type": "text"
      },
      "age": {
        "type": "integer"
      },
      "email": {
        "type": "keyword"
      }
    }
  }
}'


```