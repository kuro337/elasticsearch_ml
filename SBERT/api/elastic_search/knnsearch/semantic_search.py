"""
ES Class function implementation to create and delete an index in Elasticsearch.
"""

import json
from typing import Dict, Optional, List
from elasticsearch import Elasticsearch, NotFoundError, BadRequestError
from model.interface import ESDocument


def semantic_search(
    client: Elasticsearch,
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
        approximate=False,
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
            if not approximate
            else {"fuzzy": {field: {"value": value, "fuzziness": 2}}}
        )
        query_dict["filter"] = {"bool": {"must": filter_query}}

    res = client.search(
        knn=query_dict,
        index=index_name,
        source_excludes=["embedding"],
    )

    if debug:
        for hit in res["hits"]["hits"]:
            print(hit)

    hits = res["hits"]["hits"]
    parsed_data = parse_hits(hits)

    return parsed_data


def parse_hits(hits):
    """
    Parse the hits from Elasticsearch into a list of dictionaries,
    including all the desired information.
    """
    parsed_data = []
    for hit in hits:
        data = hit["_source"]
        data["id"] = hit["_id"]
        data["index"] = hit["_index"]
        data["score"] = hit["_score"]
        parsed_data.append(data)
    return parsed_data
