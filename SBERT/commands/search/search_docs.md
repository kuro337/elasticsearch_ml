# Searching Documents in Elasticsearch Index

- Search for Documents in ES Index

- Types of Queries - Term, Match, Range, Fuzzy, Wildcard, Prefix, Multi-Match, Regex

- Query Structure

```json
{
  "query": {
    "${QUERY_TYPE}": {"field1": "value", "field2": "value"}
  }
}
```

- Query Types

```json
Term
{
  "query": {
    "term": {
      "country": "USA"
    }
  }
}

Fuzzy
{
  "query": {
    "fuzzy": {
      "country": {
        "value": "japn",
        "fuzziness": "AUTO"
      }
    }
  }
}

WildCard
{
  "query": {
    "wildcard": {
      "country": {
        "value": "ja*n"
      }
    }
  }
}

Prefix
{
  "query": {
    "prefix": {
      "country": {
        "value": "ja"
      }
    }
  }
}

Multi-Match
{
  "query": {
    "multi_match": {
      "query": "Elizabeth",
      "fields": ["username", "email"]
    }
  }
}

Regex Expression

{
  "query": {
    "regexp": {
      "email": {
        "value": ".*@alaskaairlines\\.com"
      }
    }
  }
}


```


- Match Query

```json
// Match query on the users index (exact Match for Field)

curl --cacert ssl/ca.crt -u "elastic:password" -X POST "https://localhost:9200/user/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "country": "USA"
    }
  }
}
' |  jq

// Get all Docs

curl --cacert ssl/ca.crt -u "elastic:password" -X POST "https://localhost:9200/test/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_all": {}
  }
}
' | jq


// Range query on the products index
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