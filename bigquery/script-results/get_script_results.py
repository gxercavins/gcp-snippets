from google.cloud import bigquery

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
