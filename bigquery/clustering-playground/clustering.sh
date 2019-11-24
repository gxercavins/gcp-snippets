#!/bin/bash

bq mk clustering

bq load --schema id:INTEGER,product:STRING clustering.none clustering.csv
bq load --time_partitioning_type=DAY --schema id:INTEGER,product:STRING --clustering_fields id clustering.id clustering.csv
bq load --time_partitioning_type=DAY --schema id:INTEGER,product:STRING --clustering_fields product clustering.product clustering.csv

