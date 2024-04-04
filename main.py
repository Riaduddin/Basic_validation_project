from fastapi import File, UploadFile, FastAPI
from bas_val.component.data_transformation import DataTransformation
from bas_val.utils.main_utils import detect_language,load_model, load_vectorizer,docx_to_text
from bas_val.constant import LABELS
import docx
import os


# class MyApp:
#     def __init__(self):
#         self.app=FastAPI()

#         @self.app.post("/open-docx")
#         async def open_docx(self,file: UploadFile = File(...)):
#             """
#                 -taking docx file & return the document file
#                 -if any images include in the text file then return invalid
#             """
#             contents = await file.read()
#             texts=docx_to_text(contents)
#             language = detect_language(texts)

#             if language !='en':
#                 return {"content ": 'doc_file is garbage language'}
#             texts=DataTransformation(texts)
#             cleaned_text=texts.clean_text()

#             vectorizer=load_vectorizer()
#             model=load_model()
#             text_vector=vectorizer.transform([cleaned_text])
#             topic=model.transform(text_vector)

#             topic_index = topic.argmax()
#             label='doc_file is {}'.format(LABELS[topic_index])
            
#             return {'content':label}


# if __name__=='__main__':
#     my_app=MyApp().open_docx()
#     import uvicorn
#     uvicorn.run(my_app.app, host="127.0.0.1", port=8000, reload=True)
    
       
app = FastAPI()

@app.post("/")
async def open_docx(self,file: UploadFile = File(...)):
    """
        -taking docx file & return the document file
        -if any images include in the text file then return invalid
    """
    contents = await file.read()
    print(contents, 'line 54')
    texts=docx_to_text(contents)
    language = detect_language(texts)
    print(language, 'line 57')

    if language != 'en':
        return {"content ": 'doc_file is garbage language'}
    
    texts=DataTransformation(texts)
    cleaned_text=texts.clean_text()

    vectorizer=load_vectorizer()
    model=load_model()
    text_vector=vectorizer.transform([cleaned_text])
    topic=model.transform(text_vector)

    topic_index = topic.argmax()
    label='doc_file is {}'.format(LABELS[topic_index])
    
    return {
        'content':label
    }


# @app.get('/read')
# async def test_read():
#     try:
#         filename = 'test_resume_update.docx'

#         # Check if the file exists before attempting to open it
#         if not os.path.isfile(filename):
#             return {"error": "File not found"}

#         doc = docx.Document(filename)
#         full_text = []

#         for para in doc.paragraphs:
#             full_text.append(para.text)
            
#         text = ' '.join(full_text)

#         # Return a JSON response with the extracted text
#         return {
#             'name': 'sagor',
#             'address': 'Tangail',
#             'details': text
#         }
#     except Exception as e:
#         return {"error": str(e)}