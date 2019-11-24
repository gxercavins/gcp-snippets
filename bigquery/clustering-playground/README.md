# Clustering Playground

A quick test designed to do a little benchmark on clustered tables. Take into account that it was carried out in November 2018 so results and clustering block size might be different now.

## Example

The `generate_csv.py` script will be used to create some data. Each line will consist of a monotonically increasing index `id` and a `product`, which will be randomly selected from a list of 9 products. A uniform distribution is expected so we should see cost and performance benefits when clustering by the correct field. Script snippet:

```python
products = ['BigQuery', 'Dataflow', 'Dataproc', 'ML Engine', 'Composer', 'Dialogflow', 'Dataprep', 'Datalab', 'Vision API']

for i in range(int(NUM_LINES)):
  print(str(i) + ',' + random.choice(products))
```

and output example (N = 10):

```python
0,BigQuery
1,ML Engine
2,ML Engine
3,Dataflow
4,ML Engine
5,BigQuery
6,Dataproc
7,Dataproc
8,Composer
9,Datalab
```

Now we'll use the script to generate our `clustering.csv` data file:

```bash
python generate_csv.py 100000 > clustering.csv
```

As there is a random component, the resulting file will be different each time. Then we'll load the data into three different tables. One of them without clustering, another one clustered by `id` and a third one clustered by `product` (see `clustering.sh`):

```bash
bq mk clustering

bq load --schema id:INTEGER,product:STRING clustering.none clustering.csv
bq load --time_partitioning_type=DAY --schema id:INTEGER,product:STRING --clustering_fields id clustering.id clustering.csv
bq load --time_partitioning_type=DAY --schema id:INTEGER,product:STRING --clustering_fields product clustering.product clustering.csv
```

So now we run the following query, filtering only certaind IDs (`id < 1000`), in all three tables:

```sql
SELECT
  *
FROM
  clustering.id
WHERE
  id < 1000
LIMIT
  1000
```

With the following results:

* **none**: Query complete (2.4s elapsed, 1.76 MB processed)
* **id**: Query complete (2.0s elapsed, 1.76 MB processed)
* **product**: Query complete (2.4s elapsed, 1.76 MB processed)

(note that timing will vary across different executions but all queries seem to trigger a full table scan)

According to the `WHERE` clause we are only retrieving 1000 rows out of 100000 so we would expect to see significant savings in the `id` table. Is that right? Yes, in theory. In practice, data size is very small (a full table scan is 1.76 MB) so all IDs seem to be collocated into the same clustering block.

In fact, the same happens when we filter on product:

```sql
SELECT
  *
FROM
  clustering.product
WHERE
  product = 'Dataproc'
LIMIT
  1000
```

Corresponding results:

* **none**: Query complete (2.1s elapsed, 1.76 MB processed)
* **id**: Query complete (1.7s elapsed, 1.76 MB processed)
* **product**: Query complete (2.4s elapsed, 1.76 MB processed)

To test our theory we can just generate more data (100x) and repeat the process:

```bash
python generate_csv.py 10000000 > clustering.csv
...
```

Which gives us the following results when we filter by `id`:

* **none**: Query complete (1.9s elapsed, 176 MB processed)
* **id**: Query complete (2.1s elapsed, 38.1 MB processed)

or `product`:

* **none**: Query complete (3.0s elapsed, 176 MB processed)
* **product**: Query complete (2.2s elapsed, 43.9 MB processed)

Now we can start to see clustering benefits, which will be better with larger amounts of data. Again, note that there are no guarantees regarding clustering block size as it is subject to change without notice.

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
