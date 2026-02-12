import os
import sys
import pymongo
import certifi

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY

ca = certifi.where()


class MongoDBClient:
    """
    MongoDBClient is responsible for establishing a connection to the MongoDB database.
    """

    client = None

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(
                        f"Environment variable '{MONGODB_URL_KEY}' is not set."
                    )

                MongoDBClient.client = pymongo.MongoClient(
                    mongo_db_url,
                    tlsCAFile=ca
                )

                logging.info(f"Connected MongoDB URL: {mongo_db_url}")

            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name

            logging.info(f"Using database explicitly: {database_name}")

            available_dbs = self.client.list_database_names()
            logging.info(f"Available databases in cluster: {available_dbs}")

            if database_name not in available_dbs:
                raise Exception(
                    f"Database '{database_name}' NOT FOUND in MongoDB cluster."
                )

            logging.info("MongoDB connection successful.")

        except Exception as e:
            raise MyException(e, sys)
