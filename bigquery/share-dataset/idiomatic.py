from google.cloud import bigquery

project_id = "PROJECT_ID"
dataset_id = "DATASET_NAME"
group_name= "google-group-name@google.com"
role = "READER"

client = bigquery.Client(project=project_id)

dataset_info = client.get_dataset(client.dataset(dataset_id))

access_entries = dataset_info.access_entries
access_entries.append(
        bigquery.AccessEntry(role, "groupByEmail", group_name)
)

dataset_info.access_entries = access_entries
dataset_info = client.update_dataset(
    dataset_info, ['access_entries']) 