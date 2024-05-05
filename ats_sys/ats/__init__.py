from ats_sys.utils import clean_text,pdf_to_text,loading_cities,extract_text_from_docx_file
from ats_sys.utils.chunking import create_chunks
from transformers import pipeline
from bas_val.logger import logging
from transformers import AutoTokenizer, AutoModelForTokenClassification,DistilBertTokenizerFast

def load_model():
    logging.info("Entering into the load_model method")
    tokenizer = DistilBertTokenizerFast.from_pretrained("dslim/distilbert-NER")
    model = AutoModelForTokenClassification.from_pretrained("dslim/distilbert-NER")
    return tokenizer, model

def removing_other_countries_applicant(docx_file_path):
    logging.info("Receiving the docx file for checking eligibility")
    # Extract text from DOCX file
    input_text = extract_text_from_docx_file(docx_file_path)
    #input_text=pdf_to_text(docx_file_path)
    #print(input_text)
    input_text=clean_text(input_text)

    chunks=create_chunks(input_text,512)
    model,tokenizer=load_model()
    logging.info("Completing the loading model and tokenizer")
    nlp = pipeline("ner", model=model, tokenizer=tokenizer,framework='pt')

    results=[]
    for chunk in chunks:
        chunk=' '.join(chunk)
        ner_results=nlp(chunk)
        results.append(ner_results)
    logging.info("Completing the prediction of every words")
    locations=loading_cities()
    for result in results:
        for x in result:
            #print(x)
            entity=x['entity']
            # print(entity)
            if entity in ["B-LOC", "I-LOC","B-ORG","I-ORG"]:
                #print(x['word'])
                if x['word'] in locations:
                    #print(entity)
                # if data['city'].isin(x['word']).any():
                    #print(x['word'])
                    return f"Application {docx_file_path} is from the USA"
    return f"Application {docx_file_path} is not from the USA"