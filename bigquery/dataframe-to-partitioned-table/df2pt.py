from datetime import datetime  
from datetime import timedelta 

import pandas as pd
from google.cloud import bigquery


PROJECT = "PROJECT_ID"
DATASET = "test"
TABLE = "pandas_partitioned"

bq_client = bigquery.Client(project=PROJECT)

job_config = bigquery.LoadJobConfig(
    schema = [
        bigquery.SchemaField("foo", "STRING"),
        bigquery.SchemaField("Timestamp", "TIMESTAMP"),
        bigquery.SchemaField("bar", "INT64"),
        bigquery.SchemaField("id", "STRING")
    ],
    time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="Timestamp",  # name of the column to use for partitioning
        expiration_ms=7776000000  # 90 days
    )
)

data = {"foo": ["fighters", "manchu", "bar", "kien"],
       "Timestamp": [datetime.now() - timedelta(days=i) for i in range(4)],
       "bar": [100, 50, 75, 66],
       "id": ["1", "2", "3", "14"]}

df = pd.DataFrame(data)

load_job = bq_client.load_table_from_dataframe(
    df, '.'.join([PROJECT, DATASET, TABLE]), job_config = job_config
)

result = load_job.result()

print("Written {} rows to {}".format(result.output_rows, result.destination))
print("Partitioning: {}".format(result.time_partitioning))