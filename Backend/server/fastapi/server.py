"""
Websockets Server
"""


from fastapi import FastAPI
from fastapi import WebSocket

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
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


# To run: uvicorn main:app --reload
