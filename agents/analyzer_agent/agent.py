import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.cloud import storage
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel
import re

import re

def generate_gemini_summary(df):
    """
    Generate AI-powered summary using Gemini via Vertex AI
    """
    try:
        # Initialize Vertex AI
        project_id = os.environ.get("autosight")
        location = os.environ.get("GCP_LOCATION", "us-east1")
        
        aiplatform.init(project=project_id, location=location)
        
        # Initialize Gemini model
        model = GenerativeModel(model_name="gemini-2.5-pro")
        
        # Prepare data context for Gemini
        data_context = f"""
        Dataset Overview:
        - Shape: {df.shape}
        - Columns: {list(df.columns)}
        - Data Types: {df.dtypes.to_dict()}
        - Missing Values: {df.isnull().sum().to_dict()}
        
        Statistical Summary:
        {df.describe().to_string()}
        
        Sample Data (first 5 rows):
        {df.head().to_string()}
        """
        
        prompt = f"""
        As a data analyst, provide a comprehensive analysis of this dataset:
        
        {data_context}
        
        Please provide:
        1. Data Quality Assessment
        2. Key Statistical Insights
        3. Trend Analysis (if time series data)
        4. Anomalies or Outliers Detection
        5. Business Insights and Recommendations
        6. Actionable Next Steps
        
        Format your response as a clear, structured summary that would be valuable for stakeholders.
        Provide only the analysis without any greetings or introductory phrases.
        """
        
        response = model.generate_content(prompt)
        
        # Clean up the response text
        clean_text = clean_gemini_response(response.text)
        
        return f"\n{clean_text}\n"
        
    except Exception as e:
        return f"AI Analysis Error: {str(e)}\n\nFalling back to basic analysis:\nRows: {len(df)}\nColumns: {list(df.columns)}\nData Types: {df.dtypes.to_dict()}"

def clean_gemini_response(text):
    """
    Clean up Gemini response by removing markdown formatting and greetings
    """
    # Remove common greeting patterns
    greeting_patterns = [
        r'^(Hello|Hi|Greetings|Welcome)[^\n]*\n',
        r'^(I\'d be happy to|I can help|Let me analyze)[^\n]*\n',
        r'^(Based on the data you\'ve provided|Looking at this dataset)[^\n]*\n',
        r'^(Here\'s my analysis|Here is the analysis)[^\n]*\n'
    ]
    
    for pattern in greeting_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
    
    # Remove markdown formatting
    # Remove headers (##, ###, etc.)
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
    
    # Remove bold formatting (**text** or __text__)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    
    # Remove italic formatting (*text* or _text_)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'\1', text)
    text = re.sub(r'(?<!_)_([^_]+)_(?!_)', r'\1', text)
    
    # Remove code formatting (`code`)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    
    # Remove bullet points and replace with dashes
    text = re.sub(r'^\s*[\*\-\+]\s*', '- ', text, flags=re.MULTILINE)
    
    # Remove horizontal rules
    text = re.sub(r'^---+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\*\*\*+\s*$', '', text, flags=re.MULTILINE)
    
    # Remove extra whitespace and empty lines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = text.strip()
    
    # Remove any remaining double slashes or other common artifacts
    text = re.sub(r'//', '', text)
    text = re.sub(r'\\\\', '', text)
    
    return text

def run(inputs, outputs):
    bucket_name = inputs["bucket_name"]
    blob_path = inputs["gcs_csv_path"]

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_path)
    blob.download_to_filename("data.csv")

    # Load into pandas
    df = pd.read_csv("data.csv")
    df.dropna(inplace=True)

    # Generate AI-powered summary using Gemini
    summary = generate_gemini_summary(df)

    # Create visualization if appropriate columns exist
    if "Month" in df.columns and "1958" in df.columns:
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=df, x="Month", y="1958", marker="o", linewidth=2.5, markersize=8)
        plt.title("Monthly Air Travel - 1958 (AI Analysis)", fontsize=16, fontweight='bold')
        plt.xlabel("Month", fontsize=12)
        plt.ylabel("Air Travel Volume", fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig("output.png", dpi=300, bbox_inches='tight')
    else:
        # Create a generic visualization for other datasets
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            plt.figure(figsize=(12, 8))
            df[numeric_cols[0]].plot(kind='line', marker='o')
            plt.title(f"Data Analysis - {numeric_cols[0]}", fontsize=16, fontweight='bold')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig("output.png", dpi=300, bbox_inches='tight')

    # Upload summary and image to GCS
    image_blob = bucket.blob("trendflow/analysis_plot.png")
    image_blob.upload_from_filename("output.png")

    summary_blob = bucket.blob("trendflow/summary.txt")
    with open("summary.txt", "w") as f:
        f.write(summary)
    summary_blob.upload_from_filename("summary.txt")

    # Output URIs
    outputs["image_uri"] = f"gs://{bucket_name}/trendflow/analysis_plot.png"
    outputs["summary_uri"] = f"gs://{bucket_name}/trendflow/summary.txt"
