import datetime
import random

from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator
from airflow.operators.bash import BashOperator
from airflow.datasets import Dataset
from airflow.utils.dates import days_ago


dag1_dataset = Dataset(
    "s3://mlflow/4/7dfe532ce2cf48e2ad064affa215cab2/artifacts/estimator.html", extra={"hi": "bye"}
)


def mlflow_func(**context):
    import os
    import mlflow

    os.environ["AWS_ACCESS_KEY_ID"] = "mlflow"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "password"
    os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5000"
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_registry_uri("http://localhost:5000")
    mlflow.set_experiment("exp")

    with mlflow.start_run():
        mlflow.log_param("a", 1)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
}

dag = DAG(
    dag_id="09_mlflow",
    schedule=[dag1_dataset],
    default_args=default_args,
)

virtualenv_task = PythonVirtualenvOperator(
    task_id="virtualenv_python",
    python_callable=mlflow_func,
    requirements=["mlflow==2.16.2"],
    system_site_packages=False,
    dag=dag,
)

virtualenv_task
