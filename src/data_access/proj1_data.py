import sys
import pandas as pd
import numpy as np
from typing import Optional
from pymongo.errors import PyMongoError

from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME
from src.exception import MyException


class Proj1Data:
    """
    A class to export MongoDB records as a pandas DataFrame using batching.
    """

    def __init__(self) -> None:
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e, sys)

    def export_collection_as_dataframe(
        self,
        collection_name: str,
        database_name: Optional[str] = None,
        batch_size: int = 50000   # SAFE for Atlas Free tier
    ) -> pd.DataFrame:

        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.client[database_name][collection_name]

            total_docs = collection.count_documents({})
            print(f"Total documents in MongoDB: {total_docs}")

            dfs = []
            fetched = 0

            while fetched < total_docs:
                cursor = (
                    collection.find({})
                    .skip(fetched)
                    .limit(batch_size)
                )

                batch_df = pd.DataFrame(list(cursor))

                if batch_df.empty:
                    break

                dfs.append(batch_df)
                fetched += len(batch_df)

                print(f"Fetched {fetched}/{total_docs} documents")

            df = pd.concat(dfs, ignore_index=True)

            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            df.replace({"na": np.nan}, inplace=True)

            print("Final dataframe shape:", df.shape)
            return df

        except PyMongoError as e:
            raise MyException(e, sys)
        except Exception as e:
            raise MyException(e, sys)
