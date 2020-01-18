WITH
  authors AS (
  SELECT
    author,
    DATE_TRUNC(DATE(time_ts), MONTH) AS month
  FROM
    `bigquery-public-data.hacker_news.stories`
  WHERE
    author IS NOT NULL
  GROUP BY 1,2)

SELECT
  *,
  ROUND(100*SAFE_DIVIDE(num_returning_users,
      num_users),2) AS retention
FROM (
  SELECT
    a.month,
    COUNT(a.author) AS num_users,
    COUNTIF(b.month IS NOT NULL) AS num_returning_users
  FROM
    authors AS a
  LEFT OUTER JOIN
    authors AS b
  ON
    a.author = b.author
    AND a.month = DATE_ADD(b.month, INTERVAL 1 MONTH)
  GROUP BY 1
  ORDER BY 1
  LIMIT 100)
