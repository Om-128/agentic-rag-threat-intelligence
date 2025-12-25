import os
import sys
import json
import yaml
from tqdm import tqdm
from dataclasses import dataclass

from src.data_pipeline.parser import parse_cisa, parse_mitre, parse_nvd
from src.custom_exception import CustomException

'''
    This class stores configueration required for ingestion
'''
@dataclass
class DataIngestionConfig:
    config_file_path = os.path.join('config', 'config.yaml')
    output_text_file: str = "data/clean_security_texts.txt"

'''
    This class is responsible for
    Loading json files -> Convert them into text file
'''
class DataIngestion:

    def __init__(self, config:DataIngestionConfig):
        self.config = config

    def convert_json_to_clean_text(self):
        """
        Load JSON files from config.yaml
        Parse text
        Return list[str]
        """
        try:
            # Load config
            with open(self.config.config_file_path, "r") as f:
                config = yaml.safe_load(f)

            cleaned_text = []

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
                        cleaned_text.append(cleaned)
            
            
            print("Cleaned text returned...")

            return cleaned_text

        except Exception as e:
            CustomException(e, sys)


'''
    Remove redundant boilerplate phrases and normalize whitespace
'''
def normalize_text(text: str) -> str:

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
