from airflow.models import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime
from subdag import subdag_factory
from task_group import training_groups

default_args={
    "start_date": datetime(2021,1,1),
}

with DAG('parent_of_task_group', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:

    start=BashOperator(task_id="start", bash_command="echo 'start'")

    group_training_tasks = training_groups()

    end=BashOperator(task_id="end", bash_command="echo 'end'")

    start >> [group_training_tasks] >> end
