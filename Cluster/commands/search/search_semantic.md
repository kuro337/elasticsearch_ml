# Semantic Search on Elasticsearch Index 

- Searching Index of Embeddings with Elasticsearch

- Cosine Similarity Search

```json
// Searching in the user_embeddings index
curl -X POST "localhost:9200/user_embeddings/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "script_score": {
      "query": { "match_all": {} },
      "script": {
        "source": "cosineSimilarity(params.query_vector, doc['combined_embedding']) + 1.0",
        "params": {
          "query_vector": [0.1, 0.2, 0.3, ..., 0.766, 0.767, 0.768]  # Your query vector
        }
      }
    }
  }
}
'

# Searching in the product_embeddings index
curl -X POST "localhost:9200/product_embeddings/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "script_score": {
      "query": { "match_all": {} },
      "script": {
        "source": "cosineSimilarity(params.query_vector, doc['combined_embedding']) + 1.0",
        "params": {
          "query_vector": [0.1, 0.2, 0.3, ..., 0.766, 0.767, 0.768]  # Your query vector
        }
      }
    }
  }
}
'
```
