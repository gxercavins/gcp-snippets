# Job Substates

BigQuery jobs include three possible states in the response: `DONE`, `RUNNING` and `PENDING`. How can we extend it to include success/failure/cancellation information. Originally written as an [answer](https://stackoverflow.com/a/54708800/6121516) to a SO question.

## Example

State tracks job progress and if we need success/fail information we'll want to look into the `errorResult` of the [response](https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/list). For successful jobs this will be `None`, for cancelled ones you'll get `{u'reason': u'stopped', u'message': u'Job execution was cancelled: User requested cancellation'}`. 

Code can be found in `job-substates.py`. Replace `PROJECT-ID` accordingly. We'll monitor the following states:

```python
states = ["RUNNING", "PENDING", "SUCCESSFUL", "CANCELLED", "FAILED"]
```

and define the following criteria to map the states with the job response:

```python
def returnState(job):
  if job.state == "DONE":
    if job.error_result is None:
      return "SUCCESSFUL"
    elif job.error_result['reason'] == u'stopped':
      return "CANCELLED"
    else:
      return "FAILED"
  else:
    return job.state
```

We can list and classify the jobs with:

```python
jobs = [job for job in client.list_jobs(project=project, max_results=10)]

for state in states:
  matching_jobs = [job for job in jobs if returnState(job) == state]

  for job in matching_jobs:
    print "Job ID: {0}, State: {1}, Error Result: {2}".format(job.job_id, state, job.error_result)
```

Example output:

```python
Job ID: bquijob_..., State: SUCCESSFUL, Error Result: None
Job ID: bquijob_..., State: SUCCESSFUL, Error Result: None
Job ID: job_..., State: SUCCESSFUL, Error Result: None
Job ID: job_..., State: SUCCESSFUL, Error Result: None
Job ID: job_..., State: SUCCESSFUL, Error Result: None
Job ID: job_..., State: SUCCESSFUL, Error Result: None
Job ID: scheduled_query_..., State: SUCCESSFUL, Error Result: None
Job ID: bquijob_..., State: SUCCESSFUL, Error Result: None
Job ID: bquijob_..., State: CANCELLED, Error Result: {u'reason': u'stopped', u'message': u'Job execution was cancelled: User requested cancellation'}
Job ID: bquijob_..., State: FAILED, Error Result: {u'reason': u'invalidQuery', u'message': u'Syntax error: Illegal input character "\\\\" at [2:18]', u'location': u'query'}
```

Keep in mind that load jobs can be successful but allow for some `maxBadRecords` so that `errorResult` will be not empty, etc.

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
