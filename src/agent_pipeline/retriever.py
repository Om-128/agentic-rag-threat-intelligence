import os
import sys

from sentence_transformers import SentenceTransformer

from chromadb.config import Settings
import chromadb
from chromadb import Client, PersistentClient

from src.custom_exception import CustomException

''' --- PATHS --- '''

VECTOR_DB_PATH = "data/chromadb"
COLLECTION_NAME = "cyber_threats"
EMBDDING_MODEL = "BAAI/bge-base-en-v1.5"

class RetrieveData:

    def __init__(self):
        self.client = PersistentClient(path=VECTOR_DB_PATH)
        self.model = SentenceTransformer(EMBDDING_MODEL)
        self.collection_name = COLLECTION_NAME

    def retrive_data(self, query : str, top_k):

        try:
            print(self.client.list_collections())

        except Exception as e:
            raise CustomException(e, sys)

if __name__=="__main__":

    query = "SQL Injection in system found"
    retriver = RetrieveData()
    print(retriver.retrive_data(query=query, top_k=4))