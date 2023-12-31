"""
ElasticSearch Class function implementation to insert a document into the 
corresponding index in Elasticsearch.
"""

from model.interface import ESDocument

from typing import Dict, Optional

from elastic_search.exceptions.es_exceptions import ElasticsearchInsertionError
from elasticsearch import Elasticsearch


def insert_document(
    client: Elasticsearch,
    document: ESDocument,
    index_name: Optional[str] = None,
    id: Optional[str] = None,
) -> None:
    """
    Inserts a document into the corresponding index in Elasticsearch.

    :param document: The document to insert.
    :type document: Union[User, Post, Product]
    """

    index_name = index_name or document.get_index_name()
    doc_id = id or document.hash()

    try:
        # Insertion
        response = client.index(
            index=index_name, id=doc_id, document=document.dump_document()
        )
        if response["_shards"]["failed"] > 0:
            raise ElasticsearchInsertionError(f"Failed to insert document: {response}")
    except ElasticsearchInsertionError as e:
        print(e)

    print(f"Successfully inserted into index {index_name}")
