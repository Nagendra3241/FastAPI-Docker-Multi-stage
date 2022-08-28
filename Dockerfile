FROM python:3.10.4-slim-buster as basic


WORKDIR /code

COPY ./src/ .
COPY requirements.txt .

RUN  apt-get update\
    && python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt


CMD uvicorn app:app --reload --host ${BACKEND_HOST} --port ${PORT}
