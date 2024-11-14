FROM ghcr.io/mlflow/mlflow:v2.16.2

RUN apt-get -y update && \
    apt-get -y install python3-dev default-libmysqlclient-dev build-essential && \
    pip install --upgrade pip && \
    pip install psycopg2-binary boto3