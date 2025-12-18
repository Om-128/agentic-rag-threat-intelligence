import os
import sys

from src.ingestion.data_ingestion import DataIngestionConfig, DataIngestion
from src.vector_store.build_vector_db import BuildVectorDB

class IngestionPipeline:

    def __init__(self):
        pass

    def run_ingestion_pipeline(self):

        ingestion_config = DataIngestionConfig()
        ingestion = DataIngestion(ingestion_config)

        all_texts = ingestion.convert_json_to_clean_text()

        ingestion.save_texts_to_txt(all_texts)

        build_vector_db = BuildVectorDB()
        build_vector_db.build_vector_db()

if __name__=="__main__":
    ingestion_pipeline = IngestionPipeline()
    ingestion_pipeline.run_ingestion_pipeline()