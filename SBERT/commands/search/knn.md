# knn Search

- knn Search

```json
POST image-index/_search
{
  "knn": {
    "field": "image-vector",
    "query_vector": [-5, 9, -12],
    "k": 10,  // Number of Nearest Neighbors to Return
    "num_candidates": 100 // Higher Number , More Accuracy
  },
  "fields": [ "title", "file-type" ]
}

```

- From App

```python
# Search by Approximate Match on Document Field
def semantic_search(
        self,
        query_vector: List[float],
        index_name: str,
        size: int = 10,
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
            "filter": {"bool": {"must": {"match": {"country": "japan"}}}},
        }

        res = self.client.search(
            knn=query_dict,
            index=index_name,
            source_excludes=["embedding"],
        )

        for hit in res["hits"]["hits"]:
            print(hit)

        return res

# Search by Exact Match on Document Field

def semantic_search(
        self,
        query_vector: List[float],
        index_name: str,
        size: int = 10,
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
            "filter": {
                "term": {"country.keyword": "Japan"},
            },
        }

        

        res = self.client.search(
            knn=query_dict,
            index=index_name,
            source_excludes=["embedding"],
        )

        for hit in res["hits"]["hits"]:
            print(hit)

        return res
```
