"""
ES Class function implementation to create and delete an index in Elasticsearch.
"""

import json
from typing import Dict, Optional, Union, Type
from elasticsearch import Elasticsearch, NotFoundError, BadRequestError
from model.interface import ESDocument
from elastic_search.exceptions.es_exceptions import ElasticsearchIndexAlreadyExists


def create_index(
    client: Elasticsearch,
    model: Union[Type[ESDocument], ESDocument, str],
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
    # index_name = index_name or (
    #     model.get_index_name() if isinstance(model, ESDocument) else model
    # )

    # mappings = {"properties": {f"{key}": {"type": "text"} for key in model.keys()}}

    # mappings = model.get_mapping()

    if isinstance(model, type) and issubclass(model, ESDocument):
        index_name = index_name or getattr(model, "get_index_name")(model)
        mappings = getattr(model, "get_mapping")(model)
        print("Instance Class passed", index_name, mappings)

    elif isinstance(model, ESDocument):
        index_name = model.get_index_name()
        mappings = model.get_mapping()
        print("Actual instance passed", index_name)
    # If the model is a string
    else:
        index_name = index_name or model

    if embedding:
        mappings["properties"]["embedding"] = {
            "type": "dense_vector",
            "dims": 768,
            "index": True,
            "similarity": "cosine",
        }
    try:
        client.indices.create(index=index_name, body={"mappings": mappings})
    except BadRequestError as e:
        if e == "index_already_exists_exception":
            raise ElasticsearchIndexAlreadyExists(
                f"Index {index_name} already exists"
            ) from e
    except Exception as e:
        # This will catch any other exceptions that are being raised.
        print(f"An unexpected error occurred: {e}")

    print(f"Index {index_name} created successfully.")


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

        # Convert the response to a dictionary before serializing to JSON
        if hasattr(response, "to_dict"):
            response_dict = response.to_dict()
        else:
            response_dict = dict(
                response
            )  # This is a fallback and might not be necessary depending on the actual type of `response`

        print(json.dumps(response_dict, indent=4))
    except NotFoundError as e:
        print(f"Index not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


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


def list_all_indices(client: Elasticsearch) -> None:
    """
    Lists all indices in Elasticsearch.

    @param client: Elasticsearch client
    """
    try:
        response = client.cat.indices(format="json")
        for index_info in response:
            print(index_info["index"])
    except Exception as e:
        print(f"An error occurred: {e}")


# Usage:
# Assuming es_client is your Elasticsearch client
# list_indices_and_mappings(es_client)
