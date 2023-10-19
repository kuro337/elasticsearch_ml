"""
Loads CSV Data
"""

import pandas as pd


def load_and_merge_data(filepaths: dict, merge_keys: dict) -> pd.DataFrame:
    """
    Feature Engineering Task
    User Engagement with posts.


    @param user_filepath: filepath to the user csv
    @param post_filepath: filepath to the post csv
    @param interaction_filepath: filepath to the interaction csv

    @return: merged_df:

    ```python
    # Provide Entity 1 and Entity 2 and Interaction Data
    # Interaction should have a common key for Entity 1 and Entity 2

    filepaths = {
    "users": "dataset/csv/users.csv",
    "posts": "dataset/csv/posts.csv",
    "interactions": "dataset/csv/interactions.csv",
    }

    # Provide the keys to merge the data on - Interaction has username and post_id

    merge_keys = {"user": "username", "post": "post_id"}

    # The pd.DataFrame is returned after performing the merge

    merged_df = load_and_merge_data(filepaths, merge_keys)
    ```

    Loads the csv's and Merges the User and Post Data with the Interaction Data
    It uses username and post_id as the keys to merge the data

    """
    dfs = {key: pd.read_csv(filepath) for key, filepath in filepaths.items()}
    merged_df = (
        dfs["interactions"]
        .merge(dfs["users"], on=merge_keys["user"])
        .merge(dfs["posts"], on=merge_keys["post"])
    )
    return merged_df
