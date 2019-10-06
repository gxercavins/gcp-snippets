# Share Datasets with Python

A couple examples, using two different official Python libraries, to call the BigQuery API and share datasets programmatically. Originally written as an answer to this [StackOverflow question](https://stackoverflow.com/questions/54249049/bigquery-google-cloud-how-to-share-dataset-with-other-users-using-python/).

## Example

First, we can use the Python Client Library and adapt the sample [here][1] but adding a [`get_dataset`][2] call to get the current ACL policy for already existing datasets:

```python 
dataset_info = client.get_dataset(client.dataset(dataset_id))

access_entries = dataset_info.access_entries
access_entries.append(
        bigquery.AccessEntry(role, "groupByEmail", group_name)
)

dataset_info.access_entries = access_entries
dataset_info = client.update_dataset(
    dataset_info, ['access_entries']) 
```

Version used is `google-cloud-bigquery==1.8.1`. Code available in `idiomatic.py`.

If we favor the Google Python API Client we can use the [get][3] and [patch][4] methods. First, we retrieve the existing dataset ACL, add the group as `READER` to the response and patch the dataset metadata:

```python 
response = bq.datasets().get(projectId=project_id, datasetId=dataset_id).execute()
response['access'].append({u'role': u'{}'.format(role), u'groupByEmail': u'{}'.format(group_name)})

bq.datasets().patch(projectId=project_id, datasetId=dataset_id, body=response).execute()
```

Tested with `google-api-python-client==1.7.7` and code in `googleapis.py`.

  [1]: https://cloud.google.com/bigquery/docs/share-access-views#assign_access_controls_to_the_dataset_containing_the_view
  [2]: https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.client.Client.html#google.cloud.bigquery.client.Client.get_dataset
  [3]: https://developers.google.com/resources/api-libraries/documentation/bigquery/v2/python/latest/bigquery_v2.datasets.html#get
  [4]: https://developers.google.com/resources/api-libraries/documentation/bigquery/v2/python/latest/bigquery_v2.datasets.html#patch

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
