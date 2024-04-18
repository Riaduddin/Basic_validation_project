from fastapi import File, UploadFile, FastAPI,HTTPException
from bas_val.component.data_transformation import DataTransformation
from bas_val.utils.main_utils import detect_language,load_model, load_vectorizer,docx_to_text
from bas_val.constant import LABELS
from bas_val.logger import logging
from bas_val.utils.word_counts import FileOperation_word_count
from bas_val.utils.page_count import convert_and_count_pages
from io import BytesIO
import os

app=FastAPI()

@app.post("/open-docx")
async def open_docx(file: UploadFile = File(...)):
    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Only DOCX files are allowed")

    read_file = await file.read() # read the docx file 
    contents = BytesIO(read_file) # create a file like object from the contents
    # print(contents.getvalue(), 'line 26')
    # print(contents.getbuffer(), 'line 26')
    
    texts = docx_to_text(contents)
    language = detect_language(texts)

    if language != 'en':
        return {"content": 'doc_file is in a non-English language'}

    word_counts = FileOperation_word_count(contents)
    counts = word_counts.file_process()

    page_count=convert_and_count_pages(contents)
    print("number of pages:",page_count)


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
    
if __name__=='__main__':
    import uvicorn
    uvicorn.run("main:app",host="127.0.0.1", port=8080,reload=True)   

# @app.post("/open-docx")
# async def open_docx(file: UploadFile = File(...)):
#     """
#         -taking docx file & return the document file
#         -if any images include in the text file then return invalid
#     """
#     if not file.filename.endswith('.docx'):
#             raise HTTPException(status_code=400, detail="Only DOCX files are allowed")
        
#     upload_dir = 'uploads' 
#     os.makedirs(upload_dir, exist_ok=True)

#     # save the uploaded file
#     file_path = os.path.join(upload_dir, file.filename)
#     with open(file_path, 'wb') as f:
#         f.write(await file.read())
    
#     texts=docx_to_text(file_path)
#     language = detect_language(texts)

#     if language !='en':
#         return {"content ": 'doc_file is garbage language'}
    
#     word_counts=FileOperation_word_count(file_path)
#     counts=word_counts.file_process()

#     texts=DataTransformation(texts)
#     cleaned_text=texts.clean_text()

#     vectorizer=load_vectorizer()
#     model=load_model()
#     text_vector=vectorizer.transform([cleaned_text])
#     topic=model.transform(text_vector)

#     topic_index = topic.argmax()
#     label='doc_file is {}'.format(LABELS[topic_index])
    
#     return {'content':label,
#             'Number of words in the docx file ':counts}


# if __name__=='__main__':
#     import uvicorn
#     uvicorn.run("main:app",host="127.0.0.1", port=8080,reload=True)