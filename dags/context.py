from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime

default_args = {
    'start_date': datetime(2023, 12, 20)
}

def _my_function(ds, yesterday_ds_nodash, **context):
    for k,v in context.items():
        print(f"context key={k} : {v}", end='\n')
    print("-="*50)
    print(f"KNOWN Context keys can be directly used => ds={ds} | yesterday_ds_nodash={yesterday_ds_nodash}") 

with DAG('context', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:

    my_task = PythonOperator(
        task_id='get_print_context_task',
        python_callable=_my_function
        #in 1.0 versions->
        #provide_context=True
    )