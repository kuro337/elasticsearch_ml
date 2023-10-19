# ES Cluster Indexes

- Creating Index

- Shards

  - Primary Shard
    - Handle Indexing and Searching Operations
  
  - Replica Shard
    - Copies of Primary Shards
    - Provide redundancy and increase Read Performance


```json
PUT http://your-elasticsearch-server:9200/your-index-name
{
  "settings": {
    "number_of_shards": 5,    # Adjust based on your requirements
    "number_of_replicas": 1  # Adjust based on your requirements
  },
  "mappings": {
    "properties": {
      "field1": {
        "type": "text"
      },
      "field2": {
        "type": "keyword"
      },
      # Add more fields as needed
    }
  }
}


```

- Index Templates

- To specify settings and mappings applied to indexes that match the defined Pattern

```json
PUT http://your-elasticsearch-server:9200/_index_template/your-template-name
{
  "index_patterns": ["pattern-matching-your-indices-*"],
  "priority": 1,
  "template": {
    "settings": {
      "number_of_shards": 3,
      "number_of_replicas": 1
    },
    "mappings": {
      "properties": {
        "field1": {
          "type": "text"
        },
        "field2": {
          "type": "keyword"
        }
      }
    }
  }
}


```

- Index Alias

```json
POST http://your-elasticsearch-server:9200/_aliases
{
  "actions": [
    {
      "add": {
        "index": "your-index-name",
        "alias": "your-alias-name"
      }
    }
  ]
}


```