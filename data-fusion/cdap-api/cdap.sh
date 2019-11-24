#!/bin/bash

# set script variables
PROJECT=$(gcloud config get-value project)
TOKEN=$(gcloud auth print-access-token)
LOCATION=europe-west4
PIPELINE=BQ-to-GCS

# get instance endpoint
curl -H "Authorization: Bearer $TOKEN" \
    https://datafusion.googleapis.com/v1beta1/projects/$PROJECT/locations/$LOCATION/instances

# get run history for pipeline
curl -H "Authorization: Bearer $TOKEN" \
        https://data-fusion-1-$PROJECT-dot-euw4.datafusion.googleusercontent.com/api/v3/namespaces/default/apps/$PIPELINE/workflows/DataPipelineWorkflow/runs