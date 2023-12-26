from airflow.models import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime

default_args={
    "start_date": datetime(2021, 1, 1),
}

with DAG('sensor_parent_dag', schedule_interval='10 * * * *', default_args=default_args, catchup=False) as dag:

    start=BashOperator(task_id="start", bash_command="echo 'start'")

    end=BashOperator(task_id="end", bash_command="echo 'end'")

    start >> end
