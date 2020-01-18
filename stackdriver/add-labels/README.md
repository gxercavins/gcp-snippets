# Add labels to custom metrics

Let's imagine that we have set up application logging in our GAE app with a custom payload. How can we filter by a specific field in Stackdriver Monitoring's metrics explorer? how can we set up the corresponding alerts? Originally written as a StackOverflow [answer](https://stackoverflow.com/a/59760010/6121516). 

## Example

First of all, we can create our own [user-defined metrics][1] in Stackdriver Logging. This way, we can capture all logs that match a target filter and expose the payload fields that we want as metric labels.

We navigate to `Stackdriver Logging` -> `Logs-based Metrics` -> `Create Metric` and select a filter for a GAE application:

```
resource.type="gae_app" 
logName=("projects/REDACTED/logs/appengine.googleapis.com%2Fstdout" 
OR "projects/REDACTED/logs/appengine.googleapis.com%2Fstderr" 
OR "projects/REDACTED/logs/appengine.googleapis.com%2Fnginx.request" 
OR "projects/REDACTED/logs/appengine.googleapis.com%2Frequest_log") 
resource.labels.module_id="image-demo"
httpRequest.requestMethod="GET"
```

In my case requests contain a generic `jsonPayload` such as (but you can have your own fields as per the implemented application logging):

```
jsonPayload: {
  appLatencySeconds: "0.000"   
  latencySeconds: "0.001"   
  trace: "4ff777572199f23f4fc97388e75c0acc"   
 }
```

On the metric editor (right panel) under `Labels` there is a `Field name` dropdown selector that includes our `jsonPayload` fields: 

[![enter image description here][2]][2]

As an example, we select `jsonPayload.trace` and now we can filter our custom metric by **trace** label in the Metrics Explorer:

[![enter image description here][3]][3]

Note that we can create a Stackdriver Monitoring alert directly from our list of user-defined metrics (`Create alert from metric`):

[![enter image description here][4]][4]


  [1]: https://cloud.google.com/logging/docs/logs-based-metrics/
  [2]: https://i.stack.imgur.com/FNfC7.png
  [3]: https://i.stack.imgur.com/gDTpj.png
  [4]: https://i.stack.imgur.com/uBQm2.png

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
