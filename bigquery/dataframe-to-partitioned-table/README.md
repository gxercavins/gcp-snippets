# Dataframe to partitioned table

Example, using the Python Client library, to create a time-partitioned table to host data in a pandas dataframe. Originally written as an answer to this [StackOverflow question](https://stackoverflow.com/questions/59430708/how-to-load-dataframe-into-bigquery-partitioned-table-from-cloud-function-with-p/).

## Example

We can modify `time_partitioning` for our [`LoadJobConfig`](https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.job.LoadJobConfig.html#google.cloud.bigquery.job.LoadJobConfig) object. The description of the `TimePartitioning` class can be found [here](https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.table.TimePartitioning.html#google.cloud.bigquery.table.TimePartitioning) and a similar example in the [docs](https://cloud.google.com/bigquery/docs/creating-column-partitions#creating_an_empty_partitioned_table_with_a_schema_definition). We can use `TimePartitioning.field` to specify which field to use as the partitioning criteria. In this case it could be something like this (adding a 90-day expiration rule):

```python
job_config = bigquery.LoadJobConfig(
    schema = [
        bigquery.SchemaField("foo", "STRING"),
        bigquery.SchemaField("Timestamp", "TIMESTAMP"),
        bigquery.SchemaField("bar", "INT64"),
        bigquery.SchemaField("id", "STRING")
    ],
    time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="Timestamp",  # field to use for partitioning
        expiration_ms=7776000000  # 90 days
    )
)
```

We can use the [`LoadJob`](https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.job.LoadJob.html#google.cloud.bigquery.job.LoadJob) result to verify that everything is ok:

```python
print("Written {} rows to {}".format(result.output_rows, result.destination))
print("Partitioning: {}".format(result.time_partitioning))
```

```python
Written 4 rows to TableReference(DatasetReference(u'PROJECT_ID', u'test'), 'pandas_partitioned')
Partitioning: TimePartitioning(expirationMs=7776000000,field=Timestamp,type=DAY)
```

and describe the newly-created table:

```bash
$ bq show test.pandas_partitioned
Table PROJECT_ID:test.pandas_partitioned

   Last modified            Schema            Total Rows   Total Bytes   Expiration                  Time Partitioning                   Clustered Fields   Labels  
 ----------------- ------------------------- ------------ ------------- ------------ -------------------------------------------------- ------------------ -------- 
  21 Dec 10:01:42   |- Timestamp: timestamp   4            107                        DAY (field: Timestamp, expirationMs: 7776000000)                              
                    |- bar: integer                                                                                                                                 
                    |- foo: string                                                                                                                                  
                    |- id: string
```

Full code in `df2pt.py` file.

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
