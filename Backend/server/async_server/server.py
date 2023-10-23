"""
Websockets + REST HTTP Server

Run from Backend/server

Understands directory structure 

python -m async_server.server
"""
import json

from utils.serialize import serialize_ws_data_esdoc


from elastic_search.es_service import ElasticSearchService


from exceptions.server_exceptions import UnknownESEntityError

from fastapi import FastAPI
from fastapi import WebSocket


if __name__ == "__main__":
    print(__package__)


app = FastAPI()

# es_client = ElasticSearchService.create_service(cert_location="ssl/ca.crt")


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

    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(f"Message received:\n {data}")

        # Deserialize the JSON string
        data_dict = json.loads(data)

        print(f"Entity received:\n {data_dict.get('entity')}")

        print(f"Data received:\n {data_dict.get('data')}")

        try:
            entity_instance = serialize_ws_data_esdoc(data)
            print(f"Created instance: {entity_instance}")

            # ... you can now interact with the entity instance ...

        except UnknownESEntityError as e:
            print(f"Error: {e}")
            await websocket.send_text(f"Error: {e}")

        # es_client.doc_count(index=entity_instance.get_index_name())
        entity_instance.get_mapping()

        await websocket.send_text(f"Message text was: {data}")


# To run: uvicorn main:app --reload

# uvicorn server:app --reload

# Run from Backend/server
# uvicorn async_server.server:app --reload
