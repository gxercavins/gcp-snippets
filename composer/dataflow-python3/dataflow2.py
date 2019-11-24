import os, datetime, time

from airflow import models
from airflow.contrib.operators.dataflow_operator import DataFlowPythonOperator
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


JOB_NAME='dataflow-python2'
PROJECT='PROJECT_ID'
BUCKET='BUCKET_NAME'

yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

default_args = {
    'start_date': yesterday,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': datetime.timedelta(minutes=1),
    'dataflow_default_options': {
       'project': PROJECT,
       'tempLocation': 'gs://{}/temp/'.format(BUCKET),
       'stagingLocation': 'gs://{}/staging/'.format(BUCKET),
       'inputFile': 'gs://dataflow-samples/shakespeare/kinglear.txt',
       'output': 'gs://{}/output'.format(BUCKET)
   }
}

with models.DAG(
        'dataflow_python2',
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_args) as dag:

        task = DataFlowPythonOperator(
            py_file='/home/airflow/gcs/data/wordcount.py',
            task_id=JOB_NAME,
            dag=dag)

        task
