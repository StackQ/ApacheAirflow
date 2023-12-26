from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.latest_only import LatestOnlyOperator
from airflow.operators.dummy import DummyOperator

from datetime import datetime

default_args={
    "start_date": days_ago(3),
}

with DAG('newsletter_dag', schedule_interval='@daily', default_args=default_args, catchup=True) as dag:

    getting_date=DummyOperator(task_id="getting_date")
    creating_email=DummyOperator(task_id="creating_email")

    #run this task in latest run only in case of backfill/past triggered dag, don't want users to flood with emails
    sending_newsletter=DummyOperator(task_id="sending_newsletter")

    is_latest = LatestOnlyOperator(task_id='is_latest')

    getting_date >> creating_email >> is_latest >> sending_newsletter


