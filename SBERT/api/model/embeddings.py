"""
Models for Embeddings
"""
from typing import List
from pydantic import BaseModel


class UserEmbedding(BaseModel):
    """
    User Embedding Document
    """

    username_embedding: List[float]
    email_embedding: List[float]
    gender_embedding: List[float]
    country_embedding: List[float]
    age_embedding: List[float]
    combined_embedding: List[float]
