import pytest
import numpy as np
from app.model import custom_loss_function
from app.model import Model

@pytest.mark.parametrize(
    "y_true, y_pred, expected_loss",
    [
        ([1, 2, 3], [1, 2, 3], 0),  # Perfect prediction
        ([1, 2, 3], [2, 3, 4], 1),  # Simple case
        ([1, 2, 3], [3, 2, 1], pytest.approx(2.65, rel=1e-2)),  # Another case
    ]
)
def test_custom_loss_function(y_true, y_pred, expected_loss):
    assert custom_loss_function(y_true, y_pred) == expected_loss


@pytest.mark.parametrize(
    "X, y, expected_exception",
    [
        (np.array([]), np.array([]), ValueError),  # Empty data
        (np.array([[1], [2], [3]]), np.array([2, 4]), ValueError),  # Mismatched dimensions
        (np.array([[1], [2], [np.nan]]), np.array([2, 4, 6]), ValueError),  # NaN values
    ]
)
def test_model_training_edge_cases(X, y, expected_exception):
    model = Model()
    with pytest.raises(expected_exception):
        model.train(X, y)

@pytest.mark.slow
def test_model_training_slow(sample_train_data):
    model = Model()
    X, y = sample_train_data
    model.train(X, y)
    predictions = model.predict(X)
    assert predictions.tolist() == y.tolist()

@pytest.mark.fast
def test_model_creation_fast():
    model = Model()
    assert model.model is not None

def test_model_creation():
    model = Model()
    assert model.model is not None  # Ensure model instance is created

def test_model_training(sample_train_data):
    model = Model()
    X, y = sample_train_data
    model.train(X, y)
    predictions = model.predict(X)
    assert predictions.tolist() == y.tolist()  # Check if predictions match the target