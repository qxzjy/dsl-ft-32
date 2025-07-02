from datetime import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.task_group import TaskGroup

default_args = {
    "owner": "airflow",
    "start_date": datetime(2022, 6, 1),
}


with DAG(dag_id="taskgroup_dag", default_args=default_args, catchup=False) as dag:
    start_dag = BashOperator(task_id="start_dag", bash_command="echo 'Start!'")

    with TaskGroup(group_id="first_branch") as first_branch:
        first_task = BashOperator(
            task_id="first_branch", bash_command="echo 'First branch!'; sleep 2"
        )

        second_task = BashOperator(
            task_id="second_branch", bash_command="echo 'Second branch!'; sleep 2"
        )

        third_task = BashOperator(
            task_id="third_branch", bash_command="echo 'Third branch!'; sleep 2"
        )

        first_task >> second_task >> third_task

    with TaskGroup(group_id="second_branch") as second_branch:
        first_task = BashOperator(
            task_id="first_branch", bash_command="echo 'First branch!'; sleep 2"
        )

        second_task = BashOperator(
            task_id="second_branch", bash_command="echo 'Second branch!'; sleep 2"
        )

        third_task = BashOperator(
            task_id="third_branch", bash_command="echo 'Third branch!'; sleep 2"
        )

        first_task >> second_task >> third_task

    end_dag = BashOperator(task_id="end_dag", bash_command="echo 'End!'")

    start_dag >> [first_branch, second_branch] >> end_dag
