#!/usr/bin/python

import random, sys


if len(sys.argv) < 2:
  NUM_LINES = 100000
else:
  NUM_LINES = sys.argv[1]

products = ['BigQuery', 'Dataflow', 'Dataproc', 'ML Engine', 'Composer', 'Dialogflow', 'Dataprep', 'Datalab', 'Vision API']

for i in range(int(NUM_LINES)):
  print(str(i) + ',' + random.choice(products))

