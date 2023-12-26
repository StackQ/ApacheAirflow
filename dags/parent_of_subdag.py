from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator

from datetime import datetime
from subdag import subdag_factory

default_args={
    "start_date": datetime(2021,1,1),
}

with DAG('parent_of_subdag', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:

    start=BashOperator(task_id="start", bash_command="echo 'start'")

    group_training_tasks = SubDagOperator(
        task_id="group_training_tasks",
        #default_args should be same in both parent & subdasg else error
        subdag=subdag_factory('parent_of_subdag', 'group_training_tasks', default_args=default_args),
        #subdagoperator will release work periodically, rather than holding it
        mode='reschedule',
        #60 seconds
        timeout=60*1,
        #here providing pool only  be respected by this subdag not by it's tasks
        #pool=one_task_pool
        conf={'output': '/opt/airflow/ml'},
        #if tasks skipped in subdag, downstream of subdag will also skipped
        #propagate_skippped_state=False
    )

    group_training_tasks_2 = SubDagOperator(
        task_id="group_training_tasks_2",
        #default_args should be same in both parent & subdasg else error
        subdag=subdag_factory('parent_of_subdag', 'group_training_tasks_2', default_args=default_args),
        mode='reschedule',
        timeout=60*1     
    )

    group_training_tasks_3 = SubDagOperator(
        task_id="group_training_tasks_3",
        #default_args should be same in both parent & subdasg else error
        subdag=subdag_factory('parent_of_subdag', 'group_training_tasks_3', default_args=default_args),
        mode='reschedule'        ,
        timeout=60*1      
    )        

    end=BashOperator(task_id="end", bash_command="echo 'end'")

    start >> [group_training_tasks, group_training_tasks_2, group_training_tasks_3] >> end
