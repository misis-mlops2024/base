import datetime
import random
import os
import json

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago
from airflow.providers.docker.operators.docker import DockerOperator


default_args = {
    "owner": "airflow",
    "depends_on_past": True,
    "start_date": days_ago(1),
    "email": ["airflow@example.com"],
    "retries": 1,
    "catchup": False,
    "retry_delay": datetime.timedelta(minutes=5),
}

dag = DAG(
    dag_id="08_docker",
    schedule="@daily",
    default_args=default_args,
)

start = EmptyOperator(
    task_id="start",
    dag=dag,
)

docker_op = DockerOperator(
    task_id="docker_hello_world",
    image="hello-world"
)

start >> docker_op
