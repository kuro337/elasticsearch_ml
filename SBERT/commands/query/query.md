# Querying ES

- Queries to get posts with top 10 Scores

```json

curl --cacert ca.crt -u "elastic:password" -X POST "https://localhost:9200/user_post_score/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        { "term": { "user_id": "JohnDoe" } }
      ]
    }
  },
  "sort": [
    { "score": { "order": "desc" } }
  ],
  "size": 100
}
'


```