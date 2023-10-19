from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from elasticsearch.exceptions import ConnectionError

from .services.elasticsearch_service import ElasticsearchService
from .models import MyDataModel, User, Post, Page, Session, Metadata

import json
from pydantic import ValidationError

# Object Mapper and Error Type for Invalid Mapping
from .utils.object_mapper import get_entity
from .types.error.entity_error import InvalidEntityTypeError


"""
Update urls to include the new view whenever we add a new function

Currently Using Pydantic to Serialize

Should be using Django REST framework (DRF) Serializers instead of Pydantic


"""


class CreateIndexView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        try:
            data = json.loads(request.body)
            index_settings = data.get(
                "index_settings"
            )  # You should validate this as well
            es_service = ElasticsearchService(index_name="your_index_name")
            es_service.create_index(index_settings)
            return JsonResponse({"message": "Index created successfully"})
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)


"""
curl -X POST http://127.0.0.1:8000/httpes/insert-data/ -H "Content-Type: application/json" 
-d '{"type": "user", "data": {"username": "johndoe", "email": "johndoe@example.com"}}'

**args **kwargs in case of extra Args

"""


@method_decorator(csrf_exempt, name="dispatch")
class InsertCustomDataView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        print("Request Body : ", request.body)

        raw_data = json.loads(request.body)
        data_type = raw_data.get("type")
        data_content = raw_data.get("data")

        if not data_type or not data_content:
            return JsonResponse(
                {"error": "Type and data fields are required"}, status=400
            )

        try:
            entity_class = get_entity(data_type)
        except InvalidEntityTypeError as e:
            return JsonResponse(
                {"error": "Invalid Type Provided :" + str(e)}, status=400
            )

        try:
            # Validate and deserialize the data
            entity_instance = entity_class(**data_content)

            print("Serialized Entity Instance : ", entity_instance)
            es_service = ElasticsearchService(index_name="your_index_name")
            es_service.insert_data(entity_instance.dict())

            return JsonResponse({"message": "Data inserted successfully"})
        except ValidationError as e:  # This catches Pydantic validation errors
            return JsonResponse({"error": e.errors()}, status=400)
        except ConnectionError as e:  # This catches Elasticsearch connection errors
            return JsonResponse(
                {
                    "error": "Unable to connect to Elasticsearch. Please try again later."
                },
                status=503,
            )


# Making the view csrf exempt so that we can test it using Postman
# @method_decorator(csrf_exempt, name="dispatch")
# class InsertDataView(View):
#     def post(self, request, *args, **kwargs):
#         try:
#             # Validate request body using Pydantic
#             data = MyDataModel(**json.loads(request.body))
#             es_service = ElasticsearchService(index_name="your_index_name")
#             es_service.insert_data(data.dict())
#             es_service.insert_data(data.model_dump())
#             return JsonResponse({"message": "Data inserted successfully"})
#         except ValueError as e:
#             return JsonResponse({"error": str(e)}, status=400)
#         except ConnectionError as e:
#             # Handle the connection error
#             return JsonResponse(
#                 {
#                     "error": "Unable to connect to Elasticsearch. Please try again later."
#                 },
#                 status=503,
#             )  # 503 Service Unavailable
