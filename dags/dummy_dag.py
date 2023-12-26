from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator

from datetime import datetime

default_args={
    "start_date": days_ago(3),
}

with DAG('dummy_dag', schedule_interval='@daily', default_args=default_args, catchup=True) as dag:

    task_a=BashOperator(task_id="task_a", bash_command="echo 'task_a'")
    task_b=BashOperator(task_id="task_b", bash_command="echo 'task_b'")
    task_c=BashOperator(task_id="task_c", bash_command="echo 'task_c'")
    task_d=BashOperator(task_id="task_d", bash_command="echo 'task_d'") 
    dummy = DummyOperator(task_id='dummy')   

    task_a >> dummy << task_b
    dummy >> [task_c, task_d]


