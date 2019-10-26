# Scheduled Queries - REST API

A couple snippets to demonstrate how to use the REST API to list the scheduled queries and/or create a new one programmatically. Originally written as an [answer][7] to a SO question.

## Example

Scheduled queries are part of BigQuery's Data Transfer Service API. To retrieve the list of existing ones we'll use the [`projects.transferConfigs.list`][1] method. We need to fill in the `dataSourceIds` field with `scheduled_query` and `parent` with `projects/PROJECT_ID`. Take into account that, if we are using a regional location such as `europe-west2 instead` of a multi-regional one (`EU` or `US`) we have to use [`projects.locations.transferConfigs.list`][3] instead. Now, parent resource will be in the form of `projects/PROJECT_ID/locations/REGIONAL_LOCATION`.

In addition, for other data transfers different than scheduled queries, we can get the corresponding `dataSourceIds` value using the [`projects.dataSources.list`][2] method.

Response will be an array of scheduled queries such as:

```json
{
  "name": "projects/<PROJECT_NUMBER>/locations/us/transferConfigs/<TRANSFER_CONFIG_ID>",
  "destinationDatasetId": "<DATASET>",
  "displayName": "hacker-news",
  "updateTime": "2018-11-14T15:39:18.897911Z",
  "dataSourceId": "scheduled_query",
  "schedule": "every 24 hours",
  "nextRunTime": "2019-04-19T15:39:00Z",
  "params": {
    "write_disposition": "WRITE_APPEND",
    "query": "SELECT @run_time AS time,\n  title,\n  author,\n  text\nFROM `bigquery-public-data.hacker_news.stories`\nLIMIT\n  1000",
    "destination_table_name_template": "hacker_daily_news"
  },
  "state": "SUCCEEDED",
  "userId": "<USER_ID>",
  "datasetRegion": "us"
}
```

Example of an API call with bash and `curl` is given in the `list.sh` file:

```bash
# API call
scheduled_queries=$(curl  -H "Authorization: Bearer $authToken" \
  https://bigquerydatatransfer.googleapis.com/v1/projects/$projectId/locations/$location/transferConfigs?dataSourceIds=scheduled_query)

# pretty print results
echo $scheduled_queries | python -m json.tool
```

Similarly, we can create a new scheduled query by issuing a POST request ([`projects.locations.transferConfigs.create`][4]). Example found in `create.sh`:

```bash
# API call
scheduled_query=$(curl  -X POST -H "Authorization: Bearer $authToken" \
  -H "Content-Type: application/json" -d @request.json \
  https://bigquerydatatransfer.googleapis.com/v1/projects/$projectId/locations/$location/transferConfigs)
```

Where the request body (`request.json`) conforms to [`TransferConfig`][5]:

```json
{
  "dataSourceId": "scheduled_query",
  "destinationDatasetId": "test",
  "displayName": "test-api",
  "params": {
      "destination_table_name_template": "test_using${run_date}",
      "query": "SELECT 1",
      "write_disposition": "WRITE_TRUNCATE"
  },
  "schedule": "every day 18:03"
}
```

Note that we can use `${run_date}` to specify an ingestion-time partitioned table as destination:

![BigQuery][6]

  [1]: https://cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.transferConfigs/list
  [2]: https://cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.dataSources/list
  [3]: https://cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/list
  [4]: https://cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create
  [5]: https://cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs#TransferConfig
  [6]: https://user-images.githubusercontent.com/29493411/67624676-0822d880-f834-11e9-8741-3e1721bfe9d4.png
  [7]: https://stackoverflow.com/a/55751108/6121516

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
