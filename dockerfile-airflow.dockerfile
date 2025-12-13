# Dockerfile-airflow
FROM apache/airflow:2.9.3

# Usar usuário airflow
USER airflow

# Instalar dbt e pacotes necessários
RUN pip install --no-cache-dir dbt-core dbt-snowflake
