from fastapi import File, UploadFile, FastAPI,HTTPException
from bas_val.component.data_transformation import DataTransformation
from bas_val.utils.main_utils import detect_language,load_model, load_vectorizer,docx_to_text
from bas_val.constant import LABELS
from bas_val.logger import logging
from bas_val.utils.word_counts import FileOperation_word_count
from bas_val.utils.page_count import convert_and_count_pages,counting_pages
from io import BytesIO
from docx2pdf import convert
from ats_sys.ats import removing_other_countries_applicant
from transformers import pipeline
from ats_sys.ats import removing_other_countries_applicant
from transformers import AutoTokenizer, AutoModelForTokenClassification
from ats_sys.utils.chunking import create_chunks
from ats_sys.utils import clean_text,pdf_to_text,loading_cities,extract_text_from_docx_file
import os

app=FastAPI()

@app.post("/open-docx")
async def open_docx(file: UploadFile = File(...)):
    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Only DOCX files are allowed")

    # name_parts=docx_path.split('.')
    # # # Create an 'upload' folder if it doesn't exist
    # file_name=name_parts[0].join('.pdf')
    # print('filename is: ',file_name)
    upload_folder = os.path.join(os.getcwd(), "upload")
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    docx_path=os.path.join(upload_folder, 'input.docx')
    with open(docx_path, "wb") as buffer:
        buffer.write(await file.read())
   

    #logging.info('Created upload folders')
    # read_file = await file.read() # read the docx file 
    # contents = BytesIO(read_file) # create a file like object from the contents

    pdf_path = os.path.join(upload_folder, 'output.pdf')
    
    # print(contents.getvalue(), 'line 26')
    # print(contents.getbuffer(), 'line 26')
    texts = docx_to_text(docx_path)
    # except:
    #     texts=docx_to_text(file)
    language = detect_language(texts)

    if language != 'en':
        return {"content": 'doc_file is in a non-English language'}

    word_counts = FileOperation_word_count(docx_path)
    counts = word_counts.file_process()
    #try:
    #logging.info("trying the read_file")
    convert(docx_path, pdf_path)
    page_count=counting_pages(pdf_path)
        #print("number of pages:",page_count)
    # except:
    #     logging.info("trying the contents")
    #     page_count=counting_pages(pdf_path)


    texts = DataTransformation(texts)
    cleaned_text = texts.clean_text()

    vectorizer = load_vectorizer()
    model = load_model()
    text_vector = vectorizer.transform([cleaned_text])
    topic = model.transform(text_vector)

    topic_index = topic.argmax()
    label = 'doc_file is {}'.format(LABELS[topic_index])

    return {'content': label,
            'Number of pages': page_count,
            'Number of words in the docx file': counts}

@app.post("/checking_doc")
async def checking_doc(file: UploadFile = File(...)):
    logging.info("Start the process")
    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Only DOCX files are allowed")
    upload_folder = os.path.join(os.getcwd(), "upload")
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    docx_path=os.path.join(upload_folder, 'input.docx')
    with open(docx_path, "wb") as buffer:
        buffer.write(await file.read())
    # logging.info("Start the process")
    # return {'About applications': removing_other_countries_applicant(docx_path)}

    tokenizer = AutoTokenizer.from_pretrained("dslim/distilbert-NER")
    model = AutoModelForTokenClassification.from_pretrained("dslim/distilbert-NER")
    input_text = extract_text_from_docx_file(docx_path)
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
                    return f"Application {docx_path} is from the USA"
    return {f"Application {docx_path} is not from the USA"}
    
    
if __name__=='__main__':
    import uvicorn
    uvicorn.run("main:app",host="127.0.0.1", port=8080,reload=True)   

