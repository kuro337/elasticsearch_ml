"""
Score Model
"""
from typing import List, Optional
from numpy import ndarray
import pandas as pd

from sklearn.linear_model import LogisticRegression
from LogisticalRegression.utils.models import (
    ScoringConfig,
    MapScoringToOriginalData,
    EntityScoringConfig,
)
from LogisticalRegression.utils.prepare import add_columns_to_dataframe
from LogisticalRegression.scoring.insights import map_scores_to_merged_df
from model.models import User, UserPostScore


def score_data(
    transformed_data: pd.DataFrame,
    model: LogisticRegression,
) -> ndarray:
    """
    Score the Data with the Model
    """
    features_for_scoring = transformed_data.drop(columns=["viewed"])
    print("Scoring Model")
    predicted_probabilities = model.predict_proba(features_for_scoring)

    return predicted_probabilities


def map_scores_to_data(
    original_data: pd.DataFrame,
    transformed_data: pd.DataFrame,
    retained_dfs: dict,
    model_scores: ndarray,
    state: ScoringConfig,
    score_field: str = "score",
) -> pd.DataFrame:
    """
    Score the Data with the Model
    """
    # Drop Target var (viewed) and add scores to Data
    transformed_data = transformed_data.drop(columns=[state.target_variable])
    transformed_data["score"] = model_scores

    transformed_data = add_columns_to_dataframe(
        transformed_data,
        retained_dfs,
    )

    # Print Number of Entries in Original Data and Transformed Data with Scores
    print(f"NUMBER of rows in original_data: {len(original_data)}")
    print(f"NUMBER of rows in mapped_data_with_scores: {len(transformed_data)}")

    print("username" in transformed_data.columns)

    # Create Mapping Config from Model State Config
    mapping_scores_config = MapScoringToOriginalData(
        entity_a=EntityScoringConfig(
            entity=state.entity_a.entity,
            primary_key=state.entity_a.primary_key,
        ),
        entity_b=EntityScoringConfig(
            entity=state.entity_b.entity,
            primary_key=state.entity_b.primary_key,
        ),
        score_field=score_field,
    )

    mapped_data_with_scores = map_scores_to_merged_df(
        original_data,
        transformed_data,
        scores_map=mapping_scores_config,
    )
    return mapped_data_with_scores


def get_scores(
    data_with_scores: pd.DataFrame, state: ScoringConfig
) -> List[UserPostScore]:
    """
    @Score
    Scoring Insights from Model

    """

    entity_a_pk = (
        state.entity_a.entity.__name__.lower() + "_" + state.entity_a.primary_key
    )
    entity_b_pk = (
        state.entity_b.entity.__name__.lower() + "_" + state.entity_b.primary_key
    )

    if state.debug:
        print("\nDebug: Columns in features_for_scoring\n", data_with_scores.columns)
        print("\nDebug: Top 5 rows in features_for_scoring\n")
        print(data_with_scores.head())

    # Getting User Scores for Each Post
    user_post_scores = (
        data_with_scores.groupby([entity_a_pk, entity_b_pk])["score"]
        .mean()
        .reset_index()
    )

    # @ES -> UserPostScores
    scores_es: List[UserPostScore] = []
    # @ElasticSearch
    # > Insert Scores for Entities into ElasticSearch
    for _, row in user_post_scores.iterrows():
        user_post_score = UserPostScore(
            username=row[entity_a_pk],
            post_id=row[entity_b_pk],
            score=row["score"],
        )
        scores_es.append(user_post_score)
        if state.debug:
            print(f"\nUser-Post Score:\n{user_post_score.dump_document()}")

    # User-Post Matrix
    user_post_score_matrix = user_post_scores.pivot(
        index=entity_b_pk, columns=entity_a_pk, values="score"
    )

    # Fill NaN values
    user_post_score_matrix = user_post_score_matrix.fillna(0)

    print("\nUser-Post Score Matrix\n")

    # Printing Scores for Specific User
    single_user_scores = data_with_scores[
        data_with_scores[entity_a_pk] == "Fiero Martin"
    ][[entity_b_pk, "score"]]

    if state.debug:
        print("\nFiero Martin's Scores\n")
        print(single_user_scores)
        print("\nFiero Martin's end\n")

    # List Posts by Average Score
    average_scores = data_with_scores.groupby(entity_b_pk)["score"].mean().reset_index()
    sorted_posts = average_scores.sort_values(by="score", ascending=False)

    if state.debug:
        print("\nSorted Posts by Scores\n")
        print(sorted_posts)

    # For top 10 posts
    top_10_posts = sorted_posts.head(10)

    if state.debug:
        print("\nTop 10 Posts\n")
        print(top_10_posts)

    print(
        "EsDoc Scoring Done\n--------------------------------------------------------\n"
    )

    return scores_es
