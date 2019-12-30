from datetime import datetime  
from datetime import timedelta 

from google.cloud import bigquery

project_id = "PROJECT_ID"
table_name = "test.expiration"

client = bigquery.Client(project=project_id)

# get the initial expiration date
table_info = client.get_table(table_name)
print("Initial expiration: {}".format(table_info.expires))

# update with the new desired field
table_info.expires = datetime.now() + timedelta(days=1)
new_table_info = client.update_table(
    table_info, ['expires'])

# check results
print("Final expiration: {}".format(new_table_info.expires))
