"""
Saving and Loading the Model after Training
"""
from joblib import dump, load
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression


def save_model(model: LogisticRegression, model_filename: str) -> None:
    """
    Save the model to a file

    @Usage

    ```py
    # Save model to a file
    save_model(lr_c, "logistic_regression_model.joblib")
    ```
    """
    dump(model, model_filename)


def load_model(model_filename: str) -> LogisticRegression:
    """
    Load the model from a file
    ```py
    # Load model from the file
    loaded_model = load(model_filename)

    # Use loaded model to make predictions
    predicted_probabilities = loaded_model.predict_proba(features_for_scoring)
    ```
    """
    return load(model_filename)


def print_model_coefficients(
    lr: LogisticRegression,
    trainingset: pd.DataFrame,
) -> None:
    """
    Print the sorted coefficients and the intercept
    """

    # Map Coefficients and Feature Names to Training Set
    coef_df = pd.DataFrame(
        {"Feature": trainingset.columns.drop("viewed"), "Coefficient": lr.coef_[0]}
    ).sort_values(by="Coefficient", ascending=False)

    # Get Odds
    coef_df = coef_df.assign(Odds_ratio=np.exp(coef_df.get("Coefficient")))

    print("\nCoefficients and Odds Ratios (sorted by value):")
    print(coef_df.to_string(index=False))

    # Print Sorted Coefficients and the Intercept
    print("\nCoefficients (sorted by value):")
    print(coef_df.to_string(index=False))
    print(f"\nIntercept: {lr.intercept_[0]}")
