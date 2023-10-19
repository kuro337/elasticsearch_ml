# Semantic Search in Elasticsearch


- Storing in ElasticSearch

```json 
// Create an index with a dense_vector field

PUT /embeddings
{
  "mappings": {
    "properties": {
      "embedding": {
        "type": "dense_vector",
        "dims": 384  # Set dims to the dimension of the embeddings
      }
    }
  }
}

// Insert the embedding into the index

POST /embeddings/_doc/1
{
  "embedding": [/* values from the embedding tensor here */]
}

```

- Performing Semantic Search

```json
POST /embeddings/_search
{
  "query": {
    "script_score": {
      "query": {
        "match_all": {}
      },
      "script": {
        "source": "cosineSimilarity(params.query_vector, doc['embedding']) + 1.0",
        "params": {
          "query_vector": [/* embedding of the query document here */]
        }
      }
    }
  }
}

```