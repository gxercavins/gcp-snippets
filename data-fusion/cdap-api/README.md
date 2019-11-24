# CDAP API

The Data Fusion [REST API](https://cloud.google.com/data-fusion/docs/reference/rest/) allows to create and shutdown instances, list operations, etc. but how do we access the CDAP API in order to programmatically create pipelines or list runs? Originally written as a StackOverflow [answer](https://stackoverflow.com/a/58963012/6121516). 

## Example

We can retrieve CDAP API endpoint for a Data Fusion instances using the `projects.locations.instances.list` method. We can use, for example. the [`API Explorer`](https://cloud.google.com/data-fusion/docs/reference/rest/v1beta1/projects.locations.instances/list) or cURL:

```bash
PROJECT=$(gcloud config get-value project)
TOKEN=$(gcloud auth print-access-token)
LOCATION=europe-west4

curl -H "Authorization: Bearer $TOKEN" \
    https://datafusion.googleapis.com/v1beta1/projects/$PROJECT/locations/$LOCATION/instances

{
  "instances": [
    {
      "name": "projects/PROJECT/locations/europe-west4/instances/data-fusion-1",
      "type": "BASIC",
      "networkConfig": {},
      "createTime": "2019-11-10T12:02:55.776479620Z",
      "updateTime": "2019-11-10T12:16:41.560477044Z",
      "state": "RUNNING",
      "serviceEndpoint": "https://data-fusion-1-PROJECT-dot-euw4.datafusion.googleusercontent.com",
      "version": "6.1.0.2",
      "serviceAccount": "cloud-datafusion-management-sa@REDACTED-tp.iam.gserviceaccount.com",
      "displayName": "data-fusion-1",
      "apiEndpoint": "https://data-fusion-1-PROJECT-dot-euw4.datafusion.googleusercontent.com/api"
    }
  ]
}
```

Note that `serviceEndpoint` is in the form:

```bash
https://<INSTANCE_DISPLAY_NAME>-<PROJECT_ID>-dot-<REGION_ACRONYM>.datafusion.googleusercontent.com
```

and `apiEndpoint` appends `/api`:

```bash
https://<INSTANCE_DISPLAY_NAME>-<PROJECT_ID>-dot-<REGION_ACRONYM>.datafusion.googleusercontent.com/api
```

Now, we can follow the CDAP reference guide to see, for example, the [run history](https://cloud.google.com/data-fusion/docs/reference/cdap-reference#run_history_for_a_batch_pipeline) for one pipeline:

```bash
GET hostname/api/v3/namespaces/namespace-id/apps/pipeline-name/workflows/DataPipelineWorkflow/runs
```

where `hostname` is the previously obtained `serviceEndpoint`, `namespace-id` will be `default` for a `BASIC` instance (with Enterprise you can have different namespaces) and `pipeline-name` will be `BQ-to-GCS` in this case:

```bash
curl -H "Authorization: Bearer $TOKEN" \
        https://data-fusion-1-$PROJECT-dot-euw4.datafusion.googleusercontent.com/api/v3/namespaces/default/apps/BQ-to-GCS/workflows/DataPipelineWorkflow/runs

[{"runid":"REDACTED","starting":1573395214,"start":1573395401,"end":1573395492,"status":"COMPLETED",
"properties":{"runtimeArgs":"{\"logical.start.time\":\"1573395214003\",\"system.profile.name\":\"SYSTEM:dataproc\"}",
"phase-1":"b8f5c7d1-03c4-11ea-a553-42010aa40019"},"cluster":{"status":"DEPROVISIONED","end":1573395539,"numNodes":3},
"profile":{"profileName":"dataproc","namespace":"system","entity":"PROFILE"}}]]
```

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
