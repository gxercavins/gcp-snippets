package com.example;

import java.io.IOException;

import com.google.api.client.googleapis.auth.oauth2.GoogleCredential;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.HttpRequest;
import com.google.api.client.http.HttpRequestInitializer;
import com.google.api.client.http.HttpTransport;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.services.dataproc.Dataproc;
import com.google.api.services.dataproc.model.Cluster;
import com.google.api.services.dataproc.model.ClusterConfig;
import com.google.api.services.dataproc.model.InstanceGroupConfig;
import com.google.api.services.dataproc.model.GceClusterConfig;


/** Example of creating a Dataproc cluster. */
public class DataprocExample {

  // parameters
  private static final String CLUSTER_NAME = "cluster-name";
  private static final String PROJECT_ID = "project-id";
  private static final String REGION = "region-name";
  private static final String ZONE = "zone-name";

  private static final String ZONE_URI_FORMAT = "https://www.googleapis.com/compute/v1/projects/%s/zones/%s"; 
  private static final String MACHINE_TYPE_URI_FORMAT = "https://www.googleapis.com/compute/v1/projects/%s/zones/%s/machineTypes/%s";


  public static void main(String[] args) throws Exception {
    // auth, init
    HttpTransport httpTransport = GoogleNetHttpTransport.newTrustedTransport();
    JsonFactory jsonFactory = new JacksonFactory();
    GoogleCredential credentials = GoogleCredential.getApplicationDefault();

    Dataproc dataproc = new Dataproc.Builder(httpTransport, jsonFactory, credentials)
        .setApplicationName("Google-ClustersCreateExample/1.0").build();

    // GCE config
    GceClusterConfig computeEngineConfig = new GceClusterConfig();
    computeEngineConfig.setZoneUri(String.format(ZONE_URI_FORMAT, PROJECT_ID, ZONE));

    // Instance Group config
    String machineType = String.format(MACHINE_TYPE_URI_FORMAT,PROJECT_ID, ZONE, "n1-standard-1");
    InstanceGroupConfig masterConfig = new InstanceGroupConfig();
    masterConfig.setMachineTypeUri(machineType)
	            .setNumInstances(1);
    InstanceGroupConfig workerConfig = new InstanceGroupConfig();
    workerConfig.setMachineTypeUri(machineType)
	            .setNumInstances(2);

    // Cluster config
    ClusterConfig clusterConfig = new ClusterConfig();
    clusterConfig.setMasterConfig(masterConfig);
    clusterConfig.setWorkerConfig(workerConfig);
    clusterConfig.setGceClusterConfig(computeEngineConfig);

    Cluster cluster = new Cluster();
    cluster.setProjectId(PROJECT_ID);
    cluster.setConfig(clusterConfig);
    cluster.setClusterName(CLUSTER_NAME);

    // create cluster
    Dataproc.Projects.Regions.Clusters.Create createOp = null;

    createOp = dataproc.projects().regions().clusters()
                       .create(PROJECT_ID, REGION, cluster);

    createOp.execute();

    System.out.println("done");
  }

}
