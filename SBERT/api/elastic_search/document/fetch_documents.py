"""
ElasticSearch Class function implementation to insert a document into the 
corresponding index in Elasticsearch.
"""

from typing import Dict, Optional, List, Any, Tuple

from model.interface import ESDocument


from elastic_search.exceptions.es_exceptions import ElasticsearchInsertionError


from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan


def fetch_documents(
    client: Elasticsearch,
    index_name: str,
    filter_conditions: Optional[Dict[str, Any]] = None,
    query: Optional[Dict[str, Any]] = None,
    sort_by: Optional[Tuple[str, str]] = None,
    keyword: bool = True,
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
    if query:
        query_body = query
    elif filter_conditions:
        query_body = {
            "query": {
                "bool": {
                    "filter": [
                        construct_term_query(field, value, keyword)
                        for field, value in filter_conditions.items()
                    ]
                }
            }
        }
    else:
        query_body = {"query": {"match_all": {}}}
    if sort_by:
        field, order = sort_by
        query_body["sort"] = [{field: order}]
        # query_body["sort"] = [{sort_by[0]: {"order": sort_by[1]}}]

    print("Query Body", query_body)
    # Use the 'scan' helper function to retrieve all documents in batches
    for doc in scan(client, index=index_name, query=query_body, scroll="5m"):
        # Each 'doc' will contain the document data
        documents.append(doc["_source"])  # append the document's body to the list
    print("Ran Query")
    print(len(documents))
    return documents


def search_by(
    client: Elasticsearch,
    index_name: str,
    filter_conditions: Optional[Dict[str, Any]] = None,
    query: Optional[Dict[str, Any]] = None,
    sort_by: Optional[Tuple[str, str]] = None,
    size: int = 100,
    keyword: bool = True,
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
    if query:
        query_body = query
    elif filter_conditions:
        query_body = {
            "query": {
                "bool": {
                    "filter": [
                        construct_term_query(field, value, keyword)
                        for field, value in filter_conditions.items()
                    ]
                }
            }
        }
    else:
        query_body = {"query": {"match_all": {}}}

    if sort_by:
        field, order = sort_by
        query_body["sort"] = [{field: {"order": order}}]

    print("Query Body", query_body)

    # Change this part to use `search` instead of `scan`
    response = client.search(index=index_name, body=query_body, size=size)
    documents = [doc["_source"] for doc in response["hits"]["hits"]]

    print("Ran Query")
    print(len(documents))
    return documents


def construct_term_query(field, value, keyword):
    """Constructs a term or terms query based on the provided value."""
    if isinstance(value, list):
        return {"terms": {field + ".keyword" if keyword else "": value}}
    else:
        return {"term": {field + ".keyword" if keyword else "": value}}
