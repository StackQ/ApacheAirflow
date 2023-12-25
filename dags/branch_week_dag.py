from airflow.models import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.weekday import BranchDayOfWeekOperator
from airflow.utils.weekday import WeekDay

from datetime import datetime, time
import yaml

default_args={
    'start_date': datetime(2020, 1, 1)
}

with DAG('my_BranchDayOfWeekOperator_dag', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:

    task_a = DummyOperator(task_id="task_a")
    task_b = DummyOperator(task_id="task_b")

    is_wednesday = BranchDayOfWeekOperator(
        task_id="is_wednesday",
        follow_task_ids_if_true=["wed_MON_task"],
        follow_task_ids_if_false=["end"],
        week_day = {WeekDay.WEDNESDAY, WeekDay.MONDAY},
        #False by default evaluate current_datetime, so for past triggered date it should consider execution_date and can re-execute
        use_task_execution_day=True
    )

    wed_MON_task = DummyOperator(task_id="wed_MON_task")
    end = DummyOperator(task_id="end")

    task_a >> task_b >> is_wednesday >> [wed_MON_task, end]