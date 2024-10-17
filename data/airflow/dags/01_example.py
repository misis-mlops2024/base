from __future__ import annotations

import datetime

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.operators.python import PythonOperator

with DAG(
    dag_id="01_example",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["myexample"],
) as dag:
    
    task_bash_op = BashOperator(
        task_id="show_files",
        bash_command="ls /opt/airflow/",
    )
    
    def my_custom_function(input_value):
        print(f'Square of input value is: {input_value ** 2}')
    
    task_python_op = PythonOperator(
        task_id="python_operator",
        python_callable=my_custom_function,
        op_kwargs={"input_value": 15},
    )
    
    task_bash_op >> task_python_op


if __name__ == "__main__":
    dag.test()
