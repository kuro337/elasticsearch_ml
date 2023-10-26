"""
@Websocket
@ElasticSearch

- Serialize Document and Insert into Elasticsearch
"""

from fastapi import WebSocket
from utils.serialize import serialize_dict_to_esdoc
from elastic_search.es_service import ElasticSearchService
from exceptions.server_exceptions import DocumentInsertionError, UnknownESEntityError
from elastic_search.exceptions.es_exceptions import ElasticsearchInsertionError


async def serialize_and_insert_document(
    ws: WebSocket, client: ElasticSearchService, payload: dict
):
    """
    @Websocket
    @ElasticSearch

    - Serialize Document and Insert into Elasticsearch
    """
    print("Serializing and Inserting Document")

    try:
        es_document = serialize_dict_to_esdoc(payload)

    except UnknownESEntityError as e:
        raise DocumentInsertionError(e)

    # try:
    #     client.insert_document(es_document)

    # except ElasticsearchInsertionError as e:
    #     raise DocumentInsertionError(e)

    print("Document Inserted")

    await ws.send_text(
        f"Document Successfully Inserted into Index {es_document.get_index_name()}"
    )
    # return es_document
