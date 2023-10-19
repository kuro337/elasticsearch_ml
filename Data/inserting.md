# Inserting Documents

- Inserting Document into an Index

```bash
POST http://your-elasticsearch-server:9200/your-index-name/_doc/1
{
  "field1": "value1",
  "field2": "value2",
  # Add more fields as needed
}
```

- Bulk Insertion

```json
POST http://your-elasticsearch-server:9200/your-index-name/_bulk
{ "index": { "_id": "1" }}
{ "field1": "value1", "field2": "value2" }
{ "index": { "_id": "2" }}
{ "field1": "value3", "field2": "value4" }
```

- Update Document

```json
POST http://your-elasticsearch-server:9200/your-index-name/_update/1
{
  "doc": {
    "field1": "new-value1"
  }
}
```