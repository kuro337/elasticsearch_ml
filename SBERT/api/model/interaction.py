"""
GLM Interaction for a User

We Store Interactions inside Elasticsearch

From these Interactions - we can engineer the following Features

User-related Features:
  Age, gender, country from User model.
  Preferred language from UserPreference model.

Post-related Features:
  Age of the post (calculated from the date field in Post model).
  Language of the post from Post model.

Interaction-related Features: 
  Type of interaction from Interaction model.
  Time since last interaction for the given user (from timestamp field in Interaction).

Interactions represent one interaction of a user with a post.

- PostVisit
- PostLike
- PostRevisit

- UserLogin
- UserTimeSpent
- UserLike
- UserRevisit
- UserVisit

Import Questions:

  - Male people's favorite Posts and Languages  
  - People above Age Range favorite Posts and Languages 
  - People's favorite posts
  - Depending on when a Person Logs in - which posts they view
  - User's favorite languages
  

"""
from typing import Optional, List
from pydantic import BaseModel


# Current Goal - Using GLM to get Probability User will View a Post


class UserPostInteraction(BaseModel):
    """
    User Interaction on Post
    """

    user_username: str
    post_id: str
    interaction_type: str  # e.g., "view", "like", "comment", etc.
    timestamp: str  # ISO f


class UserPreference(BaseModel):
    """
    User Interaction on Post
    """

    user_username: str
    preferred_lang: str
    top_langs: List[str]


class BaseInteraction(BaseModel):
    """
    Base Interaction Model
    """

    user_username: str
    timestamp: str  # ISO format datetime string


# Models for interactions with posts
class PostVisit(BaseInteraction):
    """
    Base Interaction Model
    """

    post_id: str


class PostLike(BaseInteraction):
    """
    Base Interaction Model
    """

    post_id: str


class PostRevisit(BaseInteraction):
    """
    Base Interaction Model
    """

    post_id: str


# Models for user-related interactions
class UserLogin(BaseInteraction):
    """
    Base Interaction Model
    """

    pass  # No additional fields needed for this interaction


class UserTimeSpent(BaseInteraction):

    """
    Base Interaction Model
    """

    post_id: Optional[str] = None
    time_spent_seconds: int


class UserLike(BaseInteraction):
    """
    Base Interaction Model
    """

    post_id: str


class UserRevisit(BaseInteraction):
    """
    Base Interaction Model
    """

    post_id: str
