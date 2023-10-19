"""
Accepts the Merged_df with Feature Engineering (extra Cols) Added

Just pass it the name of the target Variable (viewed) that we add 
"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd


def train_and_evaluate(
    dataframe: pd.DataFrame, target_column: str, test_size=0.2, random_state=42
):
    """
    Train a logistic regression model and evaluate its performance.

    Parameters:
    - dataframe (pd.DataFrame): The preprocessed dataset.
    - target_column (str): The name of the target column.
    - test_size (float): The proportion of the dataset to include in the test split.
    - random_state (int): Seed used by the random number generator.

    Returns:
    - lr (LogisticRegression): The trained logistic regression model.
    - metrics (dict): A dictionary of evaluation metrics.
    """

    # Split the data into training and testing sets
    X = dataframe.drop(columns=[target_column])
    y = dataframe[target_column]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Train the logistic regression model
    lr = LogisticRegression(max_iter=1000, random_state=random_state)
    lr.fit(X_train, y_train)

    # Evaluate the model
    y_pred = lr.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
    }

    return lr, metrics
