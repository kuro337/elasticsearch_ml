"""
Application entry point for Interacting with Elasticsearch

Even if Index Schema is defined with Embedding - 
we can still insert Documents without providing the Embedding

Insert 10 Posts
Insert 1 User 

Which Posts to show to user?

User-Post Scores Exist in Index 
"""

from typing import List, Optional
from model.interface import ESDocument
from numpy import sort
import pandas as pd

from model.models import PostEmbeddings, User, Post, UserPostScore, UserEmbeddings
from model.interface import ESDocument, ESDocumentWithEmbedding

from elastic_search.es_service import ElasticSearchService

from ml.transformer.sbert.sbert_transformer import SbertTransformer

# @ML_Transformer
# transformer = SbertTransformer()

# @Client
# client = ElasticSearchService.create_service(cert_location="ssl/ca.crt")

from mock_data.data import users, posts, user_scores

# client.list_indices()

# insert_data()

# list_mapping()

# query_posts_for_user(users[0])


# @Functions
def query_posts_for_user(client: ElasticSearchService, user: User):
    """Get Posts for User with Highest Scores in Descending Order"""

    filter_conditions = {"username": user.username}
    score_documents = client.search_by(
        index_name="user_post_scores",
        filter_conditions=filter_conditions,
        sort_by=("score", "desc"),
    )

    for doc in score_documents:
        print("Score Doc for User", doc)

    post_ids_scores = {doc["post_id"]: doc["score"] for doc in score_documents}
    post_ids = list(post_ids_scores.keys())

    post_documents = client.search_by(
        index_name="posts",
        filter_conditions={"post_id": post_ids},
    )

    for doc in post_documents:
        print("Posts Matching PostID from Score Doc", doc)

    scores = [
        {"post_id": post_id, "score": post_ids_scores[post_id]}
        for post_id in post_ids_scores
    ]
    posts = [Post(**doc) for doc in post_documents]

    return posts, scores


def query_embeddings_for_similarity(
    client: ElasticSearchService,
    document: Optional[ESDocumentWithEmbedding] = None,
    transformer: Optional[SbertTransformer] = None,
    index_name: Optional[str] = None,
    query_vector: Optional[List[float]] = None,
):
    """
    Querying ES Index

    Can pass it List[float] and Index Name Directly
    Or can pass Document Only

    @Usage
    ```py
    # Pass the Document , ES Client, and Transformer

    results = query_embeddings_for_similarity(
    document=similar_post, client=client, transformer=transformer
    )

    # Pass the Query Embedding and Index Name Directly
    results = query_embeddings_for_similarity(query_vector=List[float],client=client)

    # print results
    ```
    """
    if document is None and transformer is None:
        raise ValueError(
            "Either a document or transformer must be provided to query_embeddings_for_similarity"
        )

    if query_vector is None:
        if transformer is None:
            raise ValueError(
                "Either a query_vector or transformer must be provided to query_embeddings_for_similarity"
            )
        query_vector = transformer.convert_doc_to_vector(document.stringify())
        embedding_doc = document.get_embedding_document(query_vector)

    if index_name is None:
        if document is None:
            raise ValueError(
                "Either a index_name or document must be provided to query_embeddings_for_similarity"
            )
        index_name = embedding_doc.get_index_name()

    print(index_name)

    results = client.semantic_search(
        query_vector=query_vector,
        index_name=index_name,
    )
    print("Original Doc\n", document, "\n")

    for i, result in enumerate(results):
        print(f"Similarity Result {i}\n {result}\n")

    return results


def list_mapping(
    client: ElasticSearchService,
):
    client.list_indices_and_mappings(index="user_post_scores")
    client.list_indices_and_mappings(index="posts")


def insert_data(
    client: ElasticSearchService,
    documents: List[ESDocument],
):
    for doc in documents:
        client.insert_document(document=doc)


def insert_embeddings_from_documents(
    client: ElasticSearchService,
    documents: List[ESDocumentWithEmbedding],
    transformer: SbertTransformer,
):
    """
    Insert Embeddings into their Indexes (UserEmbeddings, PostEmbeddings)
    """
    for doc in documents:
        if not hasattr(doc, "get_embedding_document"):
            # If the doc doesn't have the method `get_embedding_document`, skip it
            continue

        combined_embedding: List[float] = transformer.convert_doc_to_vector(
            doc.stringify()
        )

        embedding_doc = doc.get_embedding_document(combined_embedding)

        client.insert_document(document=embedding_doc)


# @Create
def create_indexes(client: ElasticSearchService):
    """
    Create Index
    """
    client.create_index(User)
    client.create_index(UserPostScore)
    client.create_index(Post)


# @Delete
def delete_indexes(client: ElasticSearchService):
    client.delete_index(User)
    client.delete_index(UserPostScore)
    client.delete_index(Post)
    client.delete_index(PostEmbeddings)
    client.delete_index(UserEmbeddings)


# Query Scores for user
def run_client_dynamically(
    documents: List[ESDocument],
    transformer: SbertTransformer,
    client: ElasticSearchService,
):
    """
    @Run

    - Client on a List[ESDocument]
    """
    # @Client Usage
    for doc in documents:
        client.doc_count(index=doc.get_index_name())

        print("Creating index\n\n")

        client.create_index(doc, embedding=True)

        print("Listing index\n\n")
        client.list_indices_and_mappings(index=doc.get_index_name())

        print("Creating Hash\n\n")
        # Generate Hash of the User Document for the Document ID
        doc_hash = doc.hash()
        print(doc_hash)

        print("Creating Embedding\n\n")
        # Generate Vector<Float> Embedding from User Document and add it to User Object
        combined_embedding: List[float] = transformer.convert_doc_to_vector(
            doc.stringify()
        )
        # doc.embedding = combined_embedding

        print("Inserting Embedding\n\n")

        # Insert the Document with Embedding into Elasticsearch
        client.insert_document(
            document=doc, id=doc.hash(), index_name=doc.get_index_name()
        )

        result = client.semantic_search(
            query_vector=combined_embedding, index_name=doc.get_index_name(), debug=True
        )

        results_df = pd.DataFrame(result)

        # Display the DataFrame
        print(results_df)
        print(results_df.columns)
        print(results_df.head())
        print(results_df.describe())

        # Fuzzy Search
        print("Fuzzy Searching Embedding\n\n")

        search_filter = {"country": "jpn"}

        result = client.semantic_search(
            query_vector=combined_embedding,
            index_name=doc.get_index_name(),
            search_filter=search_filter,
            size=5,
            approximate=True,
            debug=True,
        )

        # Now, create a DataFrame using this list of documents
        results_df = pd.DataFrame(result)

        # Display the DataFrame
        print(results_df)
        print(results_df.columns)
        print(results_df.head())
        print(results_df.describe())
