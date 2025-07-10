import os
import requests
from google.cloud import storage

def run(inputs, outputs):
    dataset_url = inputs["dataset_url"]
    file_name = "dataset.csv"

    # Download the dataset
    response = requests.get(dataset_url)
    response.raise_for_status()
    
    with open(file_name, "wb") as f:
        f.write(response.content)

    # Upload to GCS
    bucket_name = inputs["bucket_name"]
    destination_blob = inputs.get("destination_blob", "raw_data/dataset.csv")

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(file_name)

    # Return the GCS URI
    gcs_uri = f"gs://{bucket_name}/{destination_blob}"
    outputs["gcs_uri"] = gcs_uri
