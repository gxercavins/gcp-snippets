# Web Interfaces

How to use the Python Client Library to retrieve cluster endpoints such as the Jupyter gateway URL that we can see in the *Web Interfaces* section of the UI. Originally written as a [Stackoverflow answer](https://stackoverflow.com/a/59614666/6121516).

## Example

We can follow [the documentation](https://cloud.google.com/dataproc/docs/tutorials/jupyter-notebook) to setup Jupyter access by enabling Component Gateway and then access the Web Interfaces as described [here](https://cloud.google.com/dataproc/docs/concepts/accessing/dataproc-gateways#viewing_and_accessing_component_gateway_urls). The trick is that this is included in the API response for the [`v1beta2`](https://cloud.google.com/dataproc/docs/reference/rest/v1beta2/ClusterConfig#EndpointConfig) version. We can access the endpoints with `response.config.endpoint_config`:

```python
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
```

As an example, in my case I get:

```js
http_ports {
  key: "HDFS NameNode"
  value: "https://REDACTED-dot-europe-west4.dataproc.googleusercontent.com/hdfs/dfshealth.html"
}
http_ports {
  key: "Jupyter"
  value: "https://REDACTED-dot-europe-west4.dataproc.googleusercontent.com/jupyter/"
}
http_ports {
  key: "JupyterLab"
  value: "https://REDACTED-dot-europe-west4.dataproc.googleusercontent.com/jupyter/lab/"
}
http_ports {
  key: "MapReduce Job History"
  value: "https://REDACTED-dot-europe-west4.dataproc.googleusercontent.com/jobhistory/"
}
http_ports {
  key: "Spark History Server"
  value: "https://REDACTED-dot-europe-west4.dataproc.googleusercontent.com/sparkhistory/"
}
http_ports {
  key: "Tez"
  value: "https://REDACTED-dot-europe-west4.dataproc.googleusercontent.com/apphistory/tez-ui/"
}
http_ports {
  key: "YARN Application Timeline"
  value: "https://REDACTED-dot-europe-west4.dataproc.googleusercontent.com/apphistory/"
}
http_ports {
  key: "YARN ResourceManager"
  value: "https://REDACTED-dot-europe-west4.dataproc.googleusercontent.com/yarn/"
}
enable_http_port_access: true
```

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
