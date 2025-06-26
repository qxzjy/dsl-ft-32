from ray.job_submission import JobSubmissionClient
from dotenv import load_dotenv
import os

load_dotenv()

client = JobSubmissionClient("127.0.0.1:8265")
job_id = client.submit_job(
    entrypoint="python ray_train.py",
    runtime_env={
        "working_dir": "./",
        "pip": ["numpy", "joblib", "scikit-learn", "tune-sklearn", "mlflow"],
        "env_vars": {
            "MLFLOW_TRACKING_URI": os.getenv("MLFLOW_TRACKING_URI"),
            "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
            "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "ARTIFACT_STORE_URI": os.getenv("ARTIFACT_STORE_URI"),
            "BACKEND_STORE_URI": os.getenv("BACKEND_STORE_URI")
        }
    }
)
