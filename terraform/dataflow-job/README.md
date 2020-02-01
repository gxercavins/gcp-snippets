# Dataflow Job

How to execute a Dataflow template using Terraform and the Google Cloud Platform Provider. Originally written as a StackOverflow [answer](https://stackoverflow.com/a/59931467/6121516).

## Example

Below code was tested with the following setup:

```bash
$ terraform --version
Terraform v0.12.20
+ provider.google v3.5.0
```

and the Google-provided [word count][1] Dataflow template as `inputFile`. Content of `main.tf` file is:

```lang-yaml
variable "project_id" {
  type        = string
  description = "GCP Project ID."
}
variable "gcs_location" {
  type        = string
  description = "GCS bucket name (no gs:// prefix)."
}

provider "google" {
  project = var.project_id
  region  = "us-central1"
  zone    = "us-central1-c"
}

resource "google_dataflow_job" "wordcount" {
  name              = "wordcount"
  template_gcs_path = "gs://dataflow-templates/latest/Word_Count"
  temp_gcs_location = "gs://${var.gcs_location}/temp"
  parameters = {
    inputFile = "gs://dataflow-samples/shakespeare/kinglear.txt"
    output = "gs://${var.gcs_location}/wordcount/output"
  }
}
```

The variables are defined in the previous file but set in `df.tfvars` (change with the appropriate values):

```lang-yaml
project_id = "PROJECT_ID"
gcs_location = "BUCKET_NAME"
```

We can run the example with:

```bash
terraform apply -var-file="df.tvars"
```

and the job is successfully created:

```bash
google_dataflow_job.wordcount: Creating...
google_dataflow_job.wordcount: Creation complete after 3s [id=2020-01-27_...]
```


  [1]: https://cloud.google.com/dataflow/docs/guides/templates/provided-templates?hl=en#wordcount

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
