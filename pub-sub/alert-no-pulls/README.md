# Alert - no pulls

Best practices to set up a Stackdriver Monitoring Alert that notifies us when there are no subscribers pulling messages for a particular Pub/Sub subscription. Originally written as a StackOverflow [answer](https://stackoverflow.com/a/57521381/6121516). 

## Example

We want to be alerted when there are no pull message operations so we can use the [`subscription/pull_request_count`](https://cloud.google.com/monitoring/api/metrics_gcp#gcp-pubsub) metric. However, after some time without pull operations, the metric can be dropped instead of reporting 0 pulls. To cover for this situation we can add another condition: alert if `is absent for 3 minutes` OR `is below 1 for 1 minute`:

[![enter image description here][1]][1]

However, the problem here is that the UI filters out all unused resources and metrics (for the past 6 weeks). While this greatly eases out setting alerts and browsing through metrics for running operations, it requires a different approach to create new alerts before a system is in production. The easiest solution would be to make a dummy subscription and pull messages so that the metric appears and we can select it in the UI. 

Another approach relies on the Stackdriver Monitoring API to set them up. Keep in mind that the alerting policies API is in [Beta](https://cloud.google.com/monitoring/api/v3/#alerting-policies) so it's subject to non-backwards-compatible changes.

To build up our request the recommendation is to start by inspecting an already existing policy with [`projects.alertPolicies/list`](https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.alertPolicies/list) and see how the [`AlertPolicy`](https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.alertPolicies#AlertPolicy) body is constructed.

Then we can set some initial variables:

```bash
TOKEN="$(gcloud auth print-access-token)"
PROJECT=$(gcloud config get-value project)
SUBSCRIPTION=PUBSUB_SUBSCRIPTION_ID
CHANNEL=NOTIFICATION_CHANNEL_ID
```

In this case we am monitoring only a specific Pub/Sub subscription throughout the example and we already have a notification channel (email). If you already have an existing policy you can get the notification channel ID [here](https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.notificationChannels/list).

With `projects.alertPolicies/create` we can create the new alert policy:

```bash
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://monitoring.googleapis.com/v3/projects/$PROJECT/alertPolicies" \
  -d @alert.json
```

where `alert.json` is also included in this folder. The `PROJECT`, `SUBSCRIPTION` and `CHANNEL` variables should be replaced accordingly. Briefly, we don't need to pass policy or condition IDs as those will be populated by the API.

We use `OR` as the combiner (*policy violates when ANY condition is met*) to trigger the alert when the metric is either absent (`conditionAbsent`) or below 1 (`conditionThreshold`):

```js
"combiner": "OR",
"conditions": [
  {
    "conditionAbsent": {
      "filter": "metric.type=\"pubsub.googleapis.com/subscription/pull_request_count\" resource.type=\"pubsub_subscription\" resource.label.\"project_id\"=\"$PROJECT\" resource.label.\"subscription_id\"=\"$SUBSCRIPTION\"",
      "duration": "180s",
      "trigger": {
        "count": 1
      },
      "aggregations": [
        {
          "alignmentPeriod": "60s",
          "perSeriesAligner": "ALIGN_RATE"
        }
      ]
    },
    "displayName": "Pull requests absent for $PROJECT, $SUBSCRIPTION"
  },
  {
    "conditionThreshold": {
      "filter": "metric.type=\"pubsub.googleapis.com/subscription/pull_request_count\" resource.type=\"pubsub_subscription\" resource.label.\"project_id\"=\"$PROJECT\" resource.label.\"subscription_id\"=\"$SUBSCRIPTION\"",
      "comparison": "COMPARISON_LT",
      "thresholdValue": 1,
      "duration": "60s",
      "trigger": {
        "count": 1
      },
      "aggregations": [
        {
          "alignmentPeriod": "60s",
          "perSeriesAligner": "ALIGN_RATE"
        }
      ]
    },
    "displayName": "Pull requests are 0 for $PROJECT, $SUBSCRIPTION"
  }
]
```

We can modify parameters to better suit our use case: display names, descriptions, etc.

```js
"displayName": "no-pull-alert",
...
"documentation": {
  "content": "**ALERT**\n\nNo pull message operations",
  "mimeType": "text/markdown"
},
```

Finally, we set the correct notification channel and enable the alert:

```js
"notificationChannels": [
  "projects/$PROJECT/notificationChannels/$CHANNEL"
],
"enabled": true
```

[![enter image description here][2]][2]


  [1]: https://i.stack.imgur.com/sBSpc.png
  [2]: https://i.stack.imgur.com/FGX7D.png

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
