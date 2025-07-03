from sklearn.metrics import mean_squared_error
from app.model import load_model

def evaluate_model(model_file, X_test, y_test):
    model = load_model(model_file)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    return mse

