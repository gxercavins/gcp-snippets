# Calculate Returning Users

We have a record of all transactions including user ID and date. We want to calculate the ratio of repeated users in consecutive months. Full problem statement in [this StackOverflow question](https://stackoverflow.com/questions/59702176/how-to-count-monthly-retention-user-in-bigquery/59703415).

## Example

One possible way to do so is using a self-join with the same table and a 1-month lag/delay. That way, we match user&month combinations with user&previous-month to see if it qualifies as a returning user. Throughout this example, we'll query the 2M row public table `bigquery-public-data.hacker_news.stories`. Let's inspect the join for a single user:

[![enter image description here][1]][1]

Noteworthy, `prev_month` is **null** (we used `LEFT OUTER JOIN`) for **2014-02-01** as the user was **not** active during **2014-01-01**. We are joining on author and lagged months with:

```sql
FROM authors AS a 
LEFT OUTER JOIN authors AS b
ON a.author = b.author
AND a.month = DATE_ADD(b.month, INTERVAL 1 MONTH)
```

Then we count a user as repeating if the previous month was **not null**:

```sql
COUNT(a.author) AS num_users,
COUNTIF(b.month IS NOT NULL) AS num_returning_users
```

We do not use `DISTINCT` here as we already grouped by author and month combinations when defining `orders` as CTE. We might need to take this into account for other examples.

Full query in `join.sql` file:

```sql
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
```

and results snippet:

[![enter image description here][2]][2]

which are correct results, i.e. for `2007-03-01`:

[![enter image description here][3]][3]

Performance is not too fancy due to the self join. However, in this case we are selecting only the fields needed for the aggregations so the amount of scanned data is low and execution time not too high (\~5s). 

An alternative is to use `EXISTS()` inside `COUNTIF()` to replace the join but it takes longer for me (\~7s). New query in `exists.sql`.


  [1]: https://i.stack.imgur.com/xrsyV.png
  [2]: https://i.stack.imgur.com/VsKzS.png
  [3]: https://i.stack.imgur.com/hlisT.png

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
