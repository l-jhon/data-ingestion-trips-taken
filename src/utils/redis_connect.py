import redis
import os
import sys
import logging as log

log.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=log.INFO,
    stream=sys.stdout
)

REDIS_URL = os.environ.get('REDIS_URL')

def redis_connect():
    """
    Connect to the Redis database.
    Returns a Redis connection.
    """
    try:
        log.info('Connecting to the Redis database...')
        conn_redis = redis.from_url(REDIS_URL)
        log.info("Connection established.")
        return conn_redis
    except (Exception, redis.RedisError) as error:
        log.error(error)


