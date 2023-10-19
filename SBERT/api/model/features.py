"""
Feature Engineering
"""
from typing import List
from pydantic import BaseModel
from model.models import User


class UserFeatures(BaseModel):
    """
    User Features
    """

    user: User

    favorite_language: str
    top_languages: List[str]
    total_interactions: int
    total_likes: int
    total_dislikes: int
    total_comments: int


class Config:
    """
    User Features
    """

    schema_extra = {
        "example": {
            "user": {
                "username": "JohnDoe",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "gender": "Male",
                "country": "USA",
                "age": 28,
            },
            "favorite_language": "English",
            "top_languages": ["English", "Spanish"],
            "total_interactions": 100,
            "total_likes": 70,
            "total_dislikes": 5,
            "total_comments": 25,
        }
    }


class PostFeatures(BaseModel):
    """
    Post Features
    """

    post_id: str
    count_likes: int
    count_male_likes: int
    count_female_likes: int


class LanguageFeatures(BaseModel):
    """
    Lang Features
    """

    language: str
    count_interactions: int
    count_male_interactions: int
    count_female_interactions: int
