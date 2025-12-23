import os
import sys

from src.data_pipeline.data_ingestion import DataIngestionConfig, DataIngestion
from src.data_pipeline.build_vector_db import BuildVectorDBConfig, BuildVectorDB
from src.utils import save_texts_to_txt
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

            all_text = ingestion.convert_json_to_clean_text()

            ''' Save cleaned text to file '''
            clean_file_path = save_texts_to_txt(all_text, ingestion_config.output_text_file)
            print(f"Cleaned text saved at: {clean_file_path}")

            # Build vector DB from cleaned texts
            vector_builder = BuildVectorDB()
            vector_builder.build_vector_db(clean_file_path)

            print("Ingestion + Vector DB pipeline completed")
        
        except Exception as e:
            raise CustomException(e, sys)

if __name__=="__main__":
    ingestion_pipeline = IngestionPipeline()
    ingestion_pipeline.run_ingestion_pipeline()