from pymongo import MongoClient
from redis import Redis

from api.config import BaseConfig, DockerizedConfig


def create_mongo_client():
    mongo_client = MongoClient(
            host=DockerizedConfig.MONGO_DATABASE_URI,
            connect=True)
    return mongo_client


def create_redis_client():
    redis_client = Redis.from_url(
            DockerizedConfig.REDIS_DATABASE_URI)
    return redis_client


def mongo_insert_one(mongo_client, collection, data, filter_options=None):
    if isinstance(mongo_client, MongoClient):
        mongo = mongo_client[BaseConfig.DATABASE_NAME][collection]
        if filter_options:
            return mongo.insert_one(data, filter_options).inserted_id
        return mongo.insert_one(data).inserted_id

def mongo_find_one(mongo_client, collection, fields, filter_options=None):
    if isinstance(mongo_client, MongoClient):
        mongo = mongo_client[BaseConfig.DATABASE_NAME][collection]
        if filter_options:
            return mongo.find_one(fields, filter_options)
        return mongo.find_one(fields)

def redis_set_key(redis_client, key, value, expire=True):
    if isinstance(redis_client, Redis):
        if expire:
            return redis_client.set(key, value,
                    BaseConfig.OTP_EXPIRES_IN_180_SECONDS)

def redis_get_key(redis_client, key):
    if isinstance(redis_client, Redis):
        return redis_client.get(f"{key}")

def redis_get_ttl(redis_client, key):
    if isinstance(redis_client, Redis):
        return redis_client.ttl(f"{key}")
