"""
Elastic Search Class for ES Service
"""
from typing import Dict, List, Optional, Any, Union, Type, Tuple
from elasticsearch import Elasticsearch, ConnectionError

from model.interface import ESDocument
from numpy import sort

from .index.index import (
    create_index,
    delete_index,
    list_indices_and_mappings,
    print_document_count,
    list_all_indices,
)

from .knnsearch.semantic_search import semantic_search
from .document.fetch_documents import fetch_documents, search_by
from .document.insert_document import insert_document

from .exceptions.es_exceptions import (
    ElasticsearchInsertionError,
    SSLCertificateNotProvided,
    ElasticsearchConnectionError,
)

import sys

# Run this export PYTHONPATH=/home/chin/projects/Search/Elasticsearch/SBERT before running this script


class ElasticSearchService:
    """
    ElasticSearch Class
    """

    @classmethod
    def create_service(
        cls, cert_location: str = "", host: str = "localhost", port: int = 9200
    ):
        """
        Abstracts the creation of the ElasticSearch Service
        """
        try:
            client = cls(cert_location=cert_location, host=host, port=port)
            print("ElasticSearch Client Successfully Created!")
            return client
        except SSLCertificateNotProvided as e:
            print(f"SSL Certificate error: {str(e)}")
        except ElasticsearchConnectionError as e:
            print(f"An error occurred during client Initialization:\n{str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

    def __init__(self, cert_location: str, host: str, port: int):
        if cert_location == "":
            raise SSLCertificateNotProvided("SSL Certificate not provided.")

        self.client = Elasticsearch(
            [{"host": host, "port": port, "scheme": "https"}],
            verify_certs=True,
            ca_certs=cert_location,
            basic_auth=("elastic", "password"),
        )

        if not self.client.ping():
            raise ElasticsearchConnectionError(
                "Connection Failed - Make sure Elasticsearch is Running."
            )

    def create_index(
        self,
        model: Union[Type[ESDocument], ESDocument, str],
        index_name: Optional[str] = None,
        embedding: bool = False,
    ) -> None:
        """
        Create an Index in Elasticsearch
        """
        create_index(
            self.client, model=model, index_name=index_name, embedding=embedding
        )

    def delete_index(
        self,
        index_name: str,
    ) -> None:
        """
        Create an Index in Elasticsearch
        """
        delete_index(self.client, index_name)

    def insert_document(
        self,
        document: ESDocument,
        index_name: Optional[str] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        Inserts a document into the corresponding index in Elasticsearch.
        """
        insert_document(self.client, document=document, index_name=index_name, id=id)

    def list_indices_and_mappings(self, index: str):
        """
        Prints the Indexes and their Schemas
        """
        list_indices_and_mappings(self.client, index)

    def doc_count(self, index: str) -> None:
        """
        Returns the number of documents in the index
        """
        print_document_count(self.client, index)

    def query(
        self,
        index_name: str,
        filter_conditions: Optional[Dict[str, Any]] = None,
        query: Optional[Dict[str, Any]] = None,
        sort_by: Optional[Tuple[str, str]] = None,
        keyword: bool = True,
    ) -> List[Dict]:
        """
        Fetch documents from an Index
         - Optionally Specify Fields and Values to Filter by
         - Filter results if the Field is a @Keyword
         - Queries the field as a Keyword - pass keyword=False to query as a Text Field

        @Usage
        ```python
        # Get All Docs for Index
        documents = es_service.fetch_documents(index_name="user_post_scores")
        for doc in documents:
            print(doc)

        # Filter Docs by a Condition
        filter_conditions = {"username": user.username}

        documents = es_service.query(
             index_name="user_post_scores",
             filter_conditions=filter_conditions,
             sort_by=("score", "desc"),
         )

        ```
        """
        return fetch_documents(
            self.client,
            index_name=index_name,
            filter_conditions=filter_conditions,
            query=query,
            sort_by=sort_by,
            keyword=keyword,
        )

    def search_by(
        self,
        index_name: str,
        filter_conditions: Optional[Dict[str, Any]] = None,
        query: Optional[Dict[str, Any]] = None,
        sort_by: Optional[Tuple[str, str]] = None,
        keyword: bool = True,
    ):
        """
        Search an Index

        @Usage
        ```py
        # Get all Documents that match a List[post_ids]

        post_query_body = {"post_id": post_ids}

        post_documents = es_service.search_by(
            index_name="posts", filter_conditions=post_query_body
        )

        # print posts
        ```
        """
        return search_by(
            self.client,
            index_name=index_name,
            filter_conditions=filter_conditions,
            query=query,
            sort_by=sort_by,
            keyword=keyword,
            size=100,
        )

    def semantic_search(
        self,
        query_vector: List[float],
        index_name: str,
        size: int = 10,
        search_filter: Optional[Dict] = None,
        approximate: bool = False,
        debug: Optional[bool] = False,
    ):
        """
        Performs Semantic Search on the index_name with the query_vector
        - Performs a Semantic Search using a Dense Vector on an Index in Elasticsearch
        - Pass in a query_vector and the index_name to perform the search on the index
        - Returns the top 10 results by default

        Can optionally specify a Filter to narrow down the search space
        - Pass in a search_filter to narrow down the search space

        Filtering is possible by Exact or Fuzzy Matching

        1. Performing a Semantic Search

        ```python
        # Convert an Object to an Embedding

        combined_embedding : List[float] = ml.convert_doc_to_vector(document)

        result = es_service.semantic_search(
            query_vector=combined_embedding, index_name="user", debug=True
        )

        # Prints Top 10 Results by default
        ```
        2. Example of Exact Matching

        ```python
        size = 5
        search_filter = {"country": "jpn"}

        result = es_service.semantic_search(
            query_vector=user_document.embedding,
            index_name="user",
            search_filter=search_filter,
            size=size,
            aprroximate=False,
            debug=True,
         )

        ```
        3. Example of Fuzzy Matching

        ```python
        search_filter = {"country": "jpn"}

        result = es_service.semantic_search(
            query_vector=user_document.embedding,
            index_name="user",
            search_filter=search_filter,
            size=5,
            aprroximate=True,
            debug=True,
         )
        ```
        """

        return semantic_search(
            self.client,
            query_vector,
            index_name,
            size,
            search_filter,
            approximate,
            debug,
        )

    def print_search_results(self, results) -> None:
        """
        Print the results of the search query
        """
        total_results = results.get("hits", {}).get("total", {}).get("value", 0)

        print(f"Total Results: {total_results}")

        # Get and print the top scores
        hits = results.get("hits", {}).get("hits", [])
        for hit in hits:
            score = hit.get("_score", None)
            doc_id = hit.get("_id", None)
            print(f"Document ID: {doc_id}, Score: {score}")

    def print_hello(self) -> None:
        """
        Print Hello ES!
        """
        print("Hello ES!")

    def list_indices(self):
        list_all_indices(self.client)
