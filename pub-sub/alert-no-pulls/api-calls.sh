#!/bin/bash

# set script variables
TOKEN="$(gcloud auth print-access-token)"
PROJECT=$(gcloud config get-value project)
SUBSCRIPTION=PUBSUB_SUBSCRIPTION_ID
CHANNEL=NOTIFICATION_CHANNEL_ID

# create new alert policy
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://monitoring.googleapis.com/v3/projects/$PROJECT/alertPolicies" \
  -d @alert.json
