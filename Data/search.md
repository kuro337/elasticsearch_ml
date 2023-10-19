# Searching ES Cluster

- Match

  - K/V does not need to be an exact match.
  - "running" and "ran" will match "run"
  - Calculates a Relevance Score - to rank search results by relevance



```json
GET http://your-elasticsearch-server:9200/your-index-name/_search
{
  "query": {
    "match": {
      "field1": "value1"
    }
  }
}

POST http://your-elasticsearch-server:9200/your-index-name/_search
{
  "query": {
    "match": {
      "text_field": "quick brown fox"
    }
  }
}

The match query would return documents containing 
any of the terms 
"quick," "brown," or "fox," 
and it ranks the results based on relevance.
```

- Term 

  - Used for EXACT matching

```json
POST http://your-elasticsearch-server:9200/your-index-name/_search
{
  "query": {
    "term": {
      "keyword_field": "value"
    }
  }
}
```


- Multi Index Search

```json
POST http://your-elasticsearch-server:9200/your-index-1, your-index-2/_search
{
  "query": {
    "match": {
      "field1": "value1"
    }
  }
}


```

- Bool Query

  - Combine multiple query clauses using boolean operators (AND, OR, NOT).

```json
POST http://your-elasticsearch-server:9200/your-index-name/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "field1": "value1" }},
        { "range": { "field2": { "gte": 10 }}}
      ],
      "must_not": [
        { "term": { "field3": "value3" }}
      ],
      "should": [
        { "match": { "field4": "value4" }}
      ]
    }
  }
}
```


- Filtered Query:

  - Filtering documents based on specific criteria without affecting the relevance score.


```json
POST http://your-elasticsearch-server:9200/your-index-name/_search
{
  "query": {
    "filtered": {
      "filter": {
        "range": {
          "field1": { "gte": 10 }
        }
      }
    }
  }
}

```

- Aggregations

  - Perform aggregations to summarize data based on specific criteria, like counting or averaging.

```json
POST http://your-elasticsearch-server:9200/your-index-name/_search
{
  "aggs": {
    "average_age": {
      "avg": {
        "field": "age"
      }
    }
  }
}
```