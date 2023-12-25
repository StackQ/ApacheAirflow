from airflow.models import DAG, Variable
from airflow.decorators import task
from airflow.operators.python import get_current_context
from airflow.operators.bash import BashOperator

from datetime import datetime

#with taskFlowAPI as below we can't use **context / ds / other context known variables, there is another way
@task
def process(my_settings):
    context = get_current_context()
    #this function name will become the task_name coz of @task / taskFlowAPI
    print(f"{my_settings['path']} / {my_settings['filename']} - {context['ds_nodash']} = {context['ds']}")

@task(task_id='print_mysetting') # to change the task name coz default will be function name 
def print_it(my_settings):
    #this function name will become the task_name coz of @task / taskFlowAPI
    print(f"{my_settings['path']} / {my_settings['filename']}")    


with DAG('my_python_TaskFlow_API_dag', schedule_interval='@daily', start_date=datetime(2021,1,1), catchup=False) as dag:
    
    store = BashOperator(
        task_id = "store",
        bash_command = "echo 'store'"
    )

    store >> process(Variable.get("my_settings", deserialize_json=True)) >> print_it(Variable.get("my_settings", deserialize_json=True)) 

