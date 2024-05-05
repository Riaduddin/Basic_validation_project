import docx2txt
import string
import re
import PyPDF2
import pandas as pd
from bas_val.logger import logging

def clean_text(text):
    logging.info("Entering into the cleaning processing")
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize the text
    #tokens = word_tokenize(text)

    # Remove stopwords
    #stop_words = set(stopwords.words('english'))
    #filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    # Join the filtered tokens into cleaned text
    #cleaned_text = ' '.join(filtered_tokens)
    text=re.sub(r'\n','', text)
    text=re.sub(r'\t','',text)
    logging.info("Ending the clean task")
    return text

def read_words_from_file(file_path):
    logging.info("Entering into the read_words_from_file method")
    words = []
    with open(file_path, 'r') as file:
        # Read all lines from the file
        lines = file.readlines()
        for line in lines:
            # Split each line into words using whitespace as separator
            line_words = line.split()
            # Extend the words list with the words from the current line
            words.extend(line_words)
    logging.info("Ending the read_words_from_file method")
    return words

# Load DOCX file and extract text
def extract_text_from_docx_file(uploaded_file):
    logging.info("Entering into the extract_text_from_docx_file method")
    # Use docx2txt to extract text from a DOCX file
    return docx2txt.process(uploaded_file)

def pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        #print(reader)
        for page in reader.pages:
            # page = reader.getPage(page_num)
            text += page.extract_text()
    return text

def loading_cities():
    logging.info("Entering into the loading_cities method")
    data=pd.read_csv('usa_cities.csv')
    cities=list(data['city'])
    return cities

