# Start a Dataproc job

How to start a new Spark job with the `DataProcSparkOperator` and avoid errors when specifying main class and JAR. Base code and issue summary can be found in the corresponding [StackOverflow question](https://stackoverflow.com/questions/54784034/difficulties-in-using-a-gcloud-composer-dag-to-run-a-spark-job/).

## Example

To find the correct way to set the parameters we can compare it with a successful job using the CLI. We observe that, even when the class was populating the `Main class or jar` field, the path to the Jar was specified in `Jar files`:

[![enter image description here][1]][1]

Checking the operator we can use the `dataproc_spark_jars` [parameter][2], which is not mutually exclusive to setting the `main_class`:


```python
run_spark_job = dpo.DataProcSparkOperator(
    task_id = 'run_spark_job',
    dataproc_spark_jars = [MAIN_JAR],
    main_class = MAIN_CLASS,
    cluster_name = CLUSTER_NAME
)
```

Adding this will do the trick:

[![enter image description here][3]][3]

[![enter image description here][4]][4]


  [1]: https://i.stack.imgur.com/d0Pcf.png
  [2]: https://airflow.apache.org/integration.html#airflow.contrib.operators.dataproc_operator.DataProcSparkOperator
  [3]: https://i.stack.imgur.com/4R2TC.png
  [4]: https://i.stack.imgur.com/021ep.png

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
