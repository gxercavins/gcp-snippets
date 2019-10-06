from oauth2client.client import GoogleCredentials
from googleapiclient import discovery

project_id="PROJECT_ID"
dataset_id="DATASET_NAME"
group_name="google-group-name@google.com"
role="READER"    

credentials = GoogleCredentials.get_application_default()
bq = discovery.build("bigquery", "v2", credentials=credentials)

response = bq.datasets().get(projectId=project_id, datasetId=dataset_id).execute()
response['access'].append({u'role': u'{}'.format(role), u'groupByEmail': u'{}'.format(group_name)})

bq.datasets().patch(projectId=project_id, datasetId=dataset_id, body=response).execute()