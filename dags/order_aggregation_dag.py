from airflow import DAG
from airflow.operators.bash import BashOperator    
from datetime import datetime
import os

# Define your actual project path
DBT_PROJECT_DIR = "/home/seyfe/streaming-order-pipeline/dbt_project/streaming_orders"
DBT_PROFILES_DIR = "/home/seyfe/.dbt" 

with DAG(
    dag_id="order_aggregation_medallion",
    start_date=datetime(2026, 3, 2),
    schedule_interval="@hourly",
    catchup=False
) as dag:

    run_medallion_layers = BashOperator(
        task_id="run_dbt_models",
        bash_command=(
            "cd /opt/airflow/dbt_project/streaming_orders && "
            "/home/airflow/.local/bin/dbt run "
            "--log-path /tmp/dbt_logs "
            "--target-path /tmp/dbt_target"
        ),
        env={
            'DBT_PROFILES_DIR': '/opt/airflow/.dbt' 
        }
    )