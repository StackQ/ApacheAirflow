from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor

from datetime import datetime, time, timedelta

default_args={
    'start_date': datetime(2020, 1, 1)
}

def my_delta(execution_date):
    return [execution_date - timedelta(minutes=5), execution_date - timedelta(minutes=10)]

with DAG('sensor_target_dag', schedule_interval='15 * * * *', default_args=default_args, catchup=False) as dag:

    waiting_end_parent_dag = ExternalTaskSensor(
        task_id='waiting_end_parent_dag',
        external_dag_id='sensor_parent_dag',
        external_task_id='end',
        execution_delta=timedelta(minutes=5),  # -timedelta(minutes=5), when parent is later scheduled
        ##if need more complex logic for execution date, can't use both execution_delta & execution_date_fn
        #execution_date_fn=my_delta 
        mode='reschedule',
        timeout=5*60
    )

    process_ml = BashOperator(
        task_id="process_ml",
        bash_command = "echo 'prcoessing_ml'"
    )

    waiting_end_parent_dag >> process_ml