export PROJECT=PROJECT_ID

mvn compile -e exec:java \
 -Dexec.mainClass=bigquery.samples.QueryJobStatistics \
      -Dexec.args="--project=$PROJECT"

