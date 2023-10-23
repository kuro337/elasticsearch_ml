"""
Saving and Loading the Model after Training
"""
from joblib import dump, load

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
