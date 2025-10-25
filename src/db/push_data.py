import os, sys
import json
import pandas as pd
import numpy as np
import pymongo
from pymongo.server_api import ServerApi
from src.logger import logging
from src.exception import CustomException

from dotenv import load_dotenv
load_dotenv()

import certifi
ca=certifi.where()

mongo_url = os.getenv("MONGO_URL")


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys)
        
    def csv_to_json(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)

            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise CustomException(e, sys)
        
    def insert_data_to_mongo(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(mongo_url, server_api=ServerApi('1'))
            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))

        except Exception as e:
            raise CustomException(e, sys)



# if __name__ == '__main__':
#     file_path = 'Network_data/phisingData.csv'
#     database = 'demo'
#     collection = 'demoCollection'

#     obj = NetworkDataExtract()
#     records = obj.csv_to_json(file_path)

#     print(obj.insert_data_to_mongo(records, database, collection))


