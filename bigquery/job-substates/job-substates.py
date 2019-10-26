from google.cloud import bigquery
client = bigquery.Client()

project = "PROJECT-ID"
states = ["RUNNING", "PENDING", "SUCCESSFUL", "CANCELLED", "FAILED"]


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


jobs = [job for job in client.list_jobs(project=project, max_results=10)]

for state in states:
  matching_jobs = [job for job in jobs if returnState(job) == state]

  for job in matching_jobs:
    print "Job ID: {0}, State: {1}, Error Result: {2}".format(job.job_id, state, job.error_result)
