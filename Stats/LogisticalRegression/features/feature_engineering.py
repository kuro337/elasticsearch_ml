"""
Utils for Feature Engineering
"""

import pandas as pd


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


def one_hot_encode(merged_df: pd.DataFrame, columns_to_encode: list) -> pd.DataFrame:
    """
    One-hot encoding of categorical variables
    """
    return pd.get_dummies(merged_df, columns=columns_to_encode)
