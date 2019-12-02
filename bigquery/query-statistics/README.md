# Query Statistics

How to retrieve statistics for our queries using the Java Client Library. Extended use case from a [StackOverflow answer](https://stackoverflow.com/a/57150360/6121516).

## Example

Note that the example is constructed over the official sample [here](https://github.com/GoogleCloudPlatform/java-docs-samples/blob/master/bigquery/cloud-client/src/main/java/com/example/bigquery/SimpleApp.java) which plays with StackOverflow data. Code is in `QueryJobStatistics.java` and can be run with the provided script `run.sh` (fill in `PROJECT_ID`) or with: 

```bash
mvn compile -e exec:java \
 -Dexec.mainClass=bigquery.samples.QueryJobStatistics
```

The `JobStatistics` class has different nested classes as can be seen [here](https://googleapis.dev/java/google-cloud-clients/latest/com/google/cloud/bigquery/JobStatistics.html) (five as of now due to the new scripting feature). `QueryStatistics` is one of them and provides query-specific statistics such as cache hit or miss with the [`getCacheHit()`](https://googleapis.dev/java/google-cloud-clients/latest/com/google/cloud/bigquery/JobStatistics.QueryStatistics.html#getCacheHit--) method.

We can simply get both job and query statistics by specifying the class:

```java
JobStatistics js = queryJob.getStatistics();
QueryStatistics qs = queryJob.getStatistics();
```

Then we can access the necessary fields from either `js` or `qs` according to the available methods. For example:

```java
js.getCreationTime()
qs.getTotalBytesProcessed()
```

The following statistics were printed in my case:

```bash
Query statistics:
Creation time: 2019-12-02 15:19:04
Start time: 2019-12-02 15:19:04
End time: 2019-12-02 15:19:05
Duration: 00 min, 00 sec
Cache hit: false
Total Bytes Processed: 746706557
Total Bytes Billed: 747634688
Total Slot ms: 9147
```

Kudos to a couple StackOverflow answers that helped with the date formats: [1](https://stackoverflow.com/a/6782571/6121516) and [2](https://stackoverflow.com/a/625624/6121516).

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
