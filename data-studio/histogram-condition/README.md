# Histogram

Issue statement is given in StackOverflow [question](https://stackoverflow.com/questions/58678855/calculating-and-displaying-customer-lifetime-value-histogram-with-bigquery-and-d). Main idea is to construct a report containing a customer lifetime value histogram. Data source is a BigQuery table containing three fields: `customer_id, product_id, amount`. The aforementioned value is calculated as the sum of `amount` for any given customer. Customers would be segmented according to that and fall into different histogram bins.

The main difficulty appears when we want to filter customers who purchased a particular product. It would be easy to add a data filter but that would only include the amount associated to that `product_id`, discarding expenses from other products.

## Example

We can apply a neat trick to achieve this chart. The main idea is to have two data sources from the same table: one contains `customer_id` and `product_id` so that we can filter it while the other one contains `customer_id` and the already calculated `amount_bucket` field. This way we can join it (blend data) on `customer_id` and filter according to `product_id` which won't change the `amount_bucket` calculations.

First of all we create the data in BigQuery using the new [scripting](https://cloud.google.com/bigquery/docs/reference/standard-sql/scripting) feature:

```sql
CREATE OR REPLACE TABLE data_studio.histogram
(
  customer_id STRING,
  product_id STRING,
  amount INT64
);

INSERT INTO data_studio.histogram (customer_id, product_id, amount)
VALUES ('John', 'Game', 60),
       ('John', 'TV', 800),
       ('John', 'Console', 300),
       ('Paul', 'Sofa', 1200),
       ('George', 'TV', 750),
       ('Ringo', 'Movie', 20),
       ('Ringo', 'Console', 250)
;
```

First we can connect directly to the BigQuery table and start visualizing some fields. Data source is called `histogram` (this will help to follow through this explanation):

[![enter image description here][1]][1]

We add our second data source (`BigQuery`) using a custom query where we already calculate the lifetime value category:

```sql
SELECT
  customer_id,
  CASE
    WHEN SUM(amount) < 500 THEN '0-500'
    WHEN SUM(amount) < 1000 THEN '500-1000'
    WHEN SUM(amount) < 1500 THEN '1000-1500'
    ELSE '1500+'
END
  AS amount_bucket
FROM
  data_studio.histogram
GROUP BY
  customer_id
```

With only the latter we can already do a basic histogram with the following configuration:

[![enter image description here][2]][2]

Dimension is `amount_bucket`, metric is `Record count`. Note that `bucket_order` is a calculated field to sort the categories in the graph (otherwise lexicographically '1000-1500' comes before '500-1000'):

```sql
CASE 
  WHEN amount_bucket = '0-500' THEN 0
  WHEN amount_bucket = '500-1000' THEN 1
  WHEN amount_bucket = '1000-1500' THEN 2
  ELSE 3
END
```

Now we add the `product_id` filter on top and a new chart with the following configuration:

[![enter image description here][3]][3]

Note that metric is CTD (Count Distinct) of `customer_id` and the `Blended data` data source is implemented as:

[![enter image description here][4]][4]

To verify the desired behavior we can filter by `TV` so only `George` and `John` appear. The other products are still counted for the total amount calculation as expected:

[![enter image description here][5]][5]

According on your use case you might need to tweak it (for example, using the filter on the blended data).

  [1]: https://i.stack.imgur.com/dO9yU.png
  [2]: https://i.stack.imgur.com/LJF2g.png
  [3]: https://i.stack.imgur.com/4eDfT.png
  [4]: https://i.stack.imgur.com/ceb44.png
  [5]: https://i.stack.imgur.com/Pkpkx.png

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
