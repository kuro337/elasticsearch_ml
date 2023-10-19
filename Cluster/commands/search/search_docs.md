# Searching Documents in Elasticsearch Index

- Search for Documents in ES Index


```json
// Match query on the users index

curl --cacert ca.crt -u "elastic:password" -X POST "https://localhost:9200/user/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "country": "USA"
    }
  }
}
'

# Range query on the products index
curl -X POST "localhost:9200/product/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "range": {
      "last_accessed": {
        "gte": "2023-10-15T00:00:00Z",
        "lte": "2023-10-16T23:59:59Z"
      }
    }
  }
}
'


```