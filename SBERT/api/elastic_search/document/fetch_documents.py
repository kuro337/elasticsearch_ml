"""
ElasticSearch Class function implementation to insert a document into the 
corresponding index in Elasticsearch.
"""

from typing import Dict, Optional, List, Any

from model.interface import ESDocument


from elastic_search.exceptions.es_exceptions import ElasticsearchInsertionError


from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan


def fetch_documents(
    client: Elasticsearch,
    index_name: str,
    filter_conditions: Optional[Dict[str, Any]] = None,
) -> List[Dict]:
    """
    Retrieve all documents from the specified index.

    :param index_name: The name of the index from which to retrieve the documents.
    :return: A list of documents from the specified index.

    - Usage

    ```python
    filter_conditions = {"author": "JohnDoe"}
    documents = fetch_all_documents(
      index_name="posts",
      filter_conditions=filter_conditions
      )

    ```

    """
    # Initialize an empty list to store the documents
    documents = []

    if filter_conditions:
        query_body = {
            "query": {
                "bool": {
                    "filter": [
                        {"term": {field: value}}
                        for field, value in filter_conditions.items()
                    ]
                }
            }
        }
    else:
        query_body = {"query": {"match_all": {}}}

    # Use the 'scan' helper function to retrieve all documents in batches
    for doc in scan(client, index=index_name, query=query_body, scroll="5m"):
        # Each 'doc' will contain the document data
        documents.append(doc["_source"])  # append the document's body to the list

    return documents
