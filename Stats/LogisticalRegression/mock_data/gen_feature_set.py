"""
Function to Create the Dataset to Obtain Scores for each User-Post 

Leverages existing Trained Models to derive Scores
"""

from typing import List, Optional
import random
from datetime import datetime, timedelta

from model.models import Interaction, ESDocument


def simulate_interactions(
    users: List[ESDocument],
    posts: List[ESDocument],
    random_attribute: Optional[bool] = False,
) -> List[ESDocument]:
    """
    Create Interactions to Predict Scores for Posts being Viewed

    @Usage
    ```py
    # Generate interactions
    interactions = simulate_interactions(users, posts)

    # Now, you can send these interactions through your pipeline
    # Predict scores using your existing trained model.
    ```
    """
    interactions: List[ESDocument] = []

    # Get the current time and add one hour
    current_time_plus_one_hour = datetime.now() + timedelta(hours=1)

    for user in users:
        for post in posts:
            interaction = Interaction(
                interaction_type="view",
                post_id=post.post_id,
                timestamp=current_time_plus_one_hour.isoformat(),
                username=user.username,
            )
            interactions.append(interaction)

            # Optional: create a "like" interaction based on some condition or probability
            if random_attribute:
                if random.choice([True, False]):  # 50% chance to "like" the post
                    like_interaction = Interaction(
                        interaction_type="like",
                        post_id=post.post_id,
                        timestamp=current_time_plus_one_hour.isoformat(),
                        username=user.username,
                    )
                    interactions.append(like_interaction)

    return interactions
