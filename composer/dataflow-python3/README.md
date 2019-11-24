# Dataflow Python 3 Operator

Dataflow has added Python 3 support but the Airflow `DataFlowPythonOperator` available in Composer assumes that jobs use Python 2. How can we solve this? Originally written as a [StackOverflow answer](https://stackoverflow.com/a/58631655/6121516).

## Example

As of Oct 2019, the newest Airflow version available in Composer is either 1.10.2 or 1.10.3 (depending on the region). To run Python 3 Dataflow jobs with Composer we'd need to wait for a new version to be released. However, for an immediate solution we can back-port the [fix][1].

Three files are included in this folder:

* **dataflow2.py:** normal DAG to run jobs with Python 2 interpreter and the standard `DataFlowPythonOperator`
* **dataflow3.py:** adapted DAG to use a Python 3 interpreter and a modified `DataFlowPython3Operator`
* **main.py:** Dataflow job to be run (uploaded to the `data` folder)

In this case we define a new `DataFlow3Hook` to extend the normal `DataFlowHook`. We will modify it so that the `python2` interpreter is not hard-coded in the `start_python_dataflow` method:

```python
class DataFlow3Hook(DataFlowHook):
    def start_python_dataflow(
        ...
        py_interpreter: str = "python3"
    ):

        ...

        self._start_dataflow(variables, name, [py_interpreter] + py_options + [dataflow],
                             label_formatter)
```

Then, we'll have our custom `DataFlowPython3Operator` calling the new `DataFlow3Hook` hook:

```python
class DataFlowPython3Operator(DataFlowPythonOperator):

    def execute(self, context):
        ...
        hook = DataFlow3Hook(gcp_conn_id=self.gcp_conn_id,
                            delegate_to=self.delegate_to,
                            poll_sleep=self.poll_sleep)
        ...
        hook.start_python_dataflow(
            self.job_name, formatted_options,
            self.py_file, self.py_options, py_interpreter="python3")
```

Finally, in our DAG we just use the new operator:

```python
task = DataFlowPython3Operator(
    py_file='/home/airflow/gcs/data/main.py',
    task_id=JOB_NAME,
    dag=dag)
```

The job runs with Python 3.6:

[![enter image description here][2]][2]

Environment details and dependencies used (Beam job was a minimal example):

```bash
softwareConfig:
  imageVersion: composer-1.8.0-airflow-1.10.3
  pypiPackages:
    apache-beam: ==2.15.0
    google-api-core: ==1.14.3
    google-apitools: ==0.5.28
    google-cloud-core: ==1.0.3
  pythonVersion: '3'
```

Recommendation would be to move the code to a plugin for code readability and to reuse it across DAGs.


  [1]: https://github.com/apache/airflow/pull/5602
  [2]: https://i.stack.imgur.com/boRC0.png

## Shutdown

The provided DAG will schedule a daily batch job that will consume resources. You can turn it off using Airflow's UI.

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
