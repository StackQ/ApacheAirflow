from airflow.models import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.sql import BranchSQLOperator
from airflow.operators.dummy import DummyOperator

from datetime import datetime
import yaml

default_args={
    'start_date': datetime(2020, 1, 1)
}

with DAG('branch_sql_dag', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:

    create_table=PostgresOperator(
        task_id="create_table",
        sql="sql/CREATE_TABLE_PARTNERS.sql",
        postgres_conn_id='postgres'
    )

    insert_data=PostgresOperator(
        task_id="insert_data",
        sql="sql/INSERT_INTO_PARTNERS.sql",
        postgres_conn_id='postgres'
    )    

    choose_task=BranchSQLOperator(
        task_id="choose_task",
        #return type for below should be only boolean - int,bool, bit, string(may occur mistakes)
        sql="SELECT COUNT(1) FROM partners WHERE partner_status=TRUE",
        follow_task_ids_if_true=['process'],
        follow_task_ids_if_false=['notif_email', 'notif_slack'],
        conn_id='postgres',
        #database='postgres', #mysql/oracle/or dbname
        #parameters= template if required
    )

    process = DummyOperator(task_id="process")
    notif_email = DummyOperator(task_id="notif_email")
    notif_slack = DummyOperator(task_id="notif_slack")

    create_table >> insert_data >> choose_task >> [process, notif_email, notif_slack]
