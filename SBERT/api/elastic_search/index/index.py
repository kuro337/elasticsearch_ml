"""
ES Class function implementation to create and delete an index in Elasticsearch.
"""

import json
from typing import Dict, Optional
from elasticsearch import Elasticsearch, NotFoundError
from model.interface import ESDocument


def create_index(
    client: Elasticsearch,
    model: ESDocument | str,
    index_name: Optional[str] = None,
    embedding: bool = False,
) -> None:
    """
    Create an Index in Elasticsearch
    @param client: Elasticsearch client
    @param model: Dict
    @param index_name: Optional[str]
    @param embedding: bool

    Usage:

    ```python
    create_index(client, User, index_name, embedding)

    ```
    """
    index_name = index_name or (
        model.get_index_name() if isinstance(model, ESDocument) else model
    )

    # mappings = {"properties": {f"{key}": {"type": "text"} for key in model.keys()}}

    mappings = model.get_mapping()

    if embedding:
        mappings["properties"]["embedding"] = {
            "type": "dense_vector",
            "dims": 768,
            "index": True,
            "similarity": "cosine",
        }
    try:
        client.indices.create(index=index_name, body={"mappings": mappings})
    except Exception as e:
        print(e)


def delete_index(client: Elasticsearch, index_name: str) -> None:
    """
    Delete an Index in Elasticsearch
    """
    try:
        client.indices.delete(index=index_name)
    except Exception as e:
        print(e)


def list_indices_and_mappings(client: Elasticsearch, index: str) -> None:
    """
    Lists all indices and their mappings in Elasticsearch.

    @param client: Elasticsearch client

    Usage:

    ```python
    list_indices_and_mappings(client)
    ```
    """
    # Get all indices and their mappings
    try:
        response = client.indices.get_mapping(index=index, pretty=True)
        print(response)
    except NotFoundError as e:
        print(e)


def print_document_count(client: Elasticsearch, index: str) -> None:
    """
    Prints the number of documents in the specified index.

    @param client: Elasticsearch client
    @param index_name: The name of the index

    Usage:

    ```python
    print_document_count(client, index_name)
    ```
    """
    try:
        response = client.count(index=index)
        doc_count = response.get("count", 0)
        print(f"Document Count for index '{index}': {doc_count}")
    except NotFoundError:
        print(f"No such index: {index}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Usage:
# Assuming es_client is your Elasticsearch client
# list_indices_and_mappings(es_client)
