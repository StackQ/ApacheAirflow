from airflow.models import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime, time

default_args={
    'start_date': datetime(2020, 1, 1)
}

with DAG('target_dag', schedule_interval=None, default_args=default_args, catchup=False):

    process_ml=BashOperator(
        task_id="process_ml",
        bash_command="echo '{{ dag_run.conf['path]}}'"
    )