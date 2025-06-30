import logging
import os
from datetime import datetime

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator

ENDPOINT = "https://www.data.gouv.fr/fr/datasets/r/5c4e1452-3850-4b59-b11c-3dd51d7fb8b5"
DATA_FOLDER = "./data"

# We can define some default arguments for all tasks
default_args = {
    "owner": "airflow",
    "schedule_interval": "@daily",
    "start_date": datetime(2022, 6, 12),
}


def _fetch_covid_datas(ti):
    """Downloads the COVID-19 data from the endpoint and saves it as a CSV file."""
    logging.info("Fetching COVID data")
    # Download the CSV file
    df = pd.read_csv(ENDPOINT)
    # Create a filename based on the date
    target_filename =os.path.join(DATA_FOLDER, f"raw-datas-{datetime.now().strftime('%Y-%m-%d')}.csv")
    # Dump the dataframe to a CSV file
    df.to_csv(target_filename, index=False)
    # Push filename to XCom
    ti.xcom_push("target_filename", target_filename)
    logging.info("Saved COVID data to %s", target_filename)


def _transform_covid_datas(ti):
    logging.info("Transforming COVID data")
    # Get the filename from XCom
    filename = ti.xcom_pull(task_ids="fetch_covid_datas", key="target_filename")
    logging.info("target_filename: %s", filename)
    # Load CSV
    df = pd.read_csv(filename)
    # Compute the mean of new hospitalized cases per day (column "incid_hosp")
    mean = df.groupby("date")["incid_hosp"].mean()
    # Create a filename based on the date
    mean_target_filename =os.path.join(DATA_FOLDER, f"mean-incid_hosp-{datetime.now().strftime('%Y-%m-%d')}.csv")
    # Dump the dataframe to a CSV file
    mean.to_csv(mean_target_filename)
    # Push the mean to XCom
    ti.xcom_push("mean_target_filename", mean_target_filename)
    logging.info("Computed mean of new hospitalized cases per day and saved to %s", mean_target_filename)


with DAG("covid_dag", catchup=False, default_args=default_args) as dag:

    # This task fetches the data from the endpoint
    fetch_covid_datas = PythonOperator(task_id="fetch_covid_datas", python_callable=_fetch_covid_datas)

    # This task transforms the data
    transform_covid_datas = PythonOperator(task_id="transform_covid_datas", python_callable=_transform_covid_datas)

    fetch_covid_datas >> transform_covid_datas
