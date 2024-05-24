from fastapi import File, UploadFile, FastAPI,HTTPException
from bas_val.component.data_transformation import DataTransformation
from bas_val.utils.main_utils import detect_language,load_model, load_vectorizer,docx_to_text
from bas_val.constant import LABELS
from bas_val.utils.word_counts import FileOperation_word_count
from bas_val.utils.page_count import counting_pages
from docx2pdf import convert
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification
from ats_sys.utils.chunking import create_chunks
from ats_sys.utils import clean_text,loading_cities,extract_text_from_docx_file
import os

app=FastAPI()

@app.post("/open-docx")
async def check_basic_validity(file: UploadFile = File(...)):

    """
    This function is used to check the basic validity of a document.
    It takes a docx file as an input and returns a JSON response.
    The JSON response contains the basic validity of the docx file.
    The JSON response also contains the number of pages and words in the docx file.
    """

    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Only DOCX files are allowed")

    #creating folder for storing docx file and pdf file
    upload_folder = os.path.join(os.getcwd(), "upload")
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    docx_path=os.path.join(upload_folder, 'input.docx')
    with open(docx_path, "wb") as buffer:
        buffer.write(await file.read())
    
    texts = docx_to_text(docx_path) # Convert DOCX to text
   
    language = detect_language(texts) # Detecting the language english or not

    if language != 'en':
        return {"content": 'doc_file is in a non-English language'}

    word_counts = FileOperation_word_count(docx_path)
    counts = word_counts.file_process()
    
    pdf_path = os.path.join(upload_folder, 'output.pdf')
    convert(docx_path, pdf_path) # Convert docx to pdf

    page_count=counting_pages(pdf_path) #page count

    #cleaning the text 
    texts = DataTransformation(texts)
    cleaned_text = texts.clean_text()
    
    #loading the model and vectorizer
    vectorizer = load_vectorizer()
    model = load_model()
    text_vector = vectorizer.transform([cleaned_text])
    topic = model.transform(text_vector) #transforming the text into vector for similarity

    #Matching the predicting labels
    topic_index = topic.argmax()
    label = 'doc_file is {}'.format(LABELS[topic_index])

    return {'content': label,
            'Number of pages': page_count,
            'Number of words in the docx file': counts}



@app.post("/checking_doc")
async def checking_doc_location(file: UploadFile = File(...)):
    """
    This function is to check any relation of the participant with the USA
    It takes a docx file as an input and returns a JSON response of the applicant is from 
    USA or not.
    """

    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Only DOCX files are allowed")
    
    #creating folder for storing docx file and pdf file
    upload_folder = os.path.join(os.getcwd(), "upload")
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    docx_path=os.path.join(upload_folder, file.filename)
    with open(docx_path, "wb") as buffer:
        buffer.write(await file.read())

    #Calling tokenizer and model of pretrained distil bert from huggingface
    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
    input_text = extract_text_from_docx_file(docx_path)
    input_text=clean_text(input_text)

    chunks=create_chunks(input_text,512) #creating chunk for using the whole resume text data
    nlp = pipeline("ner", model=model, tokenizer=tokenizer) #putting all in the pipeline

    results=[]
    for chunk in chunks:
        chunk=' '.join(chunk)
        ner_results=nlp(chunk)
        results.append(ner_results)
    
    locations=loading_cities() #loading the USA cities name
    for result in results:
        for x in result:
            entity=x['entity'] #separating the classes

            #only checking the location and organization NER
            if entity in ["B-LOC", "I-LOC","B-ORG","I-ORG"]:  
                if x['word'] in locations:
                    return f"Application {docx_path} is from the USA"
                
    return {f"Application {docx_path} is not from the USA"}
    
    
if __name__=='__main__':
    import uvicorn
    uvicorn.run("main:app",host="127.0.0.1", port=8080,reload=True)   

