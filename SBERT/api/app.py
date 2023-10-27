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
from model.interface import ESDocument
from numpy import delete, insert, sort
import pandas as pd

from model.models import User, Post, UserPostScore, UserEmbeddings, PostEmbeddings

from elastic_search.es_service import ElasticSearchService

from ml.transformer.sbert.sbert_transformer import SbertTransformer

from mock_data.data import (
    users,
    posts,
    user_scores,
    documents,
    similar_post,
    similar_user,
)

from methods.methods import (
    insert_data,
    list_mapping,
    query_posts_for_user,
    insert_embeddings_from_documents,
    query_embeddings_for_similarity,
    create_indexes,
    delete_indexes,
)
from sympy import use

# @ML_Transformer
# transformer = SbertTransformer()

# @Client
# client = ElasticSearchService.create_service(cert_location="ssl/ca.crt")
# delete_indexes(client=client)

# client.create_index(UserEmbeddings)
# client.create_index(PostEmbeddings)
# create_indexes(client=client)

# insert_data(client, documents)

# query_posts_for_user(client=client, user=users[0])

# client.list_indices_and_mappings("user_embeddings")
# client.list_indices_and_mappings("post_embeddings")

# insert_embeddings_from_documents(
#     client=client, documents=users, transformer=transformer
# )

# insert_embeddings_from_documents(
#     client=client, documents=posts, transformer=transformer
# )

# query_embeddings_for_similarity(
#     document=similar_post, client=client, transformer=transformer
# )

# list_mapping(client=client)

# client.list_indices()


# list_mapping()

# query_posts_for_user(users[0])
