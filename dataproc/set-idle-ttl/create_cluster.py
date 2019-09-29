from google.cloud import dataproc_v1beta2
from google.protobuf import duration_pb2


project_id = "PROJECT_ID"
cluster_name = "test-ttl"
zone = "us-central1-a"
region = "global"
TTL_minutes = 10

print('Creating cluster...')

client = dataproc_v1beta2.ClusterControllerClient()

max_idle = duration_pb2.Duration(seconds=60*TTL_minutes)
                    
zone_uri = \
    'https://www.googleapis.com/compute/v1/projects/{}/zones/{}'.format(
        project_id, zone)

cluster_data = {
    'project_id': project_id,
    'cluster_name': cluster_name,
    'config': {
        'gce_cluster_config': {
            'zone_uri': zone_uri,
            'service_account_scopes': [
                'https://www.googleapis.com/auth/cloud-platform'
            ]
        },
        'master_config': {
            'num_instances': 1,
            'machine_type_uri': 'n1-standard-1'
        },
        'worker_config': {
            'num_instances': 2,
            'machine_type_uri': 'n1-standard-1'
        },
        'lifecycle_config' : {
            'idle_delete_ttl' : max_idle
        }
    }
}
    
response = client.create_cluster(project_id, region, cluster_data)
result = response.result()

print(result)