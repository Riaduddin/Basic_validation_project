from fastapi import File, UploadFile, FastAPI,HTTPException
from bas_val.component.data_transformation import DataTransformation
from bas_val.utils.main_utils import detect_language,load_model, load_vectorizer,docx_to_text
from bas_val.constant import LABELS
import os
from bas_val.logger import logging
from bas_val.utils.word_counts import FileOperation_word_count

app=FastAPI()

@app.post("/open-docx")
async def open_docx(file: UploadFile = File(...)):
    """
        -taking docx file & return the document file
        -if any images include in the text file then return invalid
    """
    contents = await file.read()
    texts=docx_to_text(contents)
    language = detect_language(texts)

    if language !='en':
        return {"content ": 'doc_file is garbage language'}
    texts=DataTransformation(texts)
    cleaned_text=texts.clean_text()

    vectorizer=load_vectorizer()
    model=load_model()
    text_vector=vectorizer.transform([cleaned_text])
    topic=model.transform(text_vector)

    topic_index = topic.argmax()
    label='doc_file is {}'.format(LABELS[topic_index])
    
    return {'content':label}


if __name__=='__main__':
    import uvicorn
    uvicorn.run(host="0.0.0.0", port=8000,reload=True)