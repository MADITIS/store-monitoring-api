# Store Management

![Python](https://img.shields.io/badge/-Python-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/-Django-brightgreen?style=for-the-badge&logo=django&logoColor=white)
![Django Rest Framework](https://img.shields.io/badge/-Django%20Rest%20Framework-orange?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-blue?style=for-the-badge&logo=docker&logoColor=white)
![Redis](https://img.shields.io/badge/-Redis-red?style=for-the-badge&logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-blue?style=for-the-badge&logo=postgresql&logoColor=white)
![Pandas](https://img.shields.io/badge/-Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)


## Table of Contents
- [Description](#description)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Features](#features)
- [Credits](#credits)
- [References](#references)

## Description

This is a web application for managing store report. It provides a REST API for generating report for the stores.

## Requirements

- Docker
- Docker Compose

## Installation

1. Clone the repository:

## Usage

The API can be accessed through the following endpoints:

1. **/trigger_report** - This endpoint triggers report generation from the data provided (stored in DB).
    - No input.
    - `GET` request.
2. **/get_report/report_id** - This endpoint returns the status of the report or the CSV.
    - Input - report_id..
    - `GET` request.

The server port is set to Django's default port, which is 8000.

## Environment Variables

The following environment variables are used in the `.env` file:

- `DEBUG`: A boolean value that determines whether or not debug mode is enabled. Set to 1 to enable debug mode.
- `DEV`: A boolean value that determines whether or not the application is running in development mode. Set to true to enable development mode.
- `SERVER_PORT`: The port number that the Django server will listen on.
- `DJANGO_SECRET_KEY`: The secret key used by Django for cryptographic signing and hashing. This should be a long, random string.
- `POSTGRES_DB_NAME`: The name of the PostgreSQL database used by the application.
- `POSTGRES_USER`: The username used to connect to the PostgreSQL database.
- `POSTGRESQL_SUPERUSER_PASS`: The password for the PostgreSQL superuser (usually `postgres`).
- `POSTGRES_PASS`: The password for the PostgreSQL user specified by `POSTGRES_USER`.
- `REDIS_PASSWORD`: The password used to connect to Redis.
- `DJANGO_ALLOWED_HOSTS`: A comma-separated list of hostnames that the Django server is allowed to serve. In this case, it is set to `127.0.0.1` to only allow requests from the local machine.

These environment variables are used throughout the application to configure various settings, such as the database connection, Redis connection, and Django settings. By using environment variables, we can easily configure the application to work in different environments (e.g. development, staging, production) without having to modify the code itself.

## Features

- **Report Generation**: The API provides an endpoint to trigger report generation from the data stored in the database. The endpoint returns a random string as the report ID.
- **Report Status**: The API provides an endpoint to check the status of the report generation. If the report is still being generated, the endpoint returns "Running". If the report is complete, the endpoint returns "Complete" along with the CSV file containing the data.
- **Redis Cache**: The API uses Redis to cache the generated report for one hour. This improves performance by reducing the number of times the report needs to be generated.

## Credits

This project was built using the following technologies:

- ~[Docker Compose](https://docs.docker.com/compose/)~
- ~[Django](https://www.djangoproject.com/)~
- ~[Django REST framework](https://www.django-rest-framework.org/)~
- ~[PostgreSQL](https://www.postgresql.org/)~
- ~[Redis](https://redis.io/)~

