# Indexes


```bash
# List All Indexes
curl --cacert ca.crt -u "elastic:password" -X GET "https://localhost:9200/_cat/indices?v"

# Index Health
curl --cacert ca.crt -u "elastic:password" -X GET "https://localhost:9200/_cat/indices/<index_name>?v"

#Index Mapping
curl --cacert ca.crt -u "elastic:password" -X GET "https://localhost:9200/<index_name>/_mapping?pretty"

# Delete Index
curl  --cacert ssl/ca.crt -u "elastic:password" -XDELETE 'https://localhost:9200/<index_name>'

curl  --cacert ssl/ca.crt -u "elastic:password" -XDELETE 'https://localhost:9200/user'


```



- Index Creation for Documents with Embeddings

```json


// User Embeddings Index

curl --cacert ssl/ca.crt -u "elastic:password" -X PUT "https://localhost:9200/user" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "username": { "type": "text" },
      "email": { "type": "text" },
      "gender": { "type": "text" },
      "country": { "type": "text" },
      "age": { "type": "text" },
      "embedding": { "type": "dense_vector", "dims": 768 , "index": true  , "similarity": "cosine"}
    }
  }
}
'

// Creating the Post Embeddings Index

curl --cacert ca.crt -u "elastic:password" -X PUT "https://localhost:9200/post_embeddings" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "title_embedding": { "type": "text" },
      "body_embedding": { "type": "text" },
      "author_embedding": { "type": "text" },
      "embedding": { "type": "dense_vector", "dims": 768 , "index": true  , "similarity": "cosine"},
    }
  }
}
'
// GLM User-Post Interaction Scores - GLM Model Scores for User-Post inserted here (O n.sq)

curl --cacert ca.crt -u "elastic:password" -X PUT "https://localhost:9200/user_post_scores" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "username": { "type": "text" },
      "post_id": { "type": "text" },
      "score": { "type": "float" },
      "timestamp": { "type": "date" },
    }
  }
}

// Interaction Index

curl --cacert ca.crt -u "elastic:password" -X PUT "https://localhost:9200/interaction" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "interaction_type": { "type": "text" },
      "post_id": { "type": "text" },
      "timestamp": { "type": "text" },
      "username": { "type": "text" },
    }
  }
}

// Product Embeddings Index
curl --cacert ca.crt -u "elastic:password"  -X PUT "https://localhost:9200/product_embeddings" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "id_embedding": { "type": "text" },
      "url_embedding": { "type": "text" },
      "last_accessed_embedding": { "type": "text" },
      "ip_address_embedding": { "type": "text" },
      "user_agent_embedding": { "type": "text" },
      "array_of_dates_embedding": { "type": "text" },
      "array_of_strings_embedding": { "type": "text" },
      "embedding": { "type": "dense_vector", "dims": 768 , "index": true  , "similarity": "cosine"},
    }
  }
}

```

- Doing knn search (cosine) on the embeddings

```json

