"""
Elastic Search Class for ES Service
"""
from typing import Dict, List, Optional
from elasticsearch import Elasticsearch

from model.interface import ESDocument

from .index.index import (
    create_index,
    delete_index,
    list_indices_and_mappings,
    print_document_count,
)
from .document.insert_document import insert_document

from .exceptions.es_exceptions import (
    ElasticsearchInsertionError,
    SSLCertificateNotProvided,
)


# Run this export PYTHONPATH=/home/chin/projects/Search/Elasticsearch/SBERT before running this script


class ElasticSearchService:
    """
    ElasticSearch Class
    """

    def __init__(
        self, cert_location: str = "", host: str = "localhost", port: int = 9200
    ):
        if cert_location == "":
            raise SSLCertificateNotProvided

        self.client = Elasticsearch(
            [{"host": host, "port": port, "scheme": "https"}],
            verify_certs=True,
            ca_certs=cert_location,
            basic_auth=("elastic", "password"),
        )

    def create_index(
        self,
        model: ESDocument | str,
        index_name: Optional[str] = None,
        embedding: bool = False,
    ) -> None:
        """
        Create an Index in Elasticsearch
        """
        create_index(self.client, model, index_name, embedding)

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
        insert_document(self.client, document, index_name, id)

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

    def semantic_search(
        self,
        query_vector: List[float],
        index_name: str,
        size: int = 10,
        search_filter: Optional[Dict] = None,
        aprroximate: bool = False,
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

        query_dict = {
            "field": "embedding",
            "query_vector": query_vector,
            "k": size,
            "num_candidates": 10,
        }

        if search_filter:
            field, value = next(iter(search_filter.items()))
            filter_query = (
                {"term": {f"{field}.keyword": value}}
                if not aprroximate
                else {"fuzzy": {field: {"value": value, "fuzziness": 2}}}
            )
            query_dict["filter"] = {"bool": {"must": filter_query}}

        res = self.client.search(
            knn=query_dict,
            index=index_name,
            source_excludes=["embedding"],
        )

        if debug:
            for hit in res["hits"]["hits"]:
                print(hit)

        return res

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
