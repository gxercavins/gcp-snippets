#!/bin/bash

# parameter(s)
location=us

authToken="$(gcloud auth print-access-token)"
projectId=$(gcloud config get-value project)

# API call
scheduled_queries=$(curl  -H "Authorization: Bearer $authToken" \
  https://bigquerydatatransfer.googleapis.com/v1/projects/$projectId/locations/$location/transferConfigs?dataSourceIds=scheduled_query)

# pretty print results
echo $scheduled_queries | python -m json.tool
