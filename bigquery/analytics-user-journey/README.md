# Google Analytics User Journey

We can export Google Analytics data to BigQuery in order to run complex analytic workloads. One interesting use case is to study how users get from page `A` to page `B` as in building a history of all possible paths and the corresponding frequency.

Originally written as an answer in [StackOverflow](https://stackoverflow.com/a/58891010/6121516).

## Example

The Google Analytics sample [dataset][1] has a cookbook with some examples such as  the *Sequence of hits* one [here][2]. We can modify it to use `STRING_AGG(hits.page.pagePath)` and build the desired `userJourney` sequence of hits.

To filter only the two desired pages we could use an approach such as the answers [here][3]. However, in our case we want to set one page as the `origin` and the other one as the `destination`. In addition, we can cut the path once the user has reached the target page so that both these journeys are analogous when `/page_13` is the origin and `/page_22` the destination:

`/page13` -> `/page_5` -> `/page_41` -> `/page_99` -> `/page_22`

`/page13` -> `/page_5` -> `/page_41` -> `/page_99` -> `/page_22` -> `page_37`

As a nice touch we can use the new [scripting][4] feature, currently in Beta, to be able to change the page pairs at the top of the script and build a dynamic regex. As an example to check journey between `/home` and `/google+redesign/shop+by+brand/youtube` using the available public data:

```sql
#standardSQL
-- Script to change origin and destination pages with dynamic regex.
DECLARE origin, destination, regex STRING;

SET origin = '/home';
SET destination = '/google+redesign/shop+by+brand/youtube';
SET regex = CONCAT('(', REPLACE(origin, '+', '\\+'), '.*?', REPLACE(destination, '+', '\\+'), ')');
```

This will build a regex such as `(/home).*?(/google\\+redesign/shop\\+by\\+brand/youtube)` to capture the first `origin` hit until we reach the `destination` page at least once.

And here's our main query where we inject the previously calculated `regex` to extract the matching paths from the concatenated session journey:

```sql
-- Run query
SELECT
  pagePath AS userJourney,
  COUNT(1) AS frequency
FROM (
  SELECT
    visitId,
    REGEXP_EXTRACT(STRING_AGG(hits.page.pagePath), regex) AS pagePath
  FROM
    `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits
  WHERE
    _TABLE_SUFFIX BETWEEN '20170701'
    AND '20170731'
    AND hits.type="PAGE"
  GROUP BY
    visitId)
WHERE
  pagePath IS NOT NULL
GROUP BY
  pagePath
ORDER BY
  COUNT(1) DESC
LIMIT
  10
```

Note that we filter out the ones where the regexp match is `NULL`.

Full script in the `script.sql` file. Upon running it, the following results are returned: 

[![enter image description here][5]][5]

To further optimize it we could select only the last occurrence of the `origin` but maybe we want to account for "back-tracking" in our results. For example, we might consider these two paths as different journeys:

`/page13` -> `/page_99` -> `/page_22`

`/page13` -> `/page_5` -> `/page_13` -> `/page_99` -> `/page_22`


  [1]: https://console.cloud.google.com/bigquery?p=bigquery-public-data&d=google_analytics_sample&t=ga_sessions_20170801&page=table
  [2]: https://support.google.com/analytics/answer/4419694
  [3]: https://stackoverflow.com/questions/41463338/page-combinations-in-bigquerys-google-analytics-data
  [4]: https://cloud.google.com/bigquery/docs/reference/standard-sql/scripting
  [5]: https://i.stack.imgur.com/MosPf.png

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
