# Semantic Search



```json
curl  --cacert ssl/ca.crt -u "elastic:password" -XDELETE 'https://localhost:9200/user'

curl --cacert ssl/ca.crt -u "elastic:password" -X PUT "https://localhost:9200/test" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "embedding": { "type": "dense_vector", "dims": 3 , "index": true  , "similarity": "cosine"},
      "username": { "type": "keyword" }
    }
  }
}
'

// Insert
curl --cacert ssl/ca.crt -u "elastic:password" -X PUT "https://localhost:9200/test/_doc/5" -H 'Content-Type: application/json' -d'
{
  "username" : "text55",
  "embedding" : [0.1, 0.9, 0.7]
}
'
```


- Query

```json
curl --cacert ssl/ca.crt -u "elastic:password" -X POST "https://localhost:9200/test/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_all": {}
  }
}
' | jq

// Below will work only from curl and not API - correct way is using knn query
// https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html#search-api-knn

// Semantic Search

curl --cacert ssl/ca.crt -u "elastic:password" -X POST "https://localhost:9200/test/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "script_score": {
      "query": {
        "match_all": {}
      },
      "script": {
        "source": "cosineSimilarity(params.query_vector, \"embedding\") + 1.0",
        "params": {
          "query_vector": [0.4, 10, 6]
        }
      }
    }
  }
}
' | jq


```

- Correct Search Function

```python
def semantic_search(
        self,
        query_vector: List[float],
        index_name: str,
        size: int = None,
        sort_order: str = "desc",
    ):
        """
        Performs Semantic Search on the index_name with the query_vector
        """
        query_dict = {
            "field": "embedding",
            "query_vector": query_vector,
            "k": 10,
            "num_candidates": 10,
        }
        res = self.client.search(knn=query_dict, index=index_name, source=["username"])

        for hit in res["hits"]["hits"]:
            print(hit)

```