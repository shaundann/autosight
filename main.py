import os
import subprocess
from agents.data_crawler_agent.agent import run as run_crawler
from agents.analyzer_agent.agent import run as run_analyzer
from agents.bigquery_writer_agent.agent import run as run_bq

def main():
    # Set credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS",
        "/Users/shaundanny/Desktop/AutoSight/autosight-agent-key.json"
    )

    bucket = "autosight-data"
    dataset_url = "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv"

    # Step 1: Crawl CSV
    crawler_out = {}
    run_crawler(
        inputs={
            "dataset_url": dataset_url,
            "bucket_name": bucket,
            "destination_blob": "trendflow/raw_airtravel.csv"
        },
        outputs=crawler_out
    )
    csv_uri = crawler_out["gcs_uri"]
    print(f"✅ Raw CSV uploaded to: {csv_uri}")

    # Step 2: Analyze and plot
    analyzer_out = {}
    run_analyzer(
        inputs={
            "bucket_name": bucket,
            "gcs_csv_path": csv_uri.replace(f"gs://{bucket}/", "")
        },
        outputs=analyzer_out
    )
    print(f"✅ Plot URI: {analyzer_out['image_uri']}")
    print(f"✅ Summary URI: {analyzer_out['summary_uri']}")

    # Step 3: Load into BigQuery
    bq_out = {}
    run_bq(
        inputs={
            "bucket_name": bucket,
            "gcs_csv_path": csv_uri.replace(f"gs://{bucket}/", ""),
            "bq_dataset": "autosight_dataset",
            "bq_table": "airtravel_data"
        },
        outputs=bq_out
    )
    print(f"✅ BigQuery Table: {bq_out['bigquery_uri']}")

    # Step 4: Launch Streamlit dashboard
    print("🚀 Launching dashboard at http://localhost:8501 ...")
    subprocess.run(["streamlit", "run", "dashboard.py"])

if __name__ == "__main__":
    main()
