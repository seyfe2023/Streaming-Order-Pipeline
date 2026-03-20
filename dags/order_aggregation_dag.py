from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator # type: ignore
from datetime import datetime

# Define the DAG to run hourly starting from March 2, 2026
with DAG(
    dag_id="order_aggregation",
    start_date=datetime(2026, 3, 2),
    schedule_interval="@hourly",
    catchup=False
) as dag:

    # Calculate daily order totals and insert into analytics table
    aggregate_orders = PostgresOperator(
        task_id="aggregate_orders",
        postgres_conn_id="postgres_default",
        sql="""
        INSERT INTO analytics.order_metrics (order_date, total_orders, revenue)
        SELECT
            DATE(created_at),
            COUNT(*),
            SUM(amount)
        FROM staging_orders
        GROUP BY DATE(created_at)

        ON CONFLICT (order_date)
        DO UPDATE SET
            total_orders = EXCLUDED.total_orders,
            revenue = EXCLUDED.revenue;
        """
    )