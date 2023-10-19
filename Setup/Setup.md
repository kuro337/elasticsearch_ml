# Setup Elasticsearch on Kube

## Launch Elasticsearch Cluster

```bash
k3d create cluster

# Download CRD's, Deploy ECK Operator, Monitor Logs
kubectl create -f https://download.elastic.co/downloads/eck/2.9.0/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/2.9.0/operator.yaml
kubectl -n elastic-system logs -f statefulset.apps/elastic-operator

# Deploy Elasticsearch Cluster

cat <<EOF | kubectl apply -f -
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: 8.10.3
  nodeSets:
  - name: default
    count: 1
    config:
      node.store.allow_mmap: false
EOF

# Validate
kubectl get elasticsearch
kubectl get pods --selector='elasticsearch.k8s.elastic.co/cluster-name=quickstart'
kubectl get service quickstart-es-http

# Check this for production guidelines related to tradeoffs for node.store.allow_mmap setting
# https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-virtual-memory.html
```

- Once ES Cluster launched

```bash
# Get the Credentials - pw
kubectl get secret quickstart-es-elastic-user -o go-template='{{.data.elastic | base64decode}}'

# Get Password from inside cluster and use to curl from within cluster
kubectl run curl-temp-pod --image=curlimages/curl --restart=Never --command -- sleep infinity
kubectl exec -it curl-temp-pod -- sh
curl -u "elastic:9hk71l38EQ8ynC4K138VBeEk" -k "https://quickstart-es-http:9200"

# Or Run from local
kubectl port-forward service/quickstart-es-http 9200
curl -u "elastic:9hk71l38EQ8ynC4K138VBeEk" -k "https://localhost:9200"


```

- We get Cluster Info

```json
{
  "name" : "quickstart-es-default-0",
  "cluster_name" : "quickstart",
  "cluster_uuid" : "gYoJRkrwSNSSk4opro_FxQ",
  "version" : {
    "number" : "8.10.3",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "c63272efed16b5a1c25f3ce500715b7fddf9a9fb",
    "build_date" : "2023-10-05T10:15:55.152563867Z",
    "build_snapshot" : false,
    "lucene_version" : "9.7.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

## Scaling/Upgrading ES Cluster

- Just reapply a config

```bash
cat <<EOF | kubectl apply -f -
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: 8.10.3
  nodeSets:
  - name: default
    count: 3
    config:
      node.store.allow_mmap: false
EOF

```

- Now we have 3 Pods

## Launch Kibana Cluster

```bash
cat <<EOF | kubectl apply -f -
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: quickstart
spec:
  version: 8.10.3
  count: 1
  elasticsearchRef:
    name: quickstart
EOF

kubectl get kibana
kubectl get pod --selector='kibana.k8s.elastic.co/name=quickstart'

# Access Kibana
kubectl get service quickstart-kb-http
kubectl port-forward service/quickstart-kb-http 5601

# Login using password
kubectl get secret quickstart-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode; echo

# Login to Kibana - user : elastic , password : 9hk71l38EQ8ynC4K138VBeEk
https://localhost:5601


```

