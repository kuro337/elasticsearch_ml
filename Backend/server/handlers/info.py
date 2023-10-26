"""
@Websocket
@ElasticSearch

- Sends a User Object - server retrieves Posts with Highest Scores

"""

from fastapi import WebSocket
from elastic_search.es_service import ElasticSearchService


async def socket_info(websocket: WebSocket, payload: dict):
    """
    @WebSockets
    @Helper

    - Sends a User Object - server retrieves Posts with Highest Scores
    """

    available_actions = ["sendEntity", "getTopPosts", "trainModel"]
    await websocket.send_text(
        f"Message received: {payload}. Available actions: {', '.join(available_actions)}"
    )

    print("Help Response Sent!")
