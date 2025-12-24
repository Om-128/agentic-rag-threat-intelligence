import os
import sys

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

from src.custom_exception import CustomException

''' --- PATHS --- '''

VECTOR_DB_PATH = "data/qdrant_db"
COLLECTION_NAME = "cyber_threats"
EMBDDING_MODEL = "BAAI/bge-base-en-v1.5"

class RetrieveData:

    def __init__(self):
        self.client = QdrantClient(path=VECTOR_DB_PATH)
        self.model = SentenceTransformer(EMBDDING_MODEL)


    def retrive_data(self, query : str, top_k):

        try:
            print("Encoding Started...")
            embeddings = self.model.encode(
                query,
                normalize_embeddings = True
            )

            result = self.client._client.search(
                collection_name = COLLECTION_NAME,
                query_vector = embeddings,
                limit = top_k
            )

            return [hit.payload["text"] for hit in result]
        except Exception as e:
            raise CustomException(e, sys)

if __name__=="__main__":

    query = "SQL Injection in system found"
    retriver = RetrieveData()
    print(retriver.retrive_data(query=query, top_k=4))