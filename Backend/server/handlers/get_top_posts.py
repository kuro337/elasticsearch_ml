"""
@Websocket
@ElasticSearch

- Sends a User Object - server retrieves Posts with Highest Scores

"""
import json
from fastapi import WebSocket
from elastic_search.es_service import ElasticSearchService
from utils.serialize import serialize_dict_to_esdoc
from elastic_search.exceptions.es_exceptions import ElasticsearchInsertionError
from exceptions.server_exceptions import (
    UnknownESEntityError,
    DocumentInsertionError,
    RecommendationSystemInternalError,
    NotUserEntityError,
)

from app import query_posts_for_user


async def get_user_top_posts(
    client: ElasticSearchService, payload: dict, websocket: WebSocket
):
    """
    @WebSockets
    @GET /userTopPosts

    - Sends a User Object - server retrieves Posts with Highest Scores
    """
    # 1. Serialize User Object
    try:
        user = serialize_dict_to_esdoc(payload)

    except UnknownESEntityError as e:
        raise RecommendationSystemInternalError(e)

    if user.get_index_name() != "users":
        raise NotUserEntityError

    # 2. Query for Top Posts using User()
    try:
        top_user_posts, post_scores = query_posts_for_user(client, user)
    except Exception as e:
        raise RecommendationSystemInternalError(e)

    posts_data = [post.dump_document() for post in top_user_posts]

    response = {"action": "sendPosts", "data": posts_data, "scores": post_scores}
    print(response)

    await websocket.send_text(
        json.dumps(
            {
                "data": {
                    "action": "getTopPosts",
                    "results": {"posts": posts_data, "scores": post_scores},
                }
            }
        )
    )

    print("Posts data sent!")
