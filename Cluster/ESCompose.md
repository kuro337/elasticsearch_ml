# Launching ES Local Cluster

```bash
# Make sure VM Limit is set appropriately
sudo sysctl -w vm.max_map_count=262144

cd Cluster/
docker-compose up -d
docker-compose down
docker-compose down -v

docker stats

http://localhost:5601 # Kibana - user:elastic pw:password -> Cluster/.env

# Get SSL Cert to run curl locally
docker cp cluster-es01-1:/usr/share/elasticsearch/config/certs/ca/ca.crt ./ca.crt

# Health
curl  --cacert ca.crt -u "elastic:password"  -X GET "https://localhost:9200/_cat/health?v"

curl --cacert ca.crt -u "elastic:password" -X GET "https://localhost:9200/_cluster/state"


```