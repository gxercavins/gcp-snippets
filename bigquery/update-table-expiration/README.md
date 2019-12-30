# Update Table Expiration

Example, using Python libraries, to call the BigQuery API to patch a table and modify its expiration/retention date. Originally written as an answer to this [StackOverflow question](https://stackoverflow.com/questions/59431486/how-to-set-existing-table-expiration-via-python-client-library-for-google-bigque/).

## Example

`client.Client` has an `update_table` method: [api reference](https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.client.Client.html#google.cloud.bigquery.client.Client.update_table) and [github](https://github.com/googleapis/google-cloud-python/blob/bigquery-1.23.1/bigquery/google/cloud/bigquery/client.py#L711).

We can retrieve the table settings with [`get_table`](https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.client.Client.html#google.cloud.bigquery.client.Client.get_table) to get the `table.Table` [representation](https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.table.Table.html#google.cloud.bigquery.table.Table). Then, we can modify the `expires` attribute with the new desired date and update it with `update_table` (note that we specify the list of fields to update with `['expires']`):

```python
table_info = client.get_table(table_name)

table_info.expires = datetime.now() + timedelta(days=1)
new_table_info = client.update_table(
    table_info, ['expires'])
```

To test this, we can create an empty table without expiration:

```bash
$ bq mk -t test.expiration
Table 'PROJECT_ID:test.expiration' successfully created.
```

and run the script (library version is `google-cloud-bigquery==1.23.1`):

```python
Initial expiration: None
Final expiration: 2019-12-22 08:47:52.507000+00:00
```

Full code in `expiration.py` file.


## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
