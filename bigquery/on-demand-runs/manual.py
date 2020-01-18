import time

from google.cloud import bigquery_datatransfer_v1
from google.protobuf.timestamp_pb2 import Timestamp


client = bigquery_datatransfer_v1.DataTransferServiceClient()

PROJECT_ID = 'PROJECT_ID'
TRANSFER_CONFIG_ID = '5e6...7bc'  # alphanumeric ID you'll find in the UI 

parent = client.project_transfer_config_path(PROJECT_ID, TRANSFER_CONFIG_ID)

start_time = bigquery_datatransfer_v1.types.Timestamp(seconds=int(time.time() + 10))

response = client.start_manual_transfer_runs(parent, requested_run_time=start_time)
print(response)