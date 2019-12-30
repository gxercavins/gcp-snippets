# Histogram

Issue statement is given in StackOverflow [question](https://stackoverflow.com/questions/59510055/bucketizing-record-counts-by-the-hour-of-this-day-only-and-showing-hours-in-axis/). Briefly, we have timestamped events and we want to bucketize into hours to build a histogram. The challenge here is that some hours might contain no events at all but we still want to have a 24-hour chart.

## Example

We can rely on an `OUTER JOIN` with all possible dimension values (0-23h) to solve this issue.

To frame the problem we will use a BigQuery public dataset: `bigquery-public-data.london_bicycles.cycle_hire` where `start_date` is a `TIMESTAMP` field containing the time when each ride started. To simulate the problem statement, we will filter out all trips that started before 7 AM with the following query:

```sql
SELECT
  *
FROM
  `bigquery-public-data.london_bicycles.cycle_hire`
WHERE
  EXTRACT(HOUR FROM start_date) > 6
```

Therefore, we can replicate the problem, when creating a data source with the previous custom query, as hours without data are not displayed:

[![enter image description here][1]][1]


---

## Blending with range data

The first and quick fix would be to create a data source that contains all possible dimension values. This could be done in a spreadsheet or, for example, with an additional (0-Bytes scanned) custom query:

```sql
SELECT
  *
FROM
  UNNEST(GENERATE_ARRAY(0, 23)) AS hour
```

and now we blend the data so that the hour array is on the left side (Data Studio uses `LEFT OUTER JOIN`) and join with `HOUR(start_date)` from the `cycle_hire` table:

[![enter image description here][2]][2]


With this approach we get the desired histogram (be sure to change the number of bars up to 24 in the `STYLE` tab and sort by `hour` ascending in the `DATA` one):

[![enter image description here][3]][3]

---

## Aggregate in BigQuery

Another alternative would be to leverage BigQuery to run the calculations for the hourly buckets. For example, in this case, we would generate the hour array, outer join it with the aggregated data and substitute `NULL` for 0:

```sql
WITH
hours AS (
  SELECT
    *
  FROM
    UNNEST(GENERATE_ARRAY(0, 23)) AS hour),
bike_rides AS (
  SELECT
    EXTRACT(HOUR FROM start_date) AS hour,
    COUNT(*) AS total
  FROM
    `bigquery-public-data.london_bicycles.cycle_hire`
  WHERE
    EXTRACT(HOUR FROM start_date) > 6
  GROUP BY
    hour )

SELECT
  hour,
  IF(total IS NULL,0,total) AS total
FROM
  bike_rides
RIGHT OUTER JOIN
  hours
USING
  (hour)
```

which gives the same result, as expected.

  [1]: https://i.stack.imgur.com/n2hk9.png
  [2]: https://i.stack.imgur.com/TIEzn.png
  [3]: https://i.stack.imgur.com/qQPIs.png

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
