import pytest
import pandas as pd
import numpy as np

# Sample DataFrame as a fixture
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'feature': [1, 2, 3, 4],
        'target': [2, 4, 6, 8]
    })

@pytest.fixture
def sample_train_data():
    X = np.array([[1], [2], [3], [4]])
    y = np.array([2, 4, 6, 8])
    return X, y

@pytest.fixture
def sample_test_data():
    X_test = np.array([[5], [6]])
    y_test = np.array([10, 12])
    return X_test, y_test

@pytest.fixture
def edge_case_data():
    empty_data = (np.array([]), np.array([]))
    mismatched_data = (np.array([[1], [2], [3]]), np.array([2, 4]))
    nan_data = (np.array([[1], [2], [np.nan]]), np.array([2, 4, 6]))
    return empty_data, mismatched_data, nan_data
