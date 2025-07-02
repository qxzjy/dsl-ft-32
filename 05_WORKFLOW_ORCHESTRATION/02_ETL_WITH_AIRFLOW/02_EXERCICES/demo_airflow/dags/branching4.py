from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime

default_args = {
    "owner": "airflow",
    "start_date": datetime(2022, 6, 1),
}

with DAG(
    dag_id="dummy_branching_etl",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description="DAG dummy simulant deux branches ETL parallèles",
) as dag:

    start = DummyOperator(task_id="start")

    with TaskGroup(group_id="status_branch") as status_branch:
        fetch_status_data = DummyOperator(task_id="fetch_status_data")
        transform_status_data = DummyOperator(task_id="transform_status_data")
        create_status_table = DummyOperator(task_id="create_status_table")
        transfer_status_data_to_postgres = DummyOperator(
            task_id="transfer_status_data_to_postgres"
        )

        (
            fetch_status_data
            >> transform_status_data
            >> create_status_table
            >> transfer_status_data_to_postgres
        )

    with TaskGroup(group_id="weather_branch") as weather_branch:
        fetch_weather_data = DummyOperator(task_id="fetch_weather_data")
        transform_weather_data = DummyOperator(task_id="transform_weather_data")
        create_weather_table = DummyOperator(task_id="create_weather_table")
        transfer_weather_data_to_postgres = DummyOperator(
            task_id="transfer_weather_data_to_postgres"
        )

        (
            fetch_weather_data
            >> transform_weather_data
            >> create_weather_table
            >> transfer_weather_data_to_postgres
        )

    end_parallel = DummyOperator(task_id="end")

    with TaskGroup(group_id="fusion_branch") as fusion_branch:
        fetch_weather_data = DummyOperator(task_id="fetch")
        transform_weather_data = DummyOperator(task_id="transform")
        create_weather_table = DummyOperator(task_id="create")
        transfer_weather_data_to_postgres = DummyOperator(task_id="transfer")

        (
            fetch_weather_data
            >> transform_weather_data
            >> create_weather_table
            >> transfer_weather_data_to_postgres
        )

    start >> [status_branch, weather_branch] >> end_parallel >> fusion_branch
