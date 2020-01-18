# On-demand Data Transfer Runs

When creating some transfers we have the possibility to set a fix refresh interval or on-demand runs. If we go with the latter we can trigger manual runs using the UI but how can we do so programmatically? Originally written as an answer to a [StackOverflow question](https://stackoverflow.com/questions/59800918/how-to-invoke-an-on-demand-bigquery-data-transfer-service/).

## Example

`StartManualTransferRuns` is part of the [RPC library][1] but it does not have a REST API equivalent as of now. How to use that will depend on our environment. In this example we'll use the Python Client Library ([docs][2]). Be sure to install the library using pip:

```bash
pip install google-cloud-bigquery-datatransfer
```

And the main code, using `start_manual_transfer_runs()` in the `manual.py` file:

```python
client = bigquery_datatransfer_v1.DataTransferServiceClient()

PROJECT_ID = 'PROJECT_ID'
TRANSFER_CONFIG_ID = '5e6...7bc'  # alphanumeric ID you'll find in the UI 

parent = client.project_transfer_config_path(PROJECT_ID, TRANSFER_CONFIG_ID)

start_time = bigquery_datatransfer_v1.types.Timestamp(seconds=int(time.time() + 10))

response = client.start_manual_transfer_runs(parent, requested_run_time=start_time)
print(response)
```

Note that we need to use the right Transfer Config ID and the `requested_run_time` has to be of type `bigquery_datatransfer_v1.types.Timestamp` (for which there was no example in the docs). We set a start time 10 seconds ahead of the current execution time.

After running the script we get a response such as:

```js
runs {
  name: "projects/PROJECT_NUMBER/locations/us/transferConfigs/5e6...7bc/runs/5e5...c04"
  destination_dataset_id: "DATASET_NAME"
  schedule_time {
    seconds: 1579358571
    nanos: 922599371
  }
  ...
  data_source_id: "google_cloud_storage"
  state: PENDING
  params {
    ...
  }
  run_time {
    seconds: 1579358581
  }
  user_id: 28...65
}
```

and the transfer is triggered as expected (nevermind the error):

[![enter image description here][3]][3]

As of now, the minimum interval for the GCS transfer is 60 minutes so it won't pick up files less than one hour old ([docs][4]). 


  [1]: https://cloud.google.com/bigquery-transfer/docs/reference/datatransfer/rpc/
  [2]: https://googleapis.dev/python/bigquerydatatransfer/latest/gapic/v1/api.html#google.cloud.bigquery_datatransfer_v1.DataTransferServiceClient.start_manual_transfer_runs
  [3]: https://i.stack.imgur.com/Dtsi6.png
  [4]: https://cloud.google.com/bigquery-transfer/docs/cloud-storage-transfer#minimum_intervals

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
