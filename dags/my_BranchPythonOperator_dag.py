from airflow.models import DAG
from airflow.operators.python import BranchPythonOperator
from airflow.operators.dummy import DummyOperator

from datetime import datetime

default_args={
    'start_date': datetime(2020, 1, 1)
}

def _check_accurancy():
    accuracy = 1
    if accuracy >= 1:
        return ['accurate', 'top_accurate']
    return 'inaccurate'

with DAG('my_BranchPythonOperator_dag', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:

    training_ml = DummyOperator(task_id="training_ml")

    check_accurancy = BranchPythonOperator(
        task_id="check_accuracy",
        python_callable=_check_accurancy
    )

    accurate = DummyOperator(task_id="accurate")
    top_accurate = DummyOperator(task_id="top_accurate")
    inaccurate = DummyOperator(task_id="inaccurate")

    publish_ml=DummyOperator(task_id="publish_ml", trigger_rule='none_failed_or_skipped')

    training_ml >> check_accurancy >> [accurate, inaccurate, top_accurate] >> publish_ml

