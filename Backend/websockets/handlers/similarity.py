"""
@Websocket
@ElasticSearch

- Sends a User Object - server retrieves Posts with Highest Scores

"""
import json
from fastapi import WebSocket

from ml.transformer.sbert.sbert_transformer import SbertTransformer
from elastic_search.es_service import ElasticSearchService
from model.interface import ESDocument

from exceptions.server_exceptions import (
    UnknownESEntityError,
    RecommendationSystemInternalError,
)

from ws_utils.serialize import serialize_dict_to_esdoc
from methods.methods import query_embeddings_for_similarity


async def get_similar_entities(
    client: ElasticSearchService,
    transformer: SbertTransformer,
    payload: dict,
    websocket: WebSocket,
):
    """
    @WebSockets
    @GET /userTopPosts

    - Sends a User Object - server retrieves Posts with Highest Scores
    """
    # 1. Serialize User Object
    try:
        document: ESDocument = serialize_dict_to_esdoc(payload)

    except UnknownESEntityError as e:
        raise RecommendationSystemInternalError(e)

    # 2. Using SBERT Embedding to get Similar Documents
    results = query_embeddings_for_similarity(
        document=document, client=client, transformer=transformer
    )
    print("Received Results\n")

    document_pk = document.get_primary_key()

    print(f"Primary Key in Results is {document_pk}\n")

    # 3. Retrieve Full Similar Documents from Results

    doc_ids_and_scores = {doc[document_pk]: doc["score"] for doc in results}
    doc_ids = list(doc_ids_and_scores.keys())

    print("Searching Scores\n")

    documents_from_ids = client.search_by(
        index_name=document.get_index_name(),
        filter_conditions={document_pk: doc_ids},
    )

    scores = [
        {document_pk: doc_id, "score": doc_ids_and_scores[doc_id]}
        for doc_id in doc_ids_and_scores
    ]

    # 4. Initialize Documents from IDs

    docs = [type(document)(**doc).dump_document() for doc in documents_from_ids]

    # 5. Send Response to Client

    response = {"action": "similar_entities", "data": docs, "scores": scores}
    print(response)

    await websocket.send_text(
        json.dumps(
            {
                "data": {
                    "action": "similar_entities",
                    "results": {document.get_index_name(): docs, "scores": scores},
                }
            }
        )
    )

    print("Similarity data sent!")
