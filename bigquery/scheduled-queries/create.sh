#!/bin/bash

# parameter(s)
location=us

authToken="$(gcloud auth print-access-token)"
projectId=$(gcloud config get-value project)

# API call
scheduled_query=$(curl  -X POST -H "Authorization: Bearer $authToken" \
  -H "Content-Type: application/json" -d @request.json \
  https://bigquerydatatransfer.googleapis.com/v1/projects/$projectId/locations/$location/transferConfigs)

# pretty print results
echo $scheduled_query | python -m json.tool
