import pandas as pd
import torch
from sklearn.model_selection import train_test_split

def load_data(path):
    data = pd.read_csv(path)
    return data

def preprocess_data(data):
    # Basic preprocessing: fill missing values and convert to tensor
    data = data.fillna(0)
    user_item_matrix = data.pivot(index='user_id', columns='item_id', values='rating').fillna(0)
    return torch.tensor(user_item_matrix.values, dtype=torch.float32)

def split_data(user_item_matrix, test_size=0.2):
    train_data, test_data = train_test_split(user_item_matrix, test_size=test_size)
    return train_data.clone().detach().float(), test_data.clone().detach().float()
