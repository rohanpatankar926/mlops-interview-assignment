import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator

default_args = {
    "owner": "airflow",
    "depends_on_spast": False,
    "start_date": pendulum.datetime(2023, 1, 9),
    "email": ["rohanpatankar926@gmail.com"],
}

def training(**kwargs):
    from mlops.pipeline import pipeline
    pipeline.pipeline_initiate()

bash_success="echo 'Training Pipeline is completed successfully'"

with DAG(dag_id="training_dag",default_args=default_args,description="Sensor Training Pipeline",
schedule_interval="@weekly",catchup=False,tags=["sensor","something"]) as dag:   
    
    training_pipeline=PythonOperator(task_id="training_pipeline",python_callable=training)
    success=BashOperator(task_id="success",bash_command=bash_success)
    email_notification = EmailOperator(
    task_id='send_email',
    to='rohanpatankar926@gmail.com',
    subject='Training pipeline successfully completed',
    html_content='<p>Training pipeline successfully completed.</p>'
)
    training_pipeline>>success>>email_notification