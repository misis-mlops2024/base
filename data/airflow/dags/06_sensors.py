import datetime
import random
import os
import json

from airflow import DAG
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.python import PythonSensor


def _wait_for_file():
    return os.path.exists("/opt/data/wait.txt")


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(3),
    "email": ["airflow@example.com"],
    "retries": 1,
    "catchup": False,
    "retry_delay": datetime.timedelta(minutes=5),
}

dag = DAG(
    dag_id="06_sensors",
    schedule="@daily",
    default_args=default_args,
)

t1 = BashOperator(task_id="touch_file_1", bash_command="touch /opt/data/1.txt", dag=dag)

wait = PythonSensor(
    task_id="wait_for_file",
    python_callable=_wait_for_file,
    timeout=6000,
    poke_interval=10,
    retries=100,
    mode="poke",
    dag=dag,
)

t3 = BashOperator(
    task_id="touch_file_3",
    bash_command="touch /opt/data/2.txt",
    dag=dag,
)

wait_fs = FileSensor(
    task_id="wait_for_local_file",
    filepath="/opt/data/3.txt",
    retries=100,
    poke_interval=10,
    mode="reschedule",
    dag=dag,
)

t1 >> wait >> t3 >> wait_fs
