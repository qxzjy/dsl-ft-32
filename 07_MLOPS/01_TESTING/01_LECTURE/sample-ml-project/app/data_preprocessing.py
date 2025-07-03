import pandas as pd
from sklearn.model_selection import train_test_split

def load_data(file_path):
    return pd.read_csv(file_path)

def clean_data(df):
    df = df.dropna()
    df['feature'] = df['feature'].astype(float)
    return df

def feature_engineering(df):
    df['feature_squared'] = df['feature'] ** 2
    return df

def split_data(df, target_column, test_size=0.2):
    X = df.drop(columns=[target_column])
    y = df[target_column]
    return train_test_split(X, y, test_size=test_size, random_state=42)

