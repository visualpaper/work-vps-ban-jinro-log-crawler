from pymongo import MongoClient
from pymongo.database import Database

from src.config.config import Settings


class DataBase:
    client: MongoClient
    database: Database


db = DataBase()


def connect_to_mongo(config: Settings):
    db.client = MongoClient(
        str(config.mongodb_url),
        maxPoolSize=config.mongodb_max_connection_pool,
        minPoolSize=config.mongodb_min_connection_pool,
    )
    db.database = db.client[config.mongodb_dbname]


def close_mongo_connection():
    db.client.close()


def get_database() -> Database:
    return db.database
