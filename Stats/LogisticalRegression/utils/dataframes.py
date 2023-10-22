"""
Utils for Pandas DataFrames
"""
import pandas as pd


def compare_dataframe_columns(
    df1: pd.DataFrame, df2: pd.DataFrame, df1_name="DataFrame 1", df2_name="DataFrame 2"
):
    """
    Compares columns of two pandas DataFrames and prints the differences.

    :param df1: First DataFrame
    :param df2: Second DataFrame
    :param df1_name: Custom name for the first DataFrame for printing, default is 'DataFrame 1'
    :param df2_name: Custom name for the second DataFrame for printing, default is 'DataFrame 2'

    @Usage
    ```py

    compare_dataframe_columns(training_df, scoring_df, 'Training Data', 'Scoring Data')

    ```
    """

    print("\n------------------- Column Matching Verification -------------------\n")

    print(f"Columns in {df1_name}:")
    df1_columns = df1.columns
    print(df1_columns)

    print(f"\nColumns in {df2_name}:")
    df2_columns = df2.columns
    print(df2_columns)

    # Check if both have the same set of columns
    if set(df1_columns) == set(df2_columns):
        print("\nColumns match: Yes")
    else:
        print("\nColumns match: No")
        # If there's a mismatch, display the differing columns for debugging
        missing_in_df2 = set(df1_columns) - set(df2_columns)
        missing_in_df1 = set(df2_columns) - set(df1_columns)
        print(
            f"\nColumns present in {df1_name} but missing in {df2_name}:",
            missing_in_df2,
        )
        print(
            f"\nColumns present in {df2_name} but missing in {df1_name}:",
            missing_in_df1,
        )

    print("\n--------------------------------------------------------------------\n")
