# Create a Dataproc Cluster

Quick example to create a cluster using Java and the Dataproc API.

## Quickstart

Set the variables in `src/main/java/com/example/DataprocExample.java` and run:

```java
mvn compile exec:java -Dexec.mainClass=com.example.DataprocExample
```

## Example

All code can be found in the previously mentioned `DataprocExample.java` file. Briefly, the API documentation is available [here](https://developers.google.com/resources/api-libraries/documentation/dataproc/v1/java/latest/).

First, the build the request with [`Dataproc.Builder`](https://developers.google.com/resources/api-libraries/documentation/dataproc/v1/java/latest/com/google/api/services/dataproc/Dataproc.Builder.html#Builder-com.google.api.client.http.HttpTransport-com.google.api.client.json.JsonFactory-com.google.api.client.http.HttpRequestInitializer-):

```java
Dataproc dataproc = new Dataproc.Builder(httpTransport, jsonFactory, credentials)
    .setApplicationName("Google-ClustersCreateExample/1.0").build();
```

We initialize [`GceClusterConfig`](https://developers.google.com/resources/api-libraries/documentation/dataproc/v1/java/latest/com/google/api/services/dataproc/model/GceClusterConfig.html) with the desired zone:

```java
GceClusterConfig computeEngineConfig = new GceClusterConfig();
computeEngineConfig.setZoneUri(String.format(ZONE_URI_FORMAT, PROJECT_ID, ZONE));
```

We use [`InstanceGroupConfig`](https://developers.google.com/resources/api-libraries/documentation/dataproc/v1/java/latest/com/google/api/services/dataproc/model/InstanceGroupConfig.html) to configure the cluster resources. In this case we'll use the same machine type for the master and the two workers:

```java
String machineType = String.format(MACHINE_TYPE_URI_FORMAT,PROJECT_ID, ZONE, "n1-standard-1");
InstanceGroupConfig masterConfig = new InstanceGroupConfig();
masterConfig.setMachineTypeUri(machineType)
            .setNumInstances(1);
InstanceGroupConfig workerConfig = new InstanceGroupConfig();
workerConfig.setMachineTypeUri(machineType)
            .setNumInstances(2);
```

Then, we put everything together to define our cluster:

```java
ClusterConfig clusterConfig = new ClusterConfig();
clusterConfig.setMasterConfig(masterConfig);
clusterConfig.setWorkerConfig(workerConfig);
clusterConfig.setGceClusterConfig(computeEngineConfig);

Cluster cluster = new Cluster();
cluster.setProjectId(PROJECT_ID);
cluster.setConfig(clusterConfig);
cluster.setClusterName(CLUSTER_NAME);
```

and send the actual API request to create it:

```java
dataproc.projects().regions().clusters()
        .create(PROJECT_ID, REGION, cluster)
        .execute();
```
## Shutdown

Delete the Dataproc cluster to avoid incurring costs.

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
