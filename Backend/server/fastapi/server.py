"""
Websockets + REST HTTP Server
"""
from fastapi import FastAPI
from fastapi import WebSocket
import json

from model.models import Interaction, User, Post, Product, ESDocument

app = FastAPI()


@app.get("/")
async def read_root():
    """
    Root Endpoint

    @Response: Hello World
    """
    return {"Hello": "World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Websockets Endpoint
    """
    print(f"Websocket endpoint: {websocket}")

    User

    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(f"Message received:\n {data}")

        data = json.loads(data)

        print(f"Entity received:\n {data.get('entity')}")

        print(f"Data received:\n {data.get('data')}")

        # Deserialize the JSON string
        # data_dict = json.loads(data)

        # Parse the dictionary into the Interaction model
        # interaction = Interaction(**data_dict)

        # Now you have a Pydantic object and can access its attributes like interaction.interaction_type
        # print(interaction.interaction_type)
        # print(interaction.get_mapping())
        # print(interaction)

        await websocket.send_text(f"Message text was: {data}")


# To run: uvicorn main:app --reload

# uvicorn server:app --reload
