"""
ETL avec Neon (classique) et S3 : crée un fichier CSV local, le charge dans S3, crée une table Neon et importe les données.
"""
from datetime import datetime
import pandas as pd
from airflow import DAG
from airflow.hooks.S3_hook import S3Hook
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from s3_to_postgres import S3ToPostgresOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 7, 1),
    "retries": 1,
}

def _create_csv():
    """Crée un fichier CSV local avec des données fictives."""
    df = pd.DataFrame({
        "first_name": ["Dark", "Dark"],
        "last_name": ["Vador", "Maul"]
    })
    df.to_csv("/tmp/my_csv_file.csv", index=False)

def _upload_to_s3():
    """Charge le fichier CSV dans le bucket S3 défini dans la variable Airflow 'S3BucketName'."""
    s3 = S3Hook(aws_conn_id="aws_default")
    s3.load_file(
        filename="/tmp/my_csv_file.csv",
        key="my_csv_file.csv",
        bucket_name=Variable.get("S3BucketName"),
        replace=True
    )

with DAG(
    dag_id="s3_neon_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description="DAG ETL simple vers Neon classique avec S3"
) as dag:

    create_csv = PythonOperator(
        task_id="create_csv",
        python_callable=_create_csv
    )

    upload_csv_to_s3 = PythonOperator(
        task_id="upload_csv_to_s3",
        python_callable=_upload_to_s3
    )

    create_neon_table = PostgresOperator(
        task_id="create_neon_table",
        postgres_conn_id="neon_default", 
        sql="""
            CREATE TABLE IF NOT EXISTS public.airflow_lecture (
                first_name VARCHAR,
                last_name VARCHAR
            );
        """
    )
    
    load_data_to_neon = S3ToPostgresOperator(
        task_id="load_data_to_neon",
        table="airflow_lecture",
        bucket="{{ var.value.S3BucketName }}",
        key="my_csv_file.csv",
        postgres_conn_id="neon_default",
        aws_conn_id="aws_default",
    )

    create_csv >> upload_csv_to_s3 >> create_neon_table >> load_data_to_neon
