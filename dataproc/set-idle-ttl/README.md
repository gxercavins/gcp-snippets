# Set Idle Delete TTL

Dataproc makes it easy and fast to spin up new clusters so it's a common practice to rely on ephemeral clusters. Using [Workflows](https://cloud.google.com/dataproc/docs/concepts/workflows/overview) or [Airflow/Composer](https://cloud.google.com/composer/) we can automate cluster shutdown. Alternatively, we can set it up as part of the cluster metadata using [Scheduled Deletion](https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/scheduled-deletion).

## Example

As explained in [this answer](https://stackoverflow.com/a/54956557/6121516), the `idle_delete_ttl` option is part of the `LifecycleConfig` in the `v1beta2` version of the library. 

```python
from google.cloud import dataproc_v1beta2

client = dataproc_v1beta2.ClusterControllerClient()
```

The field is of type [`google.protobuf.Duration`](https://developers.google.com/protocol-buffers/docs/reference/csharp/class/google/protobuf/well-known-types/duration#duration) so we can define it as:

```python
from google.protobuf import duration_pb2

TTL_minutes = 10

max_idle = duration_pb2.Duration(seconds=60*TTL_minutes)
```

Note that 10 minutes is the minimum idle period that can be specified.

Then we can include it as part of the cluster configuration upon creation:

```python
cluster_data = {
    ...
    'config': {
        ...
        'lifecycle_config' : {
            'idle_delete_ttl' : max_idle
        }
    }
}

client.create_cluster(project_id, region, cluster_data)
```

Example code in the `create_cluster.py` file.

## Shutdown

Cluster should be automatically deleted after being idle for the specified amount of time.

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
