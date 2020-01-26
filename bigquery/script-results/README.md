# Script Results

Example, using the Python Client library, to get results for one of the queries that conform a BigQuery script. Originally written as an answer to this [StackOverflow question](https://stackoverflow.com/a/59809289/6121516).

## Example

According to the scripting [documentation][1]:

> Scripts are executed in BigQuery using jobs.insert, similar to any
> other query, with the multi-statement script specified as the query
> text. When a script executes, additional jobs, known as **child jobs**,
> **are created for each statement in the script**. You can enumerate the
> child jobs of a script by calling jobs.list, passing in the script’s
> job ID as the parentJobId parameter.
> 
> **When jobs.getQueryResults is invoked on a script, it will return the**
> **query results for the last SELECT, DML, or DDL statement to execute** in
> the script, with no query results if none of the above statements have
> executed. To obtain the results of all statements in the script,
> enumerate the child jobs and call jobs.getQueryResults on each of
> them.

As an example, we use a script to query a public table: `bigquery-public-data.london_bicycles.cycle_stations`. This runs three child jobs:

[![enter image description here][2]][2]

where the **last one** drops the table and **does not return any row**:

[![enter image description here][3]][3]

That's why, if we run the Python file, we'll get an `_EmptyRowIterator` object such as `<google.cloud.bigquery.table._EmptyRowIterator object at 0x7f440aa33c88>`.

What we want is the **output result** of the middle **query**:

[![enter image description here][4]][4]

To do so, the first step is to call [`jobs.list`][5] and pass the script job ID as the `parentJobId` parameter to get the list of child job IDs:

```python
for job in client.list_jobs(parent_job=query_job.job_id):
    print("Job ID: {}, Statement Type: {}".format(job.job_id, job.statement_type))
```

We use the [`list_jobs`][6] method and check [ID and statement type][7]:

```python
Job ID: script_job_80e...296_2, Statement Type: DROP_TABLE
Job ID: script_job_9a0...7fd_1, Statement Type: SELECT
Job ID: script_job_113...e13_0, Statement Type: CREATE_TABLE_AS_SELECT
```

Note that the suffix (0, 1, 2) indicates the execution order but we can a check to verify that the job is actually a `SELECT` statement before retrieving the results:

```python
client = bigquery.Client()
QUERY = """
BEGIN
    CREATE OR REPLACE TEMP TABLE t0 AS
        SELECT name, bikes_count FROM `bigquery-public-data.london_bicycles.cycle_stations` WHERE bikes_count > 10;

    SELECT SUM(bikes_count) AS total_bikes FROM t0;

    DROP TABLE IF EXISTS t0;
END;
"""

query_job = client.query(QUERY)
query_job.result()

for job in client.list_jobs(parent_job=query_job.job_id):  # list all child jobs
    # print("Job ID: {}, Statement Type: {}".format(job.job_id, job.statement_type))
    if job.statement_type == "SELECT":  # print the desired job output only
        rows = job.result()
        for row in rows:
            print("sum={}".format(row["total_bikes"]))
```

output:

```python
sum=6676
```

Full code in `get_script_results.py` file. Tested with `google-cloud-bigquery==1.23.1`.

  [1]: https://cloud.google.com/bigquery/docs/reference/standard-sql/scripting#bigquery-scripting
  [2]: https://i.stack.imgur.com/BKBGZ.png
  [3]: https://i.stack.imgur.com/gJ5Em.png
  [4]: https://i.stack.imgur.com/8v3Sz.png
  [5]: https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/list
  [6]: https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.client.Client.html#google.cloud.bigquery.client.Client.list_jobs
  [7]: https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.job.QueryJob.html#google.cloud.bigquery.job.QueryJob



## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
