import pandas as pd
import mlflow
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import  StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from ray.util.joblib import register_ray
import joblib

data = pd.read_csv('https://lead-program-assets.s3.eu-west-3.amazonaws.com/M01-Distributed_machine_learning/datasets/creditcard.csv')

EXPERIMENT_NAME="mlflow-ray-kubernetes-deploy"

mlflow.set_tracking_uri("http://192.168.49.2:30693")

mlflow.set_experiment(EXPERIMENT_NAME)

experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

mlflow.sklearn.autolog()

X = data.drop("Class", axis=1)
y = data["Class"]

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

model = Pipeline(steps=[
        ("standard_scaler", StandardScaler()),
        ("classifier", RandomForestClassifier())
    ], verbose=True)

param_grid = {
    'classifier__max_depth': [3,5],
    'classifier__min_samples_split': [5,10],
}

grid_search = GridSearchCV(model, param_grid=param_grid, n_jobs=-1, cv=2, verbose=2, refit=True)

with mlflow.start_run(experiment_id = experiment.experiment_id):
    register_ray() 
    with joblib.parallel_backend('ray'):
        grid_search.fit(X_train, y_train)
        print(grid_search.score(X_train, y_train))