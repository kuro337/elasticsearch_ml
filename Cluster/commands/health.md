# Cluster Health


```bash
curl  --cacert ca.crt -u "elastic:password"  -X GET "https://localhost:9200/_cat/health?v"

curl --cacert ca.crt -u "elastic:password" -X GET "https://localhost:9200/_cluster/state"


```