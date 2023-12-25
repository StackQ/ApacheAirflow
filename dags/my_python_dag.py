from airflow.models import DAG, Variable
from airflow.operators.python import PythonOperator

from datetime import datetime

def _task_a(filename, path, **context):
    #print("Hello task_a")
    print(f"{path} / {filename} - {context['ds']}")

with DAG('my_python_dag', schedule_interval='@daily', start_date=datetime(2021,1,1), catchup=False) as dag:
    
    task_a = PythonOperator(
        task_id='task_a',
        python_callable=_task_a,

        ##_task_a(path, filename): order matters here in below input
        #op_args=['/user/local/airflow', 'data.csv'],

        ##_task_a(fname, path): order won't matter in below way | we can't provide both :: op_args & op_kwargs
        # op_kwargs={
        #     #'path':'/user/local/airflow',
        #     #'filename': 'data.csv'
        #     ##using defined variables in Admin->variables | here actually it will create conn to metadata to fetch the variables
        #     'path': '{{ var.value.path }}',
        #     'filename': '{{ var.value.filename }}'
        # }
        

        ##using defined variable 'my_settings' where data is provided as json with path&filename both as 2 keys in json
        op_kwargs=Variable.get("my_settings", deserialize_json=True)

        #provide_context=True # in vesion 1.0
    )