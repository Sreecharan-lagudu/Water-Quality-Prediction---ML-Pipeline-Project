# 🚰 Water Quality Prediction - ML Pipeline Project

This project builds a **complete ML pipeline** to predict water quality from raw sensor data using tools like **Apache Airflow**, **Great Expectations**, **PostgreSQL**, **Streamlit**, **FastAPI**, and **Grafana**.

---

## 📁 Project Structure

```
ml_pipeline_project/
│
├── airflow/                       # Airflow-related files
│   ├── dags/                      # DAGs for ingestion, training, etc.
│   │   └── ingestion_dag.py
│   ├── Scripts/                   # Custom scripts
│   │   └── ingestion.py
│   └── reports/                   # HTML validation reports
│
├── data/                          # Project datasets
│   ├── ingestion/
│   │   └── raw_data_chunks/
│   ├── good_data/
│   └── bad_data/
│
├── fastapi_app/                   # FastAPI backend
│   └── main.py
│
├── streamlit_app/                # Streamlit frontend
│   └── app.py
│
├── notebooks/                     # EDA and experiments
│
├── requirements.txt               # Python dependencies
└── README.md                      # You are here
```

---

## ⚙️ Setup Instructions (Mac/M1 Friendly)

1. **Create and activate virtual environment**:
   ```bash
   python3 -m venv airflow_ml
   source airflow_ml/bin/activate
   ```

2. **Install Airflow with compatible providers (Airflow 2.7.2)**:
   ```bash
   pip install apache-airflow==2.7.2        apache-airflow-providers-postgres        apache-airflow-providers-redis        apache-airflow-providers-celery        apache-airflow-providers-http        apache-airflow-providers-sqlite        apache-airflow-providers-ftp        sqlalchemy psycopg2-binary        pandas great_expectations
   ```

3. **Initialize Airflow DB and create admin user**:
   ```bash
   airflow db init
   airflow users create --username admin --password admin --firstname water --lastname quality      --role Admin --email admin@water.com
   ```

4. **Start Airflow Webserver & Scheduler**:
   ```bash
   airflow webserver --port 8080
   airflow scheduler
   ```

---

## ✅ DAG: `ingestion_dag.py`

This DAG handles:

- Reading `.csv` files from `data/ingestion/raw_data_chunks`
- Validating using `great_expectations`
- Splitting into `good_data` and `bad_data`
- Saving:
  - Good data → PostgreSQL (`good_data_table`)
  - Bad data → PostgreSQL (`bad_data_table`)
- Generating HTML validation report in `/reports`
- Sending MS Teams alert via webhook

Trigger DAG manually from Airflow UI or set a schedule.

---

## 💾 PostgreSQL Setup

- **DB Name**: `ml_pipeline_db`
- **User**: `ml_user`
- **Password**: `mlpassword`
- **Tables**:
  - `good_data_table`
  - `bad_data_table`
  - `ingestion_statistics`

You can use `PgAdmin` to visualize data.

---

## 🚀 FastAPI (Backend)

Start prediction API server:
```bash
cd fastapi_app
uvicorn main:app --reload
```

---

## 🖥️ Streamlit App (Frontend)

Launch frontend dashboard:
```bash
cd streamlit_app
streamlit run app.py
```

---

## 📊 Grafana for Monitoring

- Use `Grafana` + `PostgreSQL` connection
- Build dashboards for ingestion stats & alerts

---

