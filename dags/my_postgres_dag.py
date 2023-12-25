from airflow.models import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator

from datetime import datetime

class CustomPostgresOperator(PostgresOperator):
    template_fields = ('sql', 'parameters')

def _my_task():
    return 'tweets.csv'

with DAG('my_postgres_dag', schedule_interval='@daily', start_date=datetime(2021,1,1), catchup=False) as dag:
    #docker exec scheduler_container_id airflow providers list

    create = PostgresOperator(
        task_id = 'create_table',
        postgres_conn_id="postgres",
        #sql="CREATE TABLE IF NOT EXISTS my_table (table_value TEXT NOT NULL, PRIMARY KEY (table_value));"
        sql="sql/CREATE_TABLE_MY_TABLE.sql"
    )

    # store = PostgresOperator(
    #     task_id = 'store',
    #     postgres_conn_id="postgres",
    #     #sql="INSERT INTO my_table VALUES ('my_value')"
    #     sql=[
    #     #file content = INSERT INTO my_table (table_value) VALUES (%(filename)s) ON CONFLICT(table_value) DO UPDATE SET table_value='my_new_value'
    #     "sql/INSERT_INTO_MY_TABLE.sql",
    #     #any type of SELECT * won't work, so below sql command will return None | coz we can't fetch rows using PostgresOperator
    #     "SELECT * FROM my_table"
    #     ],
    #     parameters={
    #         'filename': 'data.csv'
    #     }
    # )

    my_task = PythonOperator(
        task_id="my_task",
        python_callable=_my_task
    )

    store = CustomPostgresOperator(
        task_id = 'store',
        postgres_conn_id="postgres",
        #sql="INSERT INTO my_table VALUES ('my_value')"
        sql=[
        "sql/INSERT_INTO_MY_TABLE.sql",
        "SELECT * FROM my_table"
        ],
        parameters={
            'filename': '{{ ti.xcom_pull(task_ids=["my_task"])[0] }}'
        }
    )
     