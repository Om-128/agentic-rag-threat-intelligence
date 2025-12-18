import os
import sys
import json
import yaml
from tqdm import tqdm
from dataclasses import dataclass

from src.ingestion.parser import parse_cisa, parse_mitre, parse_nvd
from src.custom_exception import CustomException

'''
    This class stores configueration required for ingestion
'''
@dataclass
class DataIngestionConfig:
    config_file_path = os.path.join('config', 'config.yaml')
    output_text_file: str = "data/clean_security_texts.txt"


def normalize_text(text: str) -> str:
    """
    Remove redundant boilerplate phrases and normalize whitespace
    """
    boilerplate_phrases = [
        "The exploit has been disclosed to the public and may be used.",
        "The exploit has been disclosed to the public and may be used",
        "It is possible to launch the attack remotely.",
        "It is possible to initiate the attack remotely.",
        "The attack can be launched remotely.",
        "The attack may be initiated remotely.",
        "The attack can be initiated remotely.",
    ]

    for phrase in boilerplate_phrases:
        text = text.replace(phrase, "")

    return " ".join(text.split())


'''
    This class is responsible for
    Loading json files -> Convert them into clean text
'''
class DataIngestion:

    def __init__(self, config:DataIngestionConfig):
        self.config = config

    def convert_json_to_clean_text(self):
        """
        Load JSON files from config.yaml
        Parse and clean text
        Return list[str]
        """
        try:
            # Load config
            with open(self.config.config_file_path, "r") as f:
                config = yaml.safe_load(f)

            all_texts = []

            for path in tqdm(config["json_files"], desc="Ingesting JSON files"):
                if "nvd" in path:
                    texts = parse_nvd(path)
                elif "cisa" in path:
                    texts = parse_cisa(path)
                elif "mitre" in path:
                    texts = parse_mitre(path)
                else:
                    continue

                ''' Apply normalization 
                    Remove redundunt unnecessary texts
                '''
                for text in texts:
                    cleaned = normalize_text(text)
                    if cleaned:
                        all_texts.append(cleaned)

            return all_texts

        except Exception as e:
            CustomException(e, sys)

    # def save_embeddings_to_db():
    def save_texts_to_txt(self, texts):
        """
        Save cleaned texts to UTF-8 txt file
        """
        try:
            os.makedirs(os.path.dirname(self.config.output_text_file), exist_ok=True)

            with open(self.config.output_text_file, "w", encoding="utf-8", errors="ignore") as f:
                for text in texts:
                    clean_text = text.replace("\n", " ").strip()
                    if clean_text:
                        f.write(clean_text + "\n")
        except Exception as e:
            raise CustomException(e, sys)




