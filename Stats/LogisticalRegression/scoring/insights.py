"""
@Score
Scoring Insights from Model
"""
import pandas as pd
from typing import List, Optional

from LogisticalRegression.utils.models import MapScoringToOriginalData


def map_scores_to_merged_df(
    original_data: pd.DataFrame,
    scored_data: pd.DataFrame,
    scores_map: MapScoringToOriginalData,
) -> pd.DataFrame:
    """
    Map Scores to Merged DataFrame using configurations specified in scores_map
    """

    # Extract configurations from scores_map
    entity_a_name = scores_map.entity_a.entity.__name__.lower()
    entity_b_name = scores_map.entity_b.entity.__name__.lower()
    a_pk = f"{entity_a_name}_{scores_map.entity_a.primary_key}"
    b_pk = f"{entity_b_name}_{scores_map.entity_b.primary_key}"
    score_col = scores_map.score_field

    # Define prefixes for better consistency in merged DataFrame
    entity_a_prefix = f"{entity_a_name}_"
    entity_b_prefix = f"{entity_b_name}_"

    # Aggregate scores by primary keys and calculate mean
    scored_data_agg = scored_data.groupby([a_pk, b_pk], as_index=False).agg(
        {score_col: "mean"}
    )

    # Rename columns for consistency before merging
    scored_data_agg.rename(
        columns={
            # a_pk: f"{entity_a_prefix}{a_pk}",
            # b_pk: f"{entity_b_prefix}{b_pk}",
            a_pk: a_pk,
            b_pk: b_pk,
        },
        inplace=True,
    )

    # Merge the scored dataset back to the original dataset
    merged_df = pd.merge(
        original_data,
        scored_data_agg,
        on=[f"{a_pk}", f"{b_pk}"],
        # on=[f"{entity_a_prefix}{a_pk}", f"{entity_b_prefix}{b_pk}"],
        how="left",
    )

    # Fill NaN scores with 0 after merging
    merged_df[score_col] = merged_df[score_col].fillna(value=0)

    if (
        not scores_map.entity_a.display_fields
        and not scores_map.entity_b.display_fields
    ):
        display_fields = [col for col in original_data.columns] + [score_col]
    else:
        entity_a_display_fields = [
            f"{entity_a_prefix}{field}"
            for field in (scores_map.entity_a.display_fields or [])
        ]
        entity_b_display_fields = [
            f"{entity_b_prefix}{field}"
            for field in (scores_map.entity_b.display_fields or [])
        ]
        display_fields = entity_a_display_fields + entity_b_display_fields + [score_col]

    final_df = merged_df[display_fields]

    print(
        "=====================================\n\nPRINTING SCORES MERGED TO ORIGINAL DF"
    )
    # Print each row with the new scores
    # for index, row in final_df.iterrows():
    # print(row)

    print("=====================================\n\n")

    return final_df
