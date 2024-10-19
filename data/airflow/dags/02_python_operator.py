from __future__ import annotations

import datetime
import time

import pendulum

from airflow.models.dag import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator, PythonVirtualenvOperator


def print_context(ds=None, **kwargs):
    """Print the Airflow context and ds variable from the context."""
    print("::group::All kwargs")
    print(kwargs)
    print("::endgroup::")
    print("::group::Context variable ds")
    print(ds)
    print("::endgroup::")
    return "Whatever you return gets printed in the logs"


def my_sleeping_function(random_base):
    """This is a function that will run within the DAG execution"""
    time.sleep(random_base)


def callable_virtualenv():
    """
    Example function that will be performed in a virtual environment.

    Importing at the module level ensures that it will not attempt to import the
    library before it is installed.
    """
    from time import sleep

    from colorama import Back, Fore, Style

    print(Fore.RED + "some red text")
    print(Back.GREEN + "and with a green background")
    print(Style.DIM + "and in dim text")
    print(Style.RESET_ALL)
    for _ in range(4):
        print(Style.DIM + "Please wait...", flush=True)
        sleep(1)
    print("Finished")


with DAG(
    dag_id="02_python_operator",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["myexample"],
) as dag:

    python_op = PythonOperator(task_id="print_the_context", python_callable=print_context)

    for i in range(5):
        sleeping_task = PythonOperator(
            task_id=f"sleep_for_{i}",
            python_callable=my_sleeping_function,
            op_kwargs={"random_base": i / 10},
        )

        python_op >> sleeping_task

    virtualenv_task = PythonVirtualenvOperator(
        task_id="virtualenv_python",
        python_callable=callable_virtualenv,
        requirements=["colorama==0.4.0"],
        system_site_packages=False,
    )

    sleeping_task >> virtualenv_task


if __name__ == "__main__":
    dag.test()
