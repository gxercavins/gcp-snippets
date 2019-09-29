import os, datetime, time

from airflow import models
from airflow.contrib.operators.dataflow_operator import DataflowTemplateOperator
from airflow.contrib.hooks.gcp_dataflow_hook import DataFlowHook, _DataflowJob
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials


JOB_NAME='europe_west1_template'
TEMPLATE_PATH='gs://dataflow-templates/latest/Word_Count'
REGION='europe-west1'
ZONE='europe-west1-d'
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
       'region': REGION,
       'zone': ZONE,
       'tempLocation': 'gs://{}/temp/'.format(BUCKET),
       'stagingLocation': 'gs://{}/staging/'.format(BUCKET)
   }
}

class RegionalDataFlowHook(DataFlowHook):
  def _start_template_dataflow(self, name, variables, parameters,
                               dataflow_template):
      # Builds RuntimeEnvironment from variables dictionary
      # https://cloud.google.com/dataflow/docs/reference/rest/v1b3/RuntimeEnvironment
      environment = {}
      for key in ['maxWorkers', 'zone', 'serviceAccountEmail', 'tempLocation',
                  'bypassTempDirValidation', 'machineType', 'network', 'subnetwork']:
          if key in variables:
              environment.update({key: variables[key]})
      body = {"jobName": name,
              "parameters": parameters,
              "environment": environment}
      service = self.get_conn()
      request = service.projects().locations().templates().launch(
          projectId=PROJECT,
          location=REGION,
          gcsPath=TEMPLATE_PATH,
          body=body
      )
      response = request.execute()
      #variables = self._set_variables(variables)
      _DataflowJob(self.get_conn(), PROJECT, name, REGION,
                   self.poll_sleep).wait_for_done()
      return response

class RegionalDataflowTemplateOperator(DataflowTemplateOperator):
  def execute(self, context):
    hook = RegionalDataFlowHook(gcp_conn_id=self.gcp_conn_id,
                        delegate_to=self.delegate_to,
                        poll_sleep=self.poll_sleep)

    hook.start_template_dataflow(self.task_id, self.dataflow_default_options,
                                 self.parameters, self.template)

with models.DAG(
        'dataflow_europe_west1',
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_args) as dag:

        task = RegionalDataflowTemplateOperator(
            task_id=JOB_NAME,
            template=TEMPLATE_PATH,
            parameters={
                'inputFile': 'gs://dataflow-samples/shakespeare/kinglear.txt',
                'output': 'gs://{}/europe/output'.format(BUCKET)
            },
            dag=dag,
         )


        task