from google.cloud import dataproc_v1beta2

project_id = 'PROJECT_ID'
cluster_name = 'CLUSTER_NAME'
region = 'europe-west4'

client = dataproc_v1beta2.ClusterControllerClient(
                       client_options={
                            'api_endpoint': '{}-dataproc.googleapis.com:443'.format(region)
                        }
                    )

response = client.get_cluster(project_id, region, cluster_name)
print(response.config.endpoint_config)