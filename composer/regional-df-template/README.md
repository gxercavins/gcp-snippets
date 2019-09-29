# Regional Dataflow Template Operator

Issue: I'm using the [`DataflowTemplateOperator`](https://airflow.apache.org/_api/airflow/contrib/operators/dataflow_operator/index.html#airflow.contrib.operators.dataflow_operator.DataflowTemplateOperator) in Composer and the Dataflow job always runs in `us-central1` even if I pass a different `region`.

## Example

In Airflow [1.10.2](https://github.com/apache/airflow/blob/1.10.2/airflow/contrib/hooks/gcp_dataflow_hook.py#L285)(or lower) the code calls to the `service.projects().templates().launch()` endpoint. This was fixed in [1.10.3](https://github.com/apache/airflow/blob/1.10.3/airflow/contrib/hooks/gcp_dataflow_hook.py#L283) where the regional one is used instead: `service.projects().locations().templates().launch()`. Notice `locations()` in path.

As of September 2019, the latest Airflow version available for Composer environments is 1.10.2. Taking into account that regionalization is normally imposed as an organization policy it can be of interest to backport the fix into Composer.

For this we can override the `DataflowTemplateOperator` for our own version called `RegionalDataflowTemplateOperator`:

```python
class RegionalDataflowTemplateOperator(DataflowTemplateOperator):
  def execute(self, context):
    hook = RegionalDataFlowHook(gcp_conn_id=self.gcp_conn_id,
                        delegate_to=self.delegate_to,
                        poll_sleep=self.poll_sleep)

    hook.start_template_dataflow(self.task_id, self.dataflow_default_options,
                                 self.parameters, self.template)
```

This will now make use of the modified `RegionalDataFlowHook` which overrides the `start_template_dataflow` method of the `DataFlowHook` operator to call the correct endpoint:

```python
class RegionalDataFlowHook(DataFlowHook):
  def _start_template_dataflow(self, name, variables, parameters,
                               dataflow_template):
      ...
      request = service.projects().locations().templates().launch(
          projectId=PROJECT,
          location=REGION,
          gcsPath=TEMPLATE_PATH,
          body=body
      )
      ...
      return response
```

Then, we can create a task using our new operator and a Google-provided [template](https://cloud.google.com/dataflow/docs/guides/templates/provided-templates):

```python
task = RegionalDataflowTemplateOperator(
    task_id=JOB_NAME,
    template=TEMPLATE_PATH,
    parameters={
        'inputFile': 'gs://dataflow-samples/shakespeare/kinglear.txt',
        'output': 'gs://{}/europe/output'.format(BUCKET)
    },
    dag=dag,
)
```

Example code provided in the `df-europe-west1.py` DAG file. For a cleaner version, the operator can be moved into a separate module.

## Shutdown

The provided DAG will schedule a daily batch job that will consume resources. You can turn it off using Airflow's UI.

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
