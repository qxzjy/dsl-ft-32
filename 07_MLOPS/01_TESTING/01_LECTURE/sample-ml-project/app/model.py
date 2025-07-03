from sklearn.linear_model import LinearRegression
import joblib
import numpy as np

class Model:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def save(self, file_path):
        save_model(self.model, file_path)

    def load(self, file_path):
        self.model = load_model(file_path)


def create_model():
    return Model()

def save_model(model, file_path):
    joblib.dump(model, file_path)

def load_model(file_path):
    return joblib.load(file_path)

def custom_loss_function(y_true, y_pred):
    return sum(np.subtract(y_true, y_pred) ** 2) / len(y_true)
