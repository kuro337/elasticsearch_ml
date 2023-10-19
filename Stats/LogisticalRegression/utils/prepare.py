"""
Utils for Model Preparation
"""
from sklearn.model_selection import train_test_split
import pandas as pd

from features.feature_engineering import (
    map_date_difference,
    map_interaction_type,
    one_hot_encode,
)

from utils.models import DateDifferenceFeature, PresenceFeature


def prepare_data(
    merged_df_encoded: pd.DataFrame,
    drop_columns: list,
    target_column: str,
    test_size: float,
    random_state: int,
):
    """
    Prepares the data for modelling
    """
    X = merged_df_encoded.drop(drop_columns, axis=1)
    y = merged_df_encoded[target_column]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def prepare_model_dataframe(config: dict) -> pd.DataFrame:
    """
    Prepare the Full Data Set

    """
    entities = {
        entity["index"]: {"path": entity["path"], "merge_key": entity["merge_key"]}
        for entity in config["entities"]
    }
    mapping = config["mapping"]

    filepaths = {
        **{entity: data["path"] for entity, data in entities.items()},
        **{mapping["index"]: mapping["path"]},
    }
    dfs = {key: pd.read_csv(filepath) for key, filepath in filepaths.items()}

    interaction_key = mapping["index"]
    merged_df = dfs[interaction_key].copy()

    for entity, data in entities.items():
        merged_df = merged_df.merge(dfs[entity], on=data["merge_key"])

    merged_df["interaction_type"] = merged_df["interaction_type"].fillna(
        mapping["default"]
    )

    return merged_df


def perform_feature_engineering(merged_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add Columns to Dataframe Based on Feature Engineering
    """

    # Configs for Feature

    date_feature = DateDifferenceFeature(
        date_col_1="timestamp",
        date_col_2="date",
        difference_col="post_age_days",
    )

    presence_feature = PresenceFeature(
        column="interaction_type",
        new_col="viewed",
        condition="view",
    )

    merged_df = map_date_difference(
        df=merged_df,
        **date_feature.model_dump(),
    )

    # Maps the interaction_type from Dataframe - and sets a new column viewed
    # depending on whether interaction_type is view or not
    merged_df = map_interaction_type(
        df=merged_df,
        **presence_feature.model_dump(),
    )

    # If df has a column Gender M/F - creates a new Column for each Possible Val
    # So adds an M col which is 1/0 denoting if it is Present , Same for F , etc.
    # This will add gender_Male , gender_Female as a 1/0 Col
    merged_df_encoded = one_hot_encode(
        merged_df=merged_df,
        columns_to_encode=["gender", "country", "lang", "author", "interaction_type"],
    )
    return merged_df_encoded


def get_encoded_column_names(original_columns, encoded_df):
    """
    Given a list of original column names and the DataFrame after encoding,
    this function returns a list of the new column names associated
    with the original columns.
    """

    encoded_column_names = []
    for original_column in original_columns:
        encoded_column_names.extend(
            [
                col
                for col in encoded_df.columns
                if col.startswith(original_column + "_") or col == original_column
            ]
        )
    return encoded_column_names
