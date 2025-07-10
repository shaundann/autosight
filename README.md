# 🤖 AutoSight – Automated AI Data Analysis Pipeline on Google Cloud

**AutoSight** is a multi-agent AI system that automates the entire data analytics pipeline — from dataset ingestion to AI-powered insights — using Google Cloud Platform (GCP).

With just a CSV URL, AutoSight:
- 📥 Crawls and uploads the dataset to Google Cloud Storage
- 📊 Cleans and analyzes trends using pandas and seaborn
- 🧠 Generates summaries using Gemini or GPT-like models
- 🗃️ Loads data into BigQuery for structured querying
- 📈 Displays all results in a modern Streamlit dashboard

---

## 🚀 Features

- 🌐 Web-based CSV ingestion from any public URL  
- 📈 Trend analysis + visual plots  
- 🤖 Natural language summaries with LLMs  
- ☁️ Cloud-native: Cloud Storage + BigQuery  
- 🖥️ Streamlit-powered live dashboard  
- 💡 Modular agent architecture for easy extensibility  

---

## 🛠️ Tech Stack

| Layer         | Technology                      |
|---------------|----------------------------------|
| 💻 Backend     | Python 3.12                      |
| ☁️ Cloud       | Google Cloud Storage, BigQuery, Vertex AI |
| 🤖 AI          | Gemini Pro (or OpenAI GPT)       |
| 📊 Visualization | matplotlib, seaborn, Streamlit  |
| 🧱 Architecture | Multi-Agent System               |

---

## 📁 Folder Structure

```
AutoSight/
├── main.py                      # Orchestrates entire pipeline
├── dashboard.py                 # Streamlit frontend
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── agents/
│   ├── data\_crawler\_agent/
│   │   └── agent.py             # Downloads CSV to GCS
│   ├── analyzer\_agent/
│   │   └── agent.py             # Analyzes data + generates summary
│   └── bigquery\_writer\_agent/
│       └── agent.py             # Loads dataset into BigQuery
```


---

## ⚙️ Setup Guide

### 1. Clone the repository

```bash
git clone https://github.com/your-username/AutoSight.git
cd AutoSight
````

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure GCP

1. Enable these APIs:

   * Vertex AI
   * Cloud Storage
   * BigQuery
2. Create a service account with roles:

   * `Storage Admin`
   * `BigQuery Data Editor`
   * `Vertex AI User`
3. Download its credentials file as:

   ```
   autosight-agent-key.json
   ```

### 5. Run the pipeline

```bash
python main.py
```

The script will:

* Download and store the dataset in GCS
* Analyze and generate a plot + summary
* Load structured data into BigQuery
* Launch the interactive dashboard automatically

---

## 📊 Example Dataset

Default dataset:

> [Air Travel (1958–1960)](https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv)

---

## 🧠 Future Enhancements

* [ ] Upload custom CSVs via dashboard
* [ ] Deploy Streamlit app to GCP App Engine
* [ ] Add forecasting and clustering agents
* [ ] Multi-dataset support + scheduling

---

## 🙅‍♂️ .gitignore

Create a `.gitignore` with the following:

```
autosight-agent-key.json
output.png
summary.txt
__pycache__/
*.pyc
venv/
.env
```

---

## 💬 Contact

Built by **Shaun Danny**

📧 [shaundanny2007@gmail.com](mailto:shaundanny2007@gmail.com)
💼 [LinkedIn]((https://www.linkedin.com/in/shaundanny/))

---

## 🏁 Acknowledgements

Inspired by [Google Cloud Multi-Agent Hackathon](https://googlecloudmultiagents.devpost.com) and the [original InsightAgents](https://github.com/Soulfullmens/insightagents) project.

```

---

Would you like me to create and export this `README.md` file for you directly so you can drop it into your GitHub repo?
```
