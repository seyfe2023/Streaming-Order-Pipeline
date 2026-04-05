FROM apache/airflow:2.10.4
USER root
RUN apt-get update && apt-get install -y git
USER airflow
RUN pip install dbt-postgres
