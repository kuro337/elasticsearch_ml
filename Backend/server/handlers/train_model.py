"""
@WebSocket
@TrainModel

Train the Model and Retrieve Scores based on General Linear Model
"""
from typing import List
from fastapi import WebSocket
from elastic_search.es_service import ElasticSearchService
from LogisticalRegression.demo import train_model_get_scores
from app import query_posts_for_user
from model.models import UserPostScore
from LogisticalRegression.demo import train_model_get_scores
from exceptions.server_exceptions import GLMModelTrainingFailure


async def train_model(client: ElasticSearchService, websocket: WebSocket):
    """
    @WebSockets
    @GET /userTopPosts

    - Sends a User Object - server retrieves Posts with Highest Scores

    Train the model and get scores
    """
    try:
        trained_model_scores: List[UserPostScore] = train_model_get_scores()
    except Exception as e:
        raise GLMModelTrainingFailure(e)

    for score in trained_model_scores:
        print(f"Score: {score.score}\n")
