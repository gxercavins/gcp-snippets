package bigquery.samples;

import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.FieldValueList;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobId;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.JobStatistics;
import com.google.cloud.bigquery.JobStatistics.QueryStatistics;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.QueryResponse;
import com.google.cloud.bigquery.TableResult;
import java.text.SimpleDateFormat;
import java.util.concurrent.TimeUnit;
import java.util.UUID;

public class QueryJobStatistics {
  public static void main(String... args) throws Exception {
    BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();
    QueryJobConfiguration queryConfig =
        QueryJobConfiguration.newBuilder(
          "SELECT "
              + "CONCAT('https://stackoverflow.com/questions/', CAST(id as STRING)) as url, "
              + "view_count "
              + "FROM `bigquery-public-data.stackoverflow.posts_questions` "
              + "WHERE tags like '%google-bigquery%' "
              + "ORDER BY view_count DESC LIMIT 10")
            // Use standard SQL syntax for queries.
            // See: https://cloud.google.com/bigquery/sql-reference/
            .setUseLegacySql(false)
            .build();

    // Create a job ID so that we can safely retry.
    JobId jobId = JobId.of(UUID.randomUUID().toString());
    Job queryJob = bigquery.create(JobInfo.newBuilder(queryConfig).setJobId(jobId).build());

    // Wait for the query to complete.
    queryJob = queryJob.waitFor();

    // Check for errors
    if (queryJob == null) {
      throw new RuntimeException("Job no longer exists");
    } else if (queryJob.getStatus().getError() != null) {
      // You can also look at queryJob.getStatus().getExecutionErrors() for all
      // errors, not just the latest one.
      throw new RuntimeException(queryJob.getStatus().getError().toString());
    }

    // Get the results.
    TableResult result = queryJob.getQueryResults();
    System.out.println("\nQuery results:");

    // Print all pages of the results.
    for (FieldValueList row : result.iterateAll()) {
      String url = row.get("url").getStringValue();
      long viewCount = row.get("view_count").getLongValue();
      System.out.printf("url: %s views: %d%n", url, viewCount);
    }

    JobStatistics js = queryJob.getStatistics();
    QueryStatistics qs = queryJob.getStatistics();

    SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

    Long timeDiff = js.getEndTime() - js.getStartTime();
    String executionTime = String.format("%02d min, %02d sec", 
      TimeUnit.MILLISECONDS.toMinutes(timeDiff),
      TimeUnit.MILLISECONDS.toSeconds(timeDiff) - 
      TimeUnit.MINUTES.toSeconds(TimeUnit.MILLISECONDS.toMinutes(timeDiff)));

    System.out.println("\nQuery statistics:");

    System.out.printf("Creation time: %s%n", format.format(js.getCreationTime()));
    System.out.printf("Start time: %s%n", format.format(js.getStartTime()));
    System.out.printf("End time: %s%n", format.format(js.getEndTime()));
    System.out.printf("Duration: %s%n", executionTime);

    System.out.printf("Cache hit: %b%n", qs.getCacheHit());
    System.out.printf("Total Bytes Processed: %d%n", qs.getTotalBytesProcessed());
    System.out.printf("Total Bytes Billed: %d%n", qs.getTotalBytesBilled());
    System.out.printf("Total Slot ms: %d%n", qs.getTotalSlotMs());
  }
}