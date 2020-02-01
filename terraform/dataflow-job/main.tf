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
