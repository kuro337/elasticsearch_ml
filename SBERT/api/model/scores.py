"""
Scores
"""


from typing import List, Dict
from pydantic import StringConstraints, HttpUrl
from typing_extensions import Annotated

from model.interface import ESInterface


class UserPostScore(ESInterface):
    """
    User-Post Interaction
    """

    interaction_type: Annotated[str, StringConstraints(min_length=1)]
    post_id: Annotated[str, StringConstraints(min_length=1)]
    timestamp: Annotated[str, StringConstraints(min_length=8)]
    username: Annotated[str, StringConstraints(min_length=1)]

    def get_index_name(self) -> str:
        return "user_post_scores"

    def get_mapping(self) -> Dict:
        return {
            "properties": {
                "username": {"type": "text"},
                "post_id": {"type": "text"},
                "score": {"type": "float"},
                "timestamp": {"type": "date"},
            }
        }
