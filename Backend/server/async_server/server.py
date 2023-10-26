"""
@Backend
@Websockets 

- Async Server utilizing FastAPI and Websockets
- Provides Coordination for a Real Time Machine Learning Recommendation System
- Provides an Interface and fully featured ElasticSearch Client 
- Model Training , Scoring and Caching

@ Run
uvicorn async_server.server:app --reload

@ Path: Backend/server/
"""
import json

from fastapi import FastAPI
from fastapi import WebSocket

from utils.root_serialize import serialize_client_message

from handlers.insert_document import serialize_and_insert_document
from handlers.get_top_posts import get_user_top_posts
from handlers.train_model import train_model
from handlers.info import socket_info

from elastic_search.es_service import ElasticSearchService

from exceptions.server_exceptions import (
    DocumentInsertionError,
    RecommendationSystemInternalError,
    GLMModelTrainingFailure,
)

client = ElasticSearchService.create_service(cert_location="async_server/ca.crt")

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
      @Websockets /ws

      @Shape
      @ClientRequest

      ```json
      message = {
      action: "getTopPosts",
      payload: {
        entity: "User",
        data: user
      }
    };
    ```
    """
    print(f"Websocket endpoint: {websocket}")

    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        action, payload = serialize_client_message(data)

        if not action:
            continue

        print(f"Action received:\n {action}")

        if action == "ws_help":
            await socket_info(websocket, payload)

        elif action == "sendEntity":
            try:
                await serialize_and_insert_document(websocket, client, payload)
            except DocumentInsertionError as e:
                await websocket.send_text(f"Error: {e}")

        elif action == "getTopPosts":
            print(f"Getting top posts for user")
            try:
                await get_user_top_posts(client, payload, websocket)

            except RecommendationSystemInternalError as e:
                await websocket.send_text(f"Error: {e}")

        elif action == "trainModel":
            print(f"Training Model")
            try:
                await train_model(client, websocket)
            except GLMModelTrainingFailure as e:
                await websocket.send_text(f"Error: {e}")

            await websocket.send_text(f"Model Trained and Indexed Successfully!")

        else:
            await socket_info(websocket, payload)

        await websocket.send_text(f"{action} Success!")


@app.get("/")
async def read_root():
    """
    @REST
    @GET

    - Default HTTP REST Endpoint for Server

    @Response: Hello World
    """
    return {"Hello": "World"}
