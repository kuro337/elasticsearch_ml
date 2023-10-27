"""
ES Class function implementation to create and delete an index in Elasticsearch.
"""

import json
import logging

from typing import Optional, Union, Type
from elasticsearch import Elasticsearch, NotFoundError, BadRequestError
from model.interface import ESDocument
from elastic_search.exceptions.es_exceptions import ElasticsearchIndexAlreadyExists


logging.basicConfig(level=logging.INFO)


def create_index(
    client: Elasticsearch,
    model: Union[Type[ESDocument], ESDocument, str],
    index_name: Optional[str] = None,
) -> None:
    """
    Constructs an Index

    Can pass it an Instance , Class , or Document directly
    """
    logging.info("Starting the index creation process.")

    if isinstance(model, type) and issubclass(model, ESDocument):
        index_name = index_name or getattr(model, "get_index_name")(model)
        mappings = getattr(model, "get_mapping")(model)
        logging.info(
            "Instance Class passed. Index name: %s, Mappings: %s", index_name, mappings
        )

    elif isinstance(model, ESDocument):
        index_name = model.get_index_name()
        mappings = model.get_mapping()
        logging.info(
            "Actual instance passed. Index name: %s, Mappings: %s", index_name, mappings
        )

    else:
        index_name = index_name or model
        logging.info("Model passed as string. Using index name: %s", index_name)

    try:
        logging.info("Attempting to create index with name: %s", index_name)
        client.indices.create(index=index_name, body={"mappings": mappings})
        logging.info("Successfully created index with name: %s", index_name)

    except BadRequestError as e:
        logging.error("BadRequestError encountered: %s", e)
        if e == "index_already_exists_exception":
            logging.error("Index %s already exists.", index_name)
            raise ElasticsearchIndexAlreadyExists(
                f"Index {index_name} already exists"
            ) from e

    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)

    logging.info("Index creation process completed for index: %s", index_name)


def delete_index(
    client: Elasticsearch,
    model: Union[Type[ESDocument], ESDocument, str],
    index_name: Optional[str] = None,
) -> None:
    """
    Delete an Index in Elasticsearch
    """
    logging.info("Starting the index deletion process.")

    if isinstance(model, type) and issubclass(model, ESDocument):
        index_name = index_name or getattr(model, "get_index_name")(model)
        logging.info("Instance Class passed. Index name: %s", index_name)

    elif isinstance(model, ESDocument):
        index_name = model.get_index_name()
        logging.info("Actual instance passed. Index name: %s", index_name)

    else:
        index_name = index_name or model
        logging.info("Model passed as string. Using index name: %s", index_name)

    try:
        logging.info("Attempting to delete index with name: %s", index_name)
        client.indices.delete(index=index_name)
        logging.info("Successfully deleted index with name: %s", index_name)

    except NotFoundError:
        logging.error("Index %s not found.", index_name)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)

    logging.info("Index deletion process completed for index: %s", index_name)


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
