# Fast API

- Running


```bash
pip install fastapi uvicorn 'uvicorn[standard]' gunicorn


uvicorn server:app --reload

server    -> Name of File Containing Server and Logic server.py
app       -> Name of FastAPI Instance we declare using FastAPI()

# If file -> main.py and app = FastAPI() -> uvicorn main:app --reload
```

- `server.py` 
```python
"""
Websockets + REST HTTP Server
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
    """
    Websockets Endpoint
    """
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)

# To run: uvicorn main:app --reload
```

```bash

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. FastAPI is built on top of Starlette for the web parts and Pydantic for the data parts.

Gunicorn is a pre-fork worker model based server. It pre-forks multiple instances of your application, each of which is handled by a single thread. This means that it can handle multiple requests simultaneously by assigning each incoming request to a specific worker. It's a WSGI server that interfaces with Python applications, it's often used to serve applications to web servers like Nginx or Apache.

Uvicorn, on the other hand, is an ASGI server, meaning it serves Python applications that are built to communicate with the web and websocket protocols. ASGI is the successor to WSGI, and it's designed to handle asynchronous operations and WebSockets in addition to regular HTTP requests.

Server Type:

Gunicorn: It's often termed a "pre-fork worker" model. Traditional WSGI servers (like Gunicorn or uWSGI) that are based on the pre-fork worker model can handle multiple requests simultaneously by forking the main process into multiple subprocesses at startup, each handled by a different CPU core.
Uvicorn: It's a lightning-fast ASGI server implementation, using uvloop and httptools. Until recently Python web frameworks were typically synchronous-only. Uvicorn serves as an ASGI server to run asynchronous web applications written with frameworks like FastAPI, and it's generally single-threaded, but it's designed to handle long-lived network connections.
Concurrency Handling:

Gunicorn: Each worker, by default, is a synchronous worker of the type sync. Gunicorn also supports asynchronous workers but the default worker is designed to handle only one request at a time. Gunicorn spins multiple workers (sub-processes, not threads) to handle multiple requests in parallel.
Uvicorn and FastAPI: They leverage Python's asyncio. There's no thread creation for each request; instead, asynchronous applications yield control to the event loop, allowing other tasks to run during network IO or other 'downtime' in processing. This design enables high concurrency even with a small number of threads.
To get the best of both worlds in production, Uvicorn is often run behind Gunicorn (using the gunicorn -k uvicorn.workers.UvicornWorker command). This setup uses Gunicorn for its robustness and ability to manage multiple workers, and Uvicorn for its ability to handle asynchronous ASGI applications. Each Gunicorn worker will run a Uvicorn server in a single thread.

This combination does not work per se in the "one thread per request" model of traditional servers or the pure "single-threaded event-driven" model of servers like Node.js. It's more of a hybrid, leveraging multi-process (Gunicorn) and asynchronous event-driven IO (Uvicorn/FastAPI) models.

```
