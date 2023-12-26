from airflow.models import DAG
from airflow.operators.bash import BashOperator


def subdag_factory(parent_dag_id, subdag_dag_id, default_args):
    default_args['pool'] = "one_task_pool" #or without quote have to confirm
    with DAG(f"{parent_dag_id}.{subdag_dag_id}", default_args=default_args) as dag:
        #if want to execute below in sequence | one way is pool
        training_a=BashOperator(task_id="training_a", bash_command="echo {{dag_run.conf['output']}}")
        training_b=BashOperator(task_id="training_b", bash_command="echo 'training_b'")
        training_c=BashOperator(task_id="training_c", bash_command="echo 'training_c'")  

    return dag      