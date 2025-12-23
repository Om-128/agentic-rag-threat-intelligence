import os
import sys
from dataclasses import dataclass
from tqdm import tqdm
import yaml

from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

from src.custom_exception import CustomException

@dataclass
class BuildVectorDBConfig:
    config_file_path: str = os.path.join("config", "config.yaml")
    vector_db_path = os.path.join("data", "qdrant_db")
    collection_name: str = "cyber_threats"

class BuildVectorDB:

    def __init__(self):
        self.config = BuildVectorDBConfig()

        # Load YAML
        with open(self.config.config_file_path, "r") as f:
            self.yaml_config = yaml.safe_load(f)

        # Initialize Embedding Model
        self.model = SentenceTransformer(
            self.yaml_config["embeddings"]["model_name"],
            device="cuda"
        )

        # Initialize Text splitter
        splitter_cfg = self.yaml_config["text_splitter"]
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=splitter_cfg["chunk_size"],
            chunk_overlap = splitter_cfg["chunk_overlap"]
        )

    def convert_text_to_chunks(self, text_collection):
        '''
            Split cleaned text into chunks
        '''
        chunks = []
        for text in text_collection:
            chunks.extend(self.text_splitter.split_text(text))
        return chunks

    def build_vector_db(self, cleaned_texts):
        
        try:
            ''' Create chunks '''
            print("Chunking texts...")
            chunks = self.convert_text_to_chunks(cleaned_texts)
            print(f"Total chunks: {len(chunks)}")

            ''' Init Qdrant '''
            client = QdrantClient(path=self.config.vector_db_path)

            client.recreate_collection(
                collection_name=self.config.collection_name,
                vectors_config=VectorParams(
                    size=self.yaml_config["embeddings"]["dimension"],
                    distance=Distance.COSINE
                )
            )

            # Embbed + upload in batches
            batch_size = 128
            point_id = 0

            ''' Create Embeddings '''
            print("Creating embeddings...")

            for i in tqdm(range(0, len(chunks), batch_size)):
                batch = chunks[i:i + batch_size]

                embeddings = self.model.encode(
                    batch,
                    normalize_embeddings=True
                )

                client.upload_collection(
                    collection_name= self.config.collection_name,
                    vectors = embeddings,
                    payload=[{"text": c} for c in batch],
                    ids=list(range(point_id, point_id + len(batch)))
                )

                point_id += len(batch)

            print("Vector db built successfully")

        except Exception as e:
            raise CustomException(e, sys)