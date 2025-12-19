import os
import sys

from src.ingestion.data_ingestion import DataIngestionConfig, DataIngestion
from src.pipeline.build_vector_db import BuildVectorDBConfig, BuildVectorDB

from src.custom_exception import CustomException

class IngestionPipeline:

    def run_ingestion_pipeline(self):
        
        '''
            Load Json files and apply normalization and save .txt file
        '''
        try:
            '''  Ingest JSON → cleaned text '''
            ingestion_config = DataIngestionConfig()
            ingestion = DataIngestion(ingestion_config)

            cleaned_texts = ingestion.convert_json_to_clean_text()

            ''' Save cleaned text to file '''
            clean_file_path = ingestion.save_texts_to_txt(cleaned_texts)
            print(f"Cleaned text saved at: {clean_file_path}")

            # Build vector DB from cleaned texts
            vector_builder = BuildVectorDB()
            vector_builder.build_vector_db(cleaned_texts)

            print("Ingestion + Vector DB pipeline completed")
        
        except Exception as e:
            raise CustomException(e, sys)

if __name__=="__main__":
    ingestion_pipeline = IngestionPipeline()
    ingestion_pipeline.run_ingestion_pipeline()