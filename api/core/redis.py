import aioredis

"""
Module to handle the cache:  not implemented
"""

redis_host = 'localhost'
redis_port = 6379
redis_password = 'password'


async def cache_report_in_redis(report_id, report):
    redis_pool = await aioredis.create_redis_pool(
        f'redis://{redis_host}:{redis_port}',
        password=redis_password
    )

    report_key = f'report:{report_id}'
    await redis_pool.hmset_dict(report_key, report)

    expiration_time = 3600
    await redis_pool.expire(report_key, expiration_time)

    redis_pool.close()
    await redis_pool.wait_closed()
