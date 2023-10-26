"""
Application entry point for Interacting with Elasticsearch

Even if Index Schema is defined with Embedding - 
we can still insert Documents without providing the Embedding

Insert 10 Posts
Insert 1 User 

Which Posts to show to user?

User-Post Scores Exist in Index 
"""
from operator import pos
from typing import List
from numpy import sort
import pandas as pd

from model.models import User, Post, UserPostScore

from elastic_search.es_service import ElasticSearchService

from ml.transformer.sbert.sbert_transformer import SbertTransformer

# @ML_Transformer
# transformer = SbertTransformer()

# @Client
# client = ElasticSearchService.create_service(cert_location="ssl/ca.crt")

from mock_data.data import users, posts, user_scores


# @Functions
def query_posts_for_user(client: ElasticSearchService, user: User):
    """
    Get Posts for User with Highest Scores in Descending Order
    """
    # First get the user's top scored Post_id's from UserPostScores

    filter_conditions = {"username": user.username}

    score_documents = client.search_by(
        index_name="user_post_scores",
        filter_conditions=filter_conditions,
        sort_by=("score", "desc"),
    )

    for score in score_documents:
        print("Printing Scores result\n")
        print(score)

    post_ids_scores = {doc["post_id"]: doc["score"] for doc in score_documents}
    post_ids = list(post_ids_scores.keys())

    # 2: Query the posts index with the retrieved post_ids to get the actual posts

    post_query_body = {"post_id": post_ids}

    post_documents = client.search_by(
        index_name="posts", filter_conditions=post_query_body
    )

    scores = [
        {"post_id": post_id, "score": post_ids_scores[post_id]}
        for post_id in post_ids_scores
    ]

    posts: List[Post] = [Post(**doc) for doc in post_documents]

    for post in posts:
        print(f"Post ID : {post.post_id}\n")

    return posts, scores


def list_mapping(
    client: ElasticSearchService,
):
    client.list_indices_and_mappings(index="user_post_scores")
    client.list_indices_and_mappings(index="posts")


def insert_data(
    client: ElasticSearchService,
):
    # Insert Scores and Posts
    for score in user_scores:
        client.insert_document(
            document=score, id=score.hash(), index_name=score.get_index_name()
        )
    for post in posts:
        client.insert_document(
            document=post, id=post.hash(), index_name=post.get_index_name()
        )


# client.list_indices()

# insert_data()

# list_mapping()

# query_posts_for_user(users[0])


# @Create
def create_indexes(client: ElasticSearchService):
    client.create_index(User, embedding=True)
    client.create_index(UserPostScore, embedding=True)
    client.create_index(Post, embedding=True)


# @Delete
def delete_indexes(client: ElasticSearchService):
    client.delete_index(User)
    client.delete_index(UserPostScore)
    client.delete_index(Post)


# Query Scores for user
def run_client_dynamically(client: ElasticSearchService):
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
