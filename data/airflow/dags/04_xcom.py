import datetime
import random

from airflow import DAG
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago


def branching_func(**context):
    value = random.random()
    context["task_instance"].xcom_push(key="random_value_from_function", value=value)
    if value >= 0.5:
        return "more_0.5"
    else:
        return "less_0.5"


def print_xcom_value(**context):
    value = context["task_instance"].xcom_pull(key="random_value_from_function")
    print(f"Input value is {value}")


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(3),
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
}

dag = DAG(
    dag_id="04_xcom",
    schedule="@daily",
    default_args=default_args,
)

branching = BranchPythonOperator(task_id="branching", python_callable=branching_func, dag=dag)
more = BashOperator(task_id="more_0.5", bash_command='echo "Number is more than 0.5"', dag=dag)
less = BashOperator(task_id="less_0.5", bash_command='echo "Number is less than 0.5"', dag=dag)

print_value = PythonOperator(
    task_id="print_value",
    python_callable=print_xcom_value,
    dag=dag,
    trigger_rule="one_success",
)


branching >> [more, less] >> print_value
