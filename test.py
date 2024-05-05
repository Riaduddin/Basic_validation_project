from bas_val.component.data_transformation import DataTransformation
from bas_val.utils.main_utils import detect_language,load_model, load_vectorizer,docx_to_text
from bas_val.constant import LABELS
from bas_val.utils.word_counts import FileOperation_word_count
from bas_val.logger import logging
from bas_val.utils.page_count import convert_and_count_pages
from transformers import pipeline
from ats_sys.ats import removing_other_countries_applicant
from transformers import AutoTokenizer, AutoModelForTokenClassification
from ats_sys.utils.chunking import create_chunks
from ats_sys.utils import clean_text,pdf_to_text,loading_cities,extract_text_from_docx_file

# import nltk
# nltk.download('punkt')


# def checking(contents):
#     texts=docx_to_text(contents)
#     language = detect_language(texts)
#     logging.info("language detection is completed")
#     if language !='en':
#         return {"content ": 'doc_file is garbage'}

#     #counts=FileOperation_word_count(contents)
#     # print('length of the texts: ',counts.file_process())

#     page_count=convert_and_count_pages(contents)
#     print("number of pages:",page_count)

#     texts=DataTransformation(texts)
#     cleaned_text=texts.clean_text()

    

#     vectorizer=load_vectorizer()
#     model=load_model()
#     text_vector=vectorizer.transform([cleaned_text])
#     topic=model.transform(text_vector)

#     topic_index = topic.argmax()
#     label='doc_file is {}'.format(LABELS[topic_index])

#     return label

def checking(contents):
    tokenizer = AutoTokenizer.from_pretrained("dslim/distilbert-NER")
    model = AutoModelForTokenClassification.from_pretrained("dslim/distilbert-NER")
    input_text = extract_text_from_docx_file(contents)
    input_text=clean_text(input_text)

    chunks=create_chunks(input_text,512)
    nlp = pipeline("ner", model=model, tokenizer=tokenizer)
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
                    return f"Application {contents} is from the USA"
    return f"Application {contents} is not from the USA"



file ='6373694492.docx'
print(checking(file))
            

