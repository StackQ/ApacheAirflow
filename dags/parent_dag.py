from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from datetime import datetime
from task_group import training_groups

default_args={
    "start_date": datetime(2021, 1, 1),
}

with DAG('parent_dag', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:

    start=BashOperator(task_id="start", bash_command="echo 'start'")

    group_training_tasks = training_groups()

    process_ml = TriggerDagRunOperator(
        task_id='process_ml',
        trigger_dag_id="target_dag",
        conf={
            'path': '/opt/airflow/ml'
        },
        #to have same execution date between parent & child dag | and if this date used in child ex- in sql where clause
        execution_date="{{ ds }}",
        #if rerun past triggered dag will get error with FALSE, as can't trigger dag twice | so to avoid it TRUE and to rerun
        reset_dag_run=True,
        #this dag in charge of processing machine learning model on which there is another task based on it's produce
        #so want to complete it first before moving to next task
        wait_for_completion=True,
        #TriggerDagRunOperator is not a sensor behind the scene so can't use all the same arguments as sensor, but below one avail
        #doesn't work in airflow2.5.1
        #poke_interval=60
        #allowed_states=['success'],
        #failed_states=['']
    )

    end=BashOperator(task_id="end", bash_command="echo 'end'")

    start >> group_training_tasks >> process_ml >> end
