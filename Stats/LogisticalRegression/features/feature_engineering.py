"""
Utils for Feature Engineering
"""

import pandas as pd
from LogisticalRegression.utils.models import (
    DateDifferenceFeature,
    InteractionTypeConfig,
    CategoricalVariableConfig,
)


def apply_date_difference_feature(
    df: pd.DataFrame, feature_config: DateDifferenceFeature
) -> pd.DataFrame:
    """
    Applies the date difference feature engineering to the DataFrame based on the provided configuration.

    Parameters:
    - df (pd.DataFrame): The DataFrame to operate on.
    - feature_config (DateDifferenceFeatureConfig): The configuration specifying the entities and columns.

    Returns:
    - pd.DataFrame: The DataFrame with the new date difference column added.
    """
    # Apply the map_date_difference_with_config function with the provided DataFrame and configuration
    df_with_date_difference = map_date_difference_with_config(df, feature_config)

    return df_with_date_difference


def map_date_difference_with_config(
    df: pd.DataFrame, feature_config: DateDifferenceFeature
) -> pd.DataFrame:
    """
    Calculate the difference in days between two date columns based on the provided feature configuration
    and add the result to the DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame to operate on.
    - feature_config (DateDifferenceFeatureConfig): The configuration specifying the entities and columns.

    Returns:
    - pd.DataFrame: The DataFrame with the new difference column added.
    """
    # Determine the column names.
    start_col_prefix = (
        feature_config.start_entity
        if isinstance(feature_config.start_entity, str)
        else feature_config.start_entity.__name__.lower()
    )
    end_col_prefix = (
        feature_config.end_entity
        if isinstance(feature_config.end_entity, str)
        else feature_config.end_entity.__name__.lower()
    )

    start_col = f"{start_col_prefix}_{feature_config.start_time_col}"
    end_col = f"{end_col_prefix}_{feature_config.end_time_col}"

    # Convert columns to datetime, this will keep NaT where dates are not parseable
    datetime_1 = pd.to_datetime(df[start_col], errors="coerce")
    datetime_2 = pd.to_datetime(df[end_col], errors="coerce")

    # Calculate the difference, this will result in NaT where either date is NaT
    date_difference = (datetime_2 - datetime_1).dt.days

    # Replace NaT and NaN with 0 in the date difference calculation
    date_difference = date_difference.fillna(0).astype(int)

    # Assign the new column using the assign method as was done originally
    df = df.assign(**{feature_config.new_col: date_difference})

    return df


def map_date_difference(
    df: pd.DataFrame, date_col_1: str, date_col_2: str, difference_col: str
) -> pd.DataFrame:
    """
    Calculate the difference in days between two date columns and add it to the DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame to operate on.
    - date_col_1 (str): The name of the first date column.
    - date_col_2 (str): The name of the second date column.
    - difference_col (str): The name of the new column where the date difference will be stored.

    Returns:
    - pd.DataFrame: The DataFrame with the new difference column added.
    """
    datetime_1 = pd.to_datetime(df[date_col_1])
    datetime_2 = pd.to_datetime(df[date_col_2])
    date_difference = (datetime_1 - datetime_2).dt.days
    return df.assign(**{difference_col: date_difference})


def map_interaction_type(
    df: pd.DataFrame, column: str, new_col: str, condition: str
) -> pd.DataFrame:
    """
    Requires the interaction type to be mapped to a binary variable

    Is Reusable - just need to pass in the column names

    Map the interaction type to a binary variable Viewed
    """
    df[new_col] = df[column].apply(lambda x: 1 if x == condition else 0)
    return df


def map_interaction_type_config(
    df: pd.DataFrame, config: InteractionTypeConfig
) -> pd.DataFrame:
    """
    Map a column value to a binary representation based on a condition.
    """
    prefix = (
        config.entity
        if isinstance(config.entity, str)
        else config.entity.__name__.lower()
    )

    df[config.new_col] = df[f"{prefix}_{config.column}"].apply(
        lambda x: 1 if x == config.condition else 0
    )
    return df


# def one_hot_encode_config(
#     merged_df: pd.DataFrame, config: CategoricalVariableConfig
# ) -> pd.DataFrame:
#     """
#     One-hot encoding of categorical variables specified in the config.

#     - One Hot Encoding is useful to convert Variables with no Ordinal Relationship - such as Colors or Countries.
#     - Used so ML Models can understand them as they require Numeric Inputs

#     """
#     # Prepare the full column names
#     columns_to_encode = []
#     for entity_config in [config.entity_a, config.entity_b, config.interaction]:
#         prefix = entity_config.entity.__name__.lower()
#         columns_to_encode.extend([f"{prefix}_{col}" for col in entity_config.columns])

#     return pd.get_dummies(merged_df, columns=columns_to_encode)


def one_hot_encode_config(
    merged_df: pd.DataFrame, config: CategoricalVariableConfig
) -> pd.DataFrame:
    """
    One-hot encoding of categorical variables specified in the config, while retaining specified columns.
    """
    columns_to_encode = []
    columns_to_retain = []  # These are your primary keys or columns you want to retain

    # Prepare the full column names
    for entity_config in [config.entity_a, config.entity_b, config.interaction]:
        prefix = entity_config.entity.__name__.lower()
        columns = [f"{prefix}_{col}" for col in entity_config.columns]
        columns_to_encode.extend(columns)

        # Check if there's a primary_key attribute in your entity_config
        if hasattr(entity_config, "primary_key") and entity_config.primary_key:
            primary_key = f"{prefix}_{entity_config.primary_key}"  # prepare the full primary_key name
            columns_to_retain.append(primary_key)
            # Safely remove primary key from the encoding list if it exists
            if primary_key in columns_to_encode:
                columns_to_encode.remove(primary_key)

    print("Columns to encode:", columns_to_encode)
    print("Columns to retain:", columns_to_retain)

    # Keep a copy of the columns to retain
    retained_df = merged_df[columns_to_retain].copy()

    # Temporarily remove the columns to retain from the DataFrame before one-hot encoding
    merged_df_temp = merged_df.drop(columns=columns_to_retain)

    # Perform one-hot encoding
    merged_df_encoded = pd.get_dummies(merged_df_temp, columns=columns_to_encode)

    # Concatenate the retained columns back to the one-hot encoded DataFrame
    result_df = pd.concat([merged_df_encoded, retained_df], axis=1)

    return result_df


def one_hot_encode(merged_df: pd.DataFrame, columns_to_encode: list) -> pd.DataFrame:
    """
    One-hot encoding of categorical variables
    """
    return pd.get_dummies(merged_df, columns=columns_to_encode)
