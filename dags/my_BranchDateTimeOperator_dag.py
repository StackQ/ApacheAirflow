from airflow.models import DAG
from airflow.operators.datetime import BranchDateTimeOperator
from airflow.operators.dummy import DummyOperator

from datetime import datetime, time
import yaml

default_args={
    'start_date': datetime(2020, 1, 1)
}

with DAG('my_BranchDateTimeOperator_dag', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:

    is_in_timeframe = BranchDateTimeOperator(
        task_id="is_in_timeframe",
        follow_task_ids_if_true=['move_forward'],
        follow_task_ids_if_false=['end'],
        target_lower=time(10, 0, 0), # if we set it 11.30 which is > than target_upper=11, so it will consider next day's 11.30
        target_upper=time(11, 0, 0),
        #also wont't be able to run past triggered dag runs
        #behind the scene BranchDateTimeOperator checks the current_datetime with - target_lower & target_upper
        #so if False it will not check execution_date of dag, but the current_datetime and if trigger past dags will fail coz 
        #the current_datetime is not equal to past datetimes
        #so by setting this parameter the BranchDateTimeOperator will check if execution_date of dag is within target_lower & upper
        use_task_execution_date=True      
    )

    move_forward=DummyOperator(task_id="move_forward")
    end=DummyOperator(task_id="end")

    is_in_timeframe >> [move_forward, end]