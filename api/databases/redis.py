from redis import Redis

from api.config import DockerizedConfig
from api.config import BaseConfig


def create_redis_client():
    redis_client = Redis.from_url(
            DockerizedConfig.REDIS_DATABASE_URI)
    return redis_client


def redis_set_key(redis_client, key, value, expire=True):
    if isinstance(redis_client, Redis):
        if expire:
            return redis_client.set(key, value,
                BaseConfig.OTP_EXPIRES_IN_SECONDS)

def redis_get_key(redis_client, key):
    if isinstance(redis_client, Redis):
        return redis_client.get(f"{key}")

def redis_delete_key(redis_client, key):
    if isinstance(redis_client, Redis):
        return redis_client.delete(f"{key}")
