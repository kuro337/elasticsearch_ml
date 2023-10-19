# Indexes


```bash
# List All Indexes
curl --cacert ca.crt -u "elastic:password" -X GET "https://localhost:9200/_cat/indices?v"

# Index Health
curl --cacert ca.crt -u "elastic:password" -X GET "https://localhost:9200/_cat/indices/<index_name>?v"

#Index Mapping
curl --cacert ca.crt -u "elastic:password" -X GET "https://localhost:9200/<index_name>/_mapping?pretty"

```

- Indexes Creations for Documents

```json
curl --cacert ca.crt -u "elastic:password" -X PUT "https://localhost:9200/user" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "username": { "type": "text" },
      "email": { "type": "keyword" },
      "gender": { "type": "keyword" },
      "country": { "type": "keyword" },
      "age": { "type": "integer" }
    }
  }
}
'

# Creating the Post Index
curl --cacert ca.crt -u "elastic:password" -X PUT "https://localhost:9200/post" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "body": { "type": "text" },
      "author": { "type": "keyword" }
    }
  }
}
'

# Creating the Product Index
curl --cacert ca.crt -u "elastic:password" -X PUT "https://localhost:9200/product" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "id": { "type": "integer" },
      "url": { "type": "keyword" },
      "last_accessed": { "type": "date" },
      "ip_address": { "type": "ip" },
      "user_agent": { "type": "text" },
      "array_of_dates": { "type": "date" },
      "array_of_strings": { "type": "keyword" }
    }
  }
}
'

```

- Index Creation for Embeddings

```json
// User Embeddings Index

curl --cacert ca.crt -u "elastic:password" -X PUT "https://localhost:9200/user_embeddings" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "username_embedding": { "type": "dense_vector", "dims": 768 },
      "email_embedding": { "type": "dense_vector", "dims": 768 },
      "gender_embedding": { "type": "dense_vector", "dims": 768 },
      "country_embedding": { "type": "dense_vector", "dims": 768 },
      "age_embedding": { "type": "dense_vector", "dims": 768 },
      "combined_embedding": { "type": "dense_vector", "dims": 768 } 
    }
  }
}
'

// Creating the Post Embeddings Index

curl --cacert ca.crt -u "elastic:password" -X PUT "https://localhost:9200/post_embeddings" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "title_embedding": { "type": "dense_vector", "dims": 768 },
      "body_embedding": { "type": "dense_vector", "dims": 768 },
      "author_embedding": { "type": "dense_vector", "dims": 768 },
      "combined_embedding": { "type": "dense_vector", "dims": 768 }  
    }
  }
}
'

// Product Embeddings Index
curl --cacert ca.crt -u "elastic:password"  -X PUT "https://localhost:9200/product_embeddings" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "id_embedding": { "type": "dense_vector", "dims": 768 },
      "url_embedding": { "type": "dense_vector", "dims": 768 },
      "last_accessed_embedding": { "type": "dense_vector", "dims": 768 },
      "ip_address_embedding": { "type": "dense_vector", "dims": 768 },
      "user_agent_embedding": { "type": "dense_vector", "dims": 768 },
      "array_of_dates_embedding": { "type": "dense_vector", "dims": 768 },
      "array_of_strings_embedding": { "type": "dense_vector", "dims": 768 },
      "combined_embedding": { "type": "dense_vector", "dims": 768 }
    }
  }
}
'


```