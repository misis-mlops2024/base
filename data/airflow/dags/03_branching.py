import datetime
import random

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago


def branching_func():
    if random.random() >= 0.5:
        return "more_0.5"
    else:
        return "less_0.5"


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(3),
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
}

dag = DAG(
    dag_id="03_branching",
    schedule="@daily",
    default_args=default_args,
)

branching = BranchPythonOperator(task_id="branching", python_callable=branching_func, dag=dag)
more = BashOperator(task_id="more_0.5", bash_command='echo "Number is more than 0.5"', dag=dag)
less = BashOperator(task_id="less_0.5", bash_command='echo "Number is less than 0.5"', dag=dag)

branching >> [more, less]
