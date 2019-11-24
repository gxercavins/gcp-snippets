import datetime, re, time

from airflow import models
from airflow.contrib.operators.dataflow_operator import DataFlowPythonOperator, GoogleCloudBucketHelper
from airflow.contrib.hooks.gcp_dataflow_hook import DataFlowHook
from airflow.models import BaseOperator
from typing import Dict, List


JOB_NAME='dataflow-python3'
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
       'stagingLocation': 'gs://{}/staging/'.format(BUCKET)
   }
}


class DataFlow3Hook(DataFlowHook):
    def start_python_dataflow(
        self,
        job_name: str,
        variables: Dict,
        dataflow: str,
        py_options: List[str],
        append_job_name: bool = True,
        py_interpreter: str = "python3"
    ):

        name = self._build_dataflow_job_name(job_name, append_job_name)
        variables['job_name'] = name

        def label_formatter(labels_dict):
            return ['--labels={}={}'.format(key, value)
                    for key, value in labels_dict.items()]

        self._start_dataflow(variables, name, [py_interpreter] + py_options + [dataflow],
                             label_formatter)


class DataFlowPython3Operator(DataFlowPythonOperator):

    def execute(self, context):
        """Execute the python dataflow job."""
        bucket_helper = GoogleCloudBucketHelper(
            self.gcp_conn_id, self.delegate_to)
        self.py_file = bucket_helper.google_cloud_to_local(self.py_file)
        hook = DataFlow3Hook(gcp_conn_id=self.gcp_conn_id,
                            delegate_to=self.delegate_to,
                            poll_sleep=self.poll_sleep)
        dataflow_options = self.dataflow_default_options.copy()
        dataflow_options.update(self.options)
        # Convert argument names from lowerCamelCase to snake case.
        camel_to_snake = lambda name: re.sub(
            r'[A-Z]', lambda x: '_' + x.group(0).lower(), name)
        formatted_options = {camel_to_snake(key): dataflow_options[key]
                             for key in dataflow_options}
        hook.start_python_dataflow(
            self.job_name, formatted_options,
            self.py_file, self.py_options, py_interpreter="python3")


with models.DAG(
        'dataflow_python3',
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_args) as dag:

        task = DataFlowPython3Operator(
            py_file='/home/airflow/gcs/data/main.py',
            task_id=JOB_NAME,
            dag=dag)

        task
