import os
import pandas as pd
from google.cloud import storage, bigquery

def run(inputs, outputs):
    bucket_name = inputs["bucket_name"]
    gcs_csv_path = inputs["gcs_csv_path"]
    bq_dataset = inputs["bq_dataset"]
    bq_table = inputs["bq_table"]

    # Download CSV from GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcs_csv_path)
    blob.download_to_filename("temp.csv")

    # Load into pandas
    df = pd.read_csv("temp.csv")
    df.dropna(inplace=True)

    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace('"', '').str.replace("'", "")

    # Upload to BigQuery
    bq_client = bigquery.Client()
    table_id = f"{bq_client.project}.{bq_dataset}.{bq_table}"

    job = bq_client.load_table_from_dataframe(
        df,
        table_id,
        job_config=bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE",
        )
    )
    job.result()

    outputs["bigquery_uri"] = table_id
