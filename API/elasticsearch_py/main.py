from fastapi import FastAPI, Request, HTTPException, Body, status
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

from typing import Optional, List, Dict, Union, Type
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from pydantic.fields import Field


from server.utils.check_connection import check_connection
from data.models.models import DataRequest, User, Metadata, Post
from server.utils.logger import init_logger
from settings.constants import module_name

from server.exceptions.exception_handlers import (
    universal_exception_handler,
    http_exception_handler,
)

import json


logger = init_logger(module_name)

logger.info(f"Module {module_name}")

app = FastAPI()
# app.add_exception_handler(Exception, universal_exception_handler)
# app.add_exception_handler(HTTPException, http_exception_handler)

es = Elasticsearch(hosts=["http://localhost:9200"])


@app.on_event("startup")
async def startup_event():
    try:
        if check_connection(es):
            logger.info("Connection successful")
    except ConnectionError as e:
        logger.error(f"Connection Failed to Elasticsearch:{e}")
    except Exception as e:
        logger.error(f"An error occurred while connecting to Elasticsearch: {e}")


from pydantic import BaseModel, ValidationError, validator


class IndexInformation(BaseModel):
    settings: dict = Field(
        ..., example={"number_of_shards": 5, "number_of_replicas": 1}
    )
    mappings: dict = Field(
        ...,
        example={
            "properties": {"field1": {"type": "text"}, "field2": {"type": "keyword"}}
        },
    )


# Field - how to import it?
# from pydantic.fields import Field

"""
Create an Index 

curl -X POST "http://localhost:8000/create-index/your-index-name" -H "Content-Type: application/json" -d'
{
  "settings": {
    "number_of_shards": 5,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "field1": {
        "type": "text"
      },
      "field2": {
        "type": "keyword"
      }
    }
  }
}'

"""


@app.post("/create-index/{index_name}")
async def create_index(index_name: str, index_info: IndexInformation = Body(...)):
    logger.info(f"Creating index {index_name}")
    try:
        if not es.indices.exists(index=index_name):
            es.indices.create(
                index=index_name, body=json.loads(index_info.model_dump_json())
            )
            return {
                "status": "success",
                "message": f"Index {index_name} successfully created",
            }
        else:
            return {
                "status": "information",
                "message": f"Index {index_name} already exists",
            }
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )


# @app.post("/create-index/{index_name}")
# async def create_index(index_name: str):
#     logger.info(f"Creating index {index_name}")
#     try:
#         if not es.indices.exists(index=index_name):
#             es.indices.create(index=index_name)
#             return {
#                 "status": "success",
#                 "message": f"Index {index_name} successfully created",
#             }
#         else:
#             return {
#                 "status": "information",
#                 "message": f"Index {index_name} already exists",
#             }
#     except Exception as e:
#         logger.error(f"An error occurred: {e}")
#         return JSONResponse(
#             status_code=500,
#             content={"detail": "Internal server error"},
#         )


"""
If Req Body does not match - it goes to the exception block

model: Type[BaseModel] = models.get(request.type)
-> Denotes that model is of type BaseModel
-> model is a subclass of BaseModel and not an instance of BaseModel

"""


@app.post("/{index_name}/insert")
async def insert_document(index_name: str, request: DataRequest):
    models = {"user": User, "metadata": Metadata, "post": Post}

    model: Type[BaseModel] = models.get(request.type)

    if model is None:
        logger.error(f"Unknown type provided: {request.type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown type {request.type}",
        )

    try:
        model_instance = model.model_validate(request.data)
        logger.info(f"Parsed Data: {model_instance.model_dump()}")

    except ValidationError as e:
        logger.error("Parsing Failed")
        # If request.data doesn't fit the Pydantic model's structure, a ValidationError is raised.
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )

    try:
        logger.info("Parsing Successful, inserting document.")
        res = es.index(index=index_name, body=model_instance.dict())
        return res
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/{index_name}/query/")
async def query_index(index_name: str, q: Optional[str] = ""):
    body = {"query": {"query_string": {"query": q}}}
    res = es.search(index=index_name, body=body)
    return res["hits"]["hits"]


@app.put("/{index_name}/update/{doc_id}")
async def update_document(index_name: str, doc_id: str, document: dict):
    res = es.update(index=index_name, id=doc_id, body={"doc": document})
    return res
