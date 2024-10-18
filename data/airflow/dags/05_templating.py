import datetime
import random
import os
import json

from airflow import DAG
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.models import TaskInstance


def _get_data(
    year: str,
    month: str,
    day: str,
    hour: str,
    output_dir: str,
    task_instance: TaskInstance,
    execution_date,
):
    print(execution_date)
    print("year", year)
    print("month", month)
    print("day", day)
    print("hour", hour)
    print(task_instance)

    result = {"wow": f"{year}/{month}/{day}/{hour}", "task_id": task_instance.task_id}
    output = os.path.join(output_dir, f"{year}_{month}_{day}_{hour}.json")
    with open(output, "w") as f:
        json.dump(result, f)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(3),
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
}

dag = DAG(
    dag_id="05_templating",
    schedule="@daily",
    default_args=default_args,
)

get_data = PythonOperator(
    task_id="get_data",
    python_callable=_get_data,
    op_kwargs={
        "year": "{{ execution_date.year }}",
        "month": "{{ execution_date.month }}",
        "day": "{{ execution_date.day }}",
        "hour": "{{ execution_date.hour }}",
        "output_dir": "/opt/data",
    },
    dag=dag,
)

bash_example = BashOperator(
    task_id="bash_command",
    bash_command="echo {{ ds }}",
    dag=dag,
)

bash_example >> get_data
