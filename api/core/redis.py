from typing import List
import redis
from django.core.cache import cache

# import os

# redis_host = os.environ.get("REDIS_HOST")
# redis_port = os.environ.get("REDIS_PORT")
# redis_password = os.environ.get("REDIS_PASSOWRD")


# def start_redis():
#     redis_pool = redis.Redis(
#         host=redis_host, port=redis_port, password=redis_password)
#     return redis_pool


# def cache_report_in_redis(report_id, report):
#     redis_pool = start_redis()
#     redis_pool.hmset(report_id, report)
#     expiration_time = 3600
#     redis_pool.expire(report_id, expiration_time)


# def add_report_key(report_id):
#     redis_pool = start_redis()
#     redis_pool.set(report_id, "")

def cache_report(report, report_id) -> List | None:
    if not cache.has_key(report_id):
        return None
    cached_data = cache.get(report_id)
    if cached_data:
        return cached_data
    else:
        data = report

        cache.set(report_id, data)

        return data


def add_report_key(report_id):
    cache.set(report_id, "")


def get_report(report_id: str) -> List | None:
    if not cache.has_key(report_id):
        return None
    cached_data = cache.get(report_id)
    if cached_data:
        return cached_data
    return None
