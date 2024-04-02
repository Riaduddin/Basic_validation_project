import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import sys
from bas_val.exception import bas_val_Exception
from bas_val.logger import logging

class DataTransformation:
    def __init__(self,text):
        try:
            self.text=text
        except Exception as e:
            raise bas_val_Exception(sys,e)

    # Function to clean the text
    def clean_text(self):
        logging.info("Entered get_data_transformer_object method of DataTransformation class")
        try:
            # Remove punctuation
            text = self.text.translate(str.maketrans('', '', string.punctuation))
            
            logging.info("Tokenizing the text")
            # Tokenize the text
            tokens = word_tokenize(text)

            # Remove stopwords
            stop_words = set(stopwords.words('english'))
            filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

            # Join the filtered tokens into cleaned text
            cleaned_text = ' '.join(filtered_tokens)
            logging.info("Exited clean_text_object method of DataTransformation class")
            return cleaned_text
        except Exception as e:
            raise bas_val_Exception(sys,e)