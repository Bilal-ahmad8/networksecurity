import os
import sys
import json

from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

import pandas as pd
import certifi

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger

ca = certifi.where()

load_dotenv()
uri = os.getenv('MONGODB_URL')

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json(self, filepath):
        try:
            data = pd.read_csv(filepath)
            data.reset_index(inplace=True, drop=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def push_data_to_mongo(self, database, collection, records):
        try:
            self.collection = collection
            self.database = database
            self.records = records

            self.mongclient = MongoClient(uri)
            self.database = self.mongclient[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            logger.info('Data Pushed to Mongo DB!')
            return len(self.records)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

if __name__ == "__main__":
    filepath = 'Network_data\phisingData.csv'
    database = 'bilalahmad'
    collection = 'NetworkData'
    obj = NetworkDataExtract()
    records = obj.csv_to_json(filepath=filepath)
    no_records = obj.push_data_to_mongo(database=database, collection=collection, records=records)
    print(no_records)
