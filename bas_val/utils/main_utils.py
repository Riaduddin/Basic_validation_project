import joblib
from langdetect import detect
import sys
from bas_val.constant import MODEL_PATH, VECTORIZER_PATH
from bas_val.exception import bas_val_Exception
import docx2txt
from bas_val.logger import logging
def detect_language(text):
    """
    Detect the language of a given text.

    Args:
        text (str): The text to be detected.

    Returns:
        str: The language code of the text, or "Unknown" if the language could not be detected.

    Raises:
        ValueError: If the input text is not a string.

    """
    try:
        language = detect(text)
        return language
    except:
        return "Unknown"
    
def load_vectorizer():
    vectorizer=joblib.load(VECTORIZER_PATH)
    return vectorizer
    
def load_model():
    lda_model=joblib.load(MODEL_PATH)
    return lda_model

def docx_to_text(file):
        try:
            logging.info("Converting the docx to text")
            text=docx2txt.process(file)
            return text
        except Exception as e:
            logging.info(e)
            raise bas_val_Exception(sys,e)
