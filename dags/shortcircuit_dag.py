from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import ShortCircuitOperator

from datetime import datetime

default_args={
    "start_date": datetime(2021, 1, 1),
}

def _is_tuesday(execution_date):
    print(f"today's day is => {execution_date.weekday()}")
    #"TUESDAY" , 0/1/2...where(0=Monday), {"Saturday", "Sunday"}, {WeekDay.SATURDAY, WeekDay.SUNDAY}
    return execution_date.weekday()==0

with DAG('shortcircuit_dag', schedule_interval='10 * * * *', default_args=default_args, catchup=False) as dag:

    task_a=BashOperator(task_id="task_a", bash_command="echo 'task_a'")
    task_b=BashOperator(task_id="task_b", bash_command="echo 'task_b'")
    task_c=BashOperator(task_id="task_c", bash_command="echo 'task_c'")
    
    #task_d only wants to execute on once a week
    task_d=BashOperator(task_id="task_d", bash_command="echo 'task_d'")    

    #diff between branchpythonOperator & shortcircuit is here we are not going to choose either path, 
    #simply don't go ahead for any downstream task
    is_tuesday=ShortCircuitOperator(
        task_id='is_tuesday',
        #if this function return FALSE downstream task of this operator will be skipped
        python_callable=_is_tuesday
    )

    #task_e wants to execute always irrespective of task_d, so use correct trigger_rule all_done/always have to play later
    task_e=BashOperator(task_id="task_e", bash_command="echo 'task_e'", trigger_rule='all_done')    

    task_a >> task_b >> task_c >> is_tuesday >> task_d >> task_e
