FROM bitnami/python:3.10.11
LABEL maintainer="manik das"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.dev.txt /requirements/requirements.dev.txt
COPY ./requirements.prod.txt /requirements/requirements.prod.txt
COPY ./data .

WORKDIR /storeAPI

COPY ./api ./api

ARG DEV=false

RUN apt-get update \
    && apt-get install -y postgresql-client \
                          build-essential \
                          libpq-dev && \
    if [ $DEV = "true" ]; \
        then pip install -r /requirements/requirements.dev.txt ; \
    fi && \
    pip install -r /requirements/requirements.prod.txt && \
    rm -rf /requirements
