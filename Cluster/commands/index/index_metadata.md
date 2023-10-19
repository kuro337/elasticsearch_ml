# Index Metadata

```json
//  View all Indices
curl --cacert ca.crt -u "elastic:password" -X GET "https://localhost:9200/_cat/indices?v=true&pretty"

// Metadata Specific Index
curl --cacert ca.crt -u "elastic:password" -X GET "https://localhost:9200/user/_stats?pretty"



```