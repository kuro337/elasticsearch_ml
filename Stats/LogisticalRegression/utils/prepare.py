"""
Utils for Model Preparation
"""


from typing import List, Tuple
from sklearn.model_selection import train_test_split
import pandas as pd

from utils.models import DocumentGLMConfig


from model.models import Interaction, User, Post, Product, ESDocument

from features.feature_engineering import (
    map_date_difference,
    map_interaction_type,
    one_hot_encode,
)

from utils.models import DateDifferenceFeature, PresenceFeature, RelevancyConfig


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


def prepare_dataframe_from_documents(
    entity_a: DocumentGLMConfig,
    entity_b: DocumentGLMConfig,
    entity_mapping: DocumentGLMConfig,
) -> pd.DataFrame:
    """
    Prepare the DataFrame from a list of ESDocument instances.

    @param entity_a: Configuration for Entity A including document list and merge key.
    @param entity_b: Configuration for Entity B including document list and merge key.
    @param entity_mapping: Configuration for interaction data including document list, variance key, and default value.
    @return: A merged DataFrame prepared from the list of ESDocument instances.
    """

    # Rename DataFrame columns based on the class name
    entity_a_df = rename_cols_based_on_classname(entity_a)
    entity_b_df = rename_cols_based_on_classname(entity_b)
    interaction_df = rename_cols_based_on_classname(entity_mapping)

    print(entity_a_df.columns)
    print(entity_b_df.columns)
    print(interaction_df.columns)

    # Identify the variance column
    variance_column = entity_mapping.variance_key

    # Get the class name from the first object in the list and convert to lowercase for use in merge
    entity_a_classname = entity_a.doc_list[0].__class__.__name__.lower()
    entity_b_classname = entity_b.doc_list[0].__class__.__name__.lower()
    interaction_classname = entity_mapping.doc_list[0].__class__.__name__.lower()

    # Merge the entity DataFrames into the interaction DataFrame using the class name and merge key
    merged_df = interaction_df.merge(
        entity_a_df,
        left_on=f"interaction_{entity_a.merge_key}",  # prepend 'interaction_' to construct the correct column name
        right_on=f"{entity_a_classname}_{entity_a.merge_key}",
        how="left",
    )
    merged_df = merged_df.merge(
        entity_b_df,
        left_on=f"interaction_{entity_b.merge_key}",  # prepend 'interaction_' to construct the correct column name
        right_on=f"{entity_b_classname}_{entity_b.merge_key}",
        how="left",
    )

    if variance_column:
        # Construct the correct column name post-renaming
        renamed_variance_column = f"{interaction_classname}_{variance_column}"
        # Use the correct column name when accessing the DataFrame
        merged_df[renamed_variance_column] = merged_df[renamed_variance_column].fillna(
            entity_mapping.default_value
        )

    return merged_df


def prepare_model_dataframe(config: dict) -> pd.DataFrame:
    """
    Prepare the Full Data Set

    """
    print(config["mapping"])

    variance_column = config["mapping"]["variance_field"]

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

    # merged_df["interaction_type"] = merged_df["interaction_type"].fillna(
    #     mapping["default"]
    # )

    merged_df[variance_column] = merged_df[variance_column].fillna(mapping["default"])

    return merged_df


def perform_feature_engineering(
    merged_df: pd.DataFrame, features: DateDifferenceFeature = None
) -> pd.DataFrame:
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
    # Works for any n number of Options such as Country Too
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


def drop_irrelevant_columns_config(
    relevant_config: RelevancyConfig, encoded_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Modify the DataFrame to drop the irrelevant columns based on the RelevancyConfig,
    dynamically matching the entity lowercased class names with the column names.
    """

    # Extract all columns from the DataFrame
    all_columns = set(encoded_df.columns)

    # Initialize the set of relevant columns
    relevant_columns = set()

    # Add the target column to the set of relevant columns to ensure it's not dropped
    if relevant_config.target:
        relevant_columns.add(relevant_config.target)

    for feature in relevant_config.features:
        relevant_columns.add(feature)

    # Helper function to match the prefixed column names
    def match_prefixed_columns(entity_columns, entity_name):
        # Look for columns that contain both the entity prefix and the column name
        # If col passed is username - user_username_SomeName will be dropped
        # But exact matches not dropped - such as user_username
        return {
            col
            for col in all_columns
            for entity_col in entity_columns
            if f"{entity_name.lower()}_{entity_col}_" in col
        }

    # Add the relevant entity columns by matching prefixes
    for entity_config in [
        relevant_config.entity_a,
        relevant_config.entity_b,
        relevant_config.interaction,
    ]:
        if entity_config:
            entity_name = entity_config.entity.__name__
            entity_columns = entity_config.columns
            matched_columns = match_prefixed_columns(entity_columns, entity_name)
            relevant_columns.update(matched_columns)

    # Determine the columns to drop
    columns_to_drop = all_columns - relevant_columns

    # Drop the irrelevant columns and retain the DataFrame's flexibility
    encoded_df.drop(columns=list(columns_to_drop), inplace=True)

    return encoded_df


def prepare_data_for_training_and_scoring(
    relevant_config: RelevancyConfig,
    encoded_df: pd.DataFrame,
    identifier_columns: list = None,
) -> pd.DataFrame:
    """
    Modify the DataFrame to drop the irrelevant columns based on the RelevancyConfig,
    dynamically matching the entity lowercased class names with the column names.
    """

    # Make a copy of the original DataFrame for scoring
    # This copy retains all original columns, including identifiers
    scoring_df = encoded_df.copy()

    # Extract all columns from the DataFrame
    all_columns = set(encoded_df.columns)

    # Initialize the set of relevant columns
    relevant_columns = set()

    # Add the target column to the set of relevant columns to ensure it's not dropped
    if relevant_config.target:
        relevant_columns.add(relevant_config.target)

    # Helper function to match the prefixed column names
    def match_prefixed_columns(entity_columns, entity_name):
        # Look for columns that contain both the entity prefix and the column name
        # If col passed is username - user_username_SomeName will be dropped
        # But exact matches not dropped - such as user_username
        return {
            col
            for col in all_columns
            for entity_col in entity_columns
            if f"{entity_name.lower()}_{entity_col}_" in col
        }

    # Add the relevant entity columns by matching prefixes
    for entity_config in [
        relevant_config.entity_a,
        relevant_config.entity_b,
        relevant_config.interaction,
    ]:
        if entity_config:
            entity_name = entity_config.entity.__name__
            entity_columns = entity_config.columns
            matched_columns = match_prefixed_columns(entity_columns, entity_name)
            relevant_columns.update(matched_columns)

    columns_to_drop = all_columns - relevant_columns

    # Drop the irrelevant columns from the training DataFrame
    encoded_df.drop(columns=list(columns_to_drop), inplace=True)
    training_df = encoded_df

    # If there are identifier columns specified, make sure they're in the scoring DataFrame
    if identifier_columns:
        missing_identifiers = set(identifier_columns) - all_columns
        if missing_identifiers:
            raise ValueError(
                f"Identifier columns {missing_identifiers} are not present in the DataFrame"
            )
        # The scoring DataFrame already contains identifier columns, so no need to add them.

    return training_df, scoring_df


def rename_cols_based_on_classname(entity: DocumentGLMConfig) -> pd.DataFrame:
    """
    Rename the columns of the dataframes derived from the lists,
    using the class name of the objects in the list as the prefix.

    @Logic:
    This function is required for Feature Engineering in Case of Common Column Issues

    For example - if we want to Merge User , Post , and User-Post Interaction Documents -
    User and Post could all share a field timestamp

    When we perform DataFrame Merging - common columns are prefixed with _x and _y ..._n

    We use this function so that if timestamp is commong between user , post , and interaction -

    The Column gets renamed to
    user_timestamp
    post_timestamp
    interaction_timestamp

    """

    # Convert list of ESDocument instances to DataFrame
    df = pd.DataFrame([doc.dump_document() for doc in entity.doc_list])

    # Get the class name from the first object in the list and convert to lowercase
    prefix = entity.doc_list[0].__class__.__name__.lower() + "_"

    # Rename columns with class name as prefix
    df = df.rename(columns={col: prefix + col for col in df.columns})

    return df
