#standardSQL
-- Script to change origin and destination pages with dynamic regex.
DECLARE origin, destination, regex STRING;

SET origin = '/home';
SET destination = '/google+redesign/shop+by+brand/youtube';
SET regex = CONCAT('(', REPLACE(origin, '+', '\\+'), '.*?', REPLACE(destination, '+', '\\+'), ')');

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
