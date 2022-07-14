from pymongo import MongoClient, ReturnDocument

from api.config import BaseConfig, DockerizedConfig


def create_mongo_client():
    mongo_client = MongoClient(
            host=DockerizedConfig.MONGO_DATABASE_URI,
            connect=True)
    return mongo_client


def mongo_insert_one(mongo_client, collection, data, filter_option=None):
    if isinstance(mongo_client, MongoClient):
        mongo = mongo_client[BaseConfig.DATABASE_NAME][collection]
        if filter_option:
            return mongo.insert_one(data, filter_option).inserted_id
        return mongo.insert_one(data).inserted_id

def mongo_find_one(mongo_client, collection, fields, filter_option=None):
    if isinstance(mongo_client, MongoClient):
        mongo = mongo_client[BaseConfig.DATABASE_NAME][collection]
        if filter_option:
            return mongo.find_one(fields, filter_option)
        return mongo.find_one(fields)

def mongo_find_one_update(mongo_client, collection, email, data):
    if isinstance(mongo_client, MongoClient):
        mongo = mongo_client[BaseConfig.DATABASE_NAME][collection]
        return mongo.find_one_and_update(
            {"email": f"{email}"},
            {"$set": data}, return_document=ReturnDocument.AFTER)
