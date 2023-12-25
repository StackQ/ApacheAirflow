from airflow.models import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime

with DAG('my_bash_dag', schedule_interval='@daily', start_date=datetime(2021,1,1), catchup=False) as dag:

    execute_command = BashOperator(
        task_id = 'execute_command',
        #bash_command="echo 'execute my command' && echo 'hello'"
        
        ##all the commands/line/statements written in sh file will be returned to XCom
        #bash_command = "scripts/commands.sh"

        ##all the commands/line/statements written in sh file will be returned to XCom, which obvi we wouldn't want coz of limit
        # bash_command = "scripts/commands.sh"
        # do_xcom_push = False

        ##by default bashOperator is able to access all env variables
        # bash_command = "scripts/commands.sh",
        # do_xcom_push = False       

        ##by default bashOperator is able to access all env variables | to avoid this issue
        # bash_command = "scripts/commands.sh",
        # do_xcom_push = False,
        # env = {
        #     "my_var" : "my_value"
        # }      

        ##if words are like - key, token, pass, auth, secret | airflow will automatically hide | will be hidden in 'env' in sh file also
        bash_command = "scripts/commands.sh",
        do_xcom_push = False,
        #defined in admin->variables
        env = {
            "api_aws" : "{{ var.value.api_key_aws }}"
        }                 
    )