import pandas as pd
import torch
from app.data_preprocessing import load_data, preprocess_data

def test_load_data():
    data = load_data('./data/user_item_ratings.csv')
    assert not data.empty

def test_preprocess_data():
    data = pd.DataFrame({
        'user_id': [0, 1, 2],
        'item_id': [0, 1, 2],
        'rating': [4, 5, 3]
    })
    user_item_matrix = preprocess_data(data)
    assert user_item_matrix.shape == (3, 3)
    assert torch.is_tensor(user_item_matrix)
