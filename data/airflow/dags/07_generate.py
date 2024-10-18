import datetime
import random
import os
import json

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago


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
    dag_id="07_generate",
    schedule="@daily",
    default_args=default_args,
)

start = EmptyOperator(
    task_id="start",
    dag=dag,
)

with TaskGroup("section_1", tooltip="Group for section_1", dag=dag) as section_1:
    last = None
    for i in range(3):
        op = EmptyOperator(
            task_id=f"empty_section_1_{i+1}",
            dag=dag,
        )
        if last:
            last >> op
            last = op
        else:
            last = op

with TaskGroup("section_2", tooltip="Group for section_2", dag=dag) as section_2:
    last = None
    with TaskGroup("section_21", tooltip="Group for section_21", dag=dag) as section_21:
        for i in range(3):
            op = EmptyOperator(
                task_id=f"empty_section_21_{i+1}",
                dag=dag,
            )
            if last:
                last >> op
                last = op
            else:
                last = op

    with TaskGroup("section_22", tooltip="Group for section_22", dag=dag) as section_22:
        for i in range(3):
            op = EmptyOperator(
                task_id=f"empty_section_22_{i+1}",
                dag=dag,
            )
    section_21 >> section_22

end = EmptyOperator(
    task_id="end",
    dag=dag,
)


start >> section_1 >> section_2 >> end
