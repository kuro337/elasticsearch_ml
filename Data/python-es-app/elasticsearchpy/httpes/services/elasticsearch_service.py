from elasticsearch import Elasticsearch


class ElasticsearchService:
    def __init__(self, index_name):
        self.es = Elasticsearch(
            hosts=["http://localhost:9200"]
        )  # Set URL of Elasticsearch instance
        self.index_name = index_name

    def create_index(self, index_settings):
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name, body=index_settings)

    def insert_data(self, data):
        self.es.index(index=self.index_name, body=data)

    def search_data(self, index, query):
        """Search for data in the specified index using the query."""
        return self.es.search(index=index, body=query)

    def update_data(self, index, doc_id, data):
        """Update the document with specified id in the given index."""
        return self.es.update(index=index, id=doc_id, body={"doc": data})

    def delete_data(self, index, doc_id):
        """Delete the document with specified id from the given index."""
        return self.es.delete(index=index, id=doc_id)

    def bulk_insert(self, index, data_list):
        """Perform a bulk insert operation to the specified index."""
        actions = [
            {
                "_index": index,
                "_source": data,
            }
            for data in data_list
        ]
        return self.helpers.bulk(self.es, actions)
