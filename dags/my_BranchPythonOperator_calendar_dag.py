from airflow.models import DAG
from airflow.operators.python import BranchPythonOperator
from airflow.operators.dummy import DummyOperator

from datetime import datetime
import yaml

default_args={
    'start_date': datetime(2020, 1, 1)
}

def _check_holidays(ds):
    with open('dags/files/days_off.yml', 'r') as f:
        days_off = set(yaml.load(f, Loader=yaml.FullLoader))
        if ds not in days_off:
            return 'process'
        return 'stop'

with DAG('my_BranchPythonOperator_calendar_dag', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:

    check_holidays = BranchPythonOperator(
        task_id="check_holidays",
        python_callable=_check_holidays
    )

    process=DummyOperator(task_id="process")

    cleaning_stock=DummyOperator(task_id="cleaning_stock")

    stop=DummyOperator(task_id="stop")

    check_holidays >> [process, stop]
    process >> cleaning_stock

