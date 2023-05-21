FROM python:3.10-slim-buster
RUN apt-get update && \
    apt-get install -y gcc g++ build-essential make openssl libssl-dev
WORKDIR /filter
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt