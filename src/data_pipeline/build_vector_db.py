import os
import sys
from dataclasses import dataclass
from tqdm import tqdm
import yaml

from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

import chromadb

from src.custom_exception import CustomException

@dataclass
class BuildVectorDBConfig:
    config_file_path: str = os.path.join("config", "config.yaml")
    vector_db_path = 'data/chromadb'
    collection_name: str = "cyber_threats"

class BuildVectorDB:

    '''
        Initialize Yaml, Embedding Model, Text Spliiter, Chromadb
    '''
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

    '''
        Split text to chunks
    '''
    def convert_text_to_chunks(self, text_collection):
        '''
            Split cleaned text into chunks
        '''
        chunks = []
        for text in text_collection:
            chunks.extend(self.text_splitter.split_text(text))
        return chunks

    '''
        Build vector DB
    '''
    def build_vector_db(self, cleaned_texts):
        
        try:
            ''' Create chunks '''
            print("Chunking texts...")
            chunks = self.convert_text_to_chunks(cleaned_texts)
            print(f"Total chunks: {len(chunks)}")

            # Chroma client + collection
            client = chromadb.PersistentClient(path=self.config.vector_db_path)
            collection = client.get_or_create_collection(
            name=self.config.collection_name
            )

            print("Collection List:",client.list_collections())

            batch_size = 128

            ''' Create Embeddings '''
            print("Creating embeddings...")

            for i in tqdm(range(0, len(chunks), batch_size)):
                batch_text = chunks[i:i + batch_size]

                embeddings = self.model.encode(
                    batch_text,
                    normalize_embeddings=True
                ).tolist()

                collection.add(
                    documents=batch_text,
                    embeddings=embeddings,
                    ids=[str(i + j) for j in range(len(batch_text))]
                )

            print("Chroma vector DB built successfully")

        except Exception as e:
            raise CustomException(e, sys)