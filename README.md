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
- [Methods](#methods)
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

The `Report` class is responsible for generating reports based on store data.

## Methods

### `generate_report(self, report_id)`

Generates a report for each store based on the provided `report_id`.

- **Parameters:**
  - `report_id`: The ID of the report.

### `uptime_last_hour(self, store: Store)`

Calculates the uptime and downtime for a specific store in the last hour.

- **Parameters:**
  - `store`: The store object for which to calculate the uptime and downtime.

### `__interpolate(self, business_hour: BusinessHour, stores, last_hour_start, last_hour_end)`

Performs interpolation to calculate the uptime and downtime for a specific store within the last hour.

- **Parameters:**
  - `business_hour`: The business hours object for the store.
  - `stores`: The list of store activities for the store.
  - `last_hour_start`: The start time of the last hour.
  - `last_hour_end`: The end time of the last hour.

### `calculate_time_diff(start_time, end_time)`

Calculates the time difference in hours between two given times.

- **Parameters:**
  - `start_time`: The start time.
  - `end_time`: The end time.

### `calculate_uptime_downtime(self, store)`

Calculates the uptime and downtime for a store over the last day and week.

- **Parameters:**
  - `store`: The store object for which to calculate the uptime and downtime.

## Interpolation Logic

To calculate the uptime and downtime within the last hour, the `__interpolate` method is used. It performs the following steps:

1. Initialize variables for downtime and uptime as 0.
2. Get the start and end times of the business hours for the store.
3. Create a list of intervals with the start and end times of the business hours.
4. Iterate over the store activities and check if the activity time falls within the business hours.
   - If the status is "active" or "inactive", add a new interval with the respective status and time.
5. Sort the intervals based on the time.
6. Handle edge cases:
   - If there are no intervals, set the downtime as the difference between the end and start times of the business hours.
   - If the last hour's end time is greater than the business hour's end time, adjust the last hour's end time to the business hour's end time.
   - If the last hour's start time is less than the business hour's start time, adjust the last hour's start time to the business hour's start time.
7. Iterate over the intervals and calculate the uptime and downtime based on the last hour's start and end times.
   - If the interval completely falls within the last hour, add the time difference to the corresponding uptime or downtime.
   - If the interval starts before the last hour's start time and ends within the last hour, add the time difference from the interval's start to the last hour's end time to the corresponding uptime or downtime.
   - If the interval starts within the last hour and ends after the last hour's end time, add the time difference from the last hour's start time to the interval's end time to the corresponding uptime or downtime.


## Credits

This project was built using the following technologies:

- ~[Docker Compose](https://docs.docker.com/compose/)~
- ~[Django](https://www.djangoproject.com/)~
- ~[Django REST framework](https://www.django-rest-framework.org/)~
- ~[PostgreSQL](https://www.postgresql.org/)~
- ~[Redis](https://redis.io/)~

