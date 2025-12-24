import os
import sys

from src.custom_exception import CustomException

''' Save text file to file path '''
def save_texts_to_txt(texts, file_path):
    """
    Save cleaned texts to UTF-8 txt file
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8", errors="ignore") as f:
            for text in texts:
                clean_text = text.replace("\n", " ").strip()
                if clean_text:
                    f.write(clean_text + "\n")

        return file_path

    except Exception as e:
        raise CustomException(e, sys)