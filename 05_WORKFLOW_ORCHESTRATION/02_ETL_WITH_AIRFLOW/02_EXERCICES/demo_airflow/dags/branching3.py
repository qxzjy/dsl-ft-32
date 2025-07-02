from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2022, 6, 1),
}

with DAG(
    dag_id="branching_etl",
    default_args=default_args,
    catchup=False,
    description="DAG intermédiaire illustrant le branching avant un ETL",
) as dag:
    start = DummyOperator(task_id="start")

    extract_fr = BashOperator(
        task_id="extract_fr", bash_command="echo 'Extraction FR terminée'; sleep 1"
    )

    extract_us = BashOperator(
        task_id="extract_us", bash_command="echo 'Extraction US terminée'; sleep 1"
    )

    extract_asia = BashOperator(
        task_id="extract_asia", bash_command="echo 'Extraction ASIA terminée'; sleep 1"
    )

    join = DummyOperator(task_id="join")

    transform_load = BashOperator(
        task_id="transform_load",
        bash_command="echo 'Transformation et chargement terminés'; sleep 2",
    )

    end = DummyOperator(task_id="end")

    start >> [extract_fr, extract_us, extract_asia] >> join >> transform_load >> end
