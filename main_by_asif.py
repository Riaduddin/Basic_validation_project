from fastapi import File, UploadFile, FastAPI, HTTPException
from bas_val.component.data_transformation import DataTransformation
from bas_val.utils.main_utils import detect_language, load_model, load_vectorizer, docx_to_text
from bas_val.constant import LABELS
from bas_val.logger import logging
from bas_val.utils.word_counts import FileOperation_word_count
from bas_val.utils.page_count_by_asif import convert_and_count_pages
from io import BytesIO
import os

app = FastAPI()

@app.post("/open-docx")
async def open_docx(file: UploadFile = File(...)):
    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Only DOCX files are allowed")

    try:
        #temp_dir = 'temp'
       # os.makedirs(temp_dir, exist_ok=True)
        #temp_file_path = os.path.join(temp_dir, file.filename)
        # with open(temp_file_path, 'wb') as f:
        #     f.write(await file.read())

        # Pass the file path to the convert_and_count_pages function
        page_count = convert_and_count_pages(temp_file_path)

        # Read the file content for further processing
        with open(temp_file_path, 'rb') as f:
            contents = BytesIO(f.read())

        texts = docx_to_text(contents)
        language = detect_language(texts)

        if language != 'en':
            return {"content": 'doc_file is in a non-English language'}

        word_counts = FileOperation_word_count(contents)
        counts = word_counts.file_process()

        texts = DataTransformation(texts)
        cleaned_text = texts.clean_text()

        vectorizer = load_vectorizer()
        model = load_model()
        text_vector = vectorizer.transform([cleaned_text])
        topic = model.transform(text_vector)

        topic_index = topic.argmax()
        label = 'doc_file is {}'.format(LABELS[topic_index])

        # Remove the temporary file
        os.remove(temp_file_path)

        return {'content': label,
                'Number of pages': page_count,
                'Number of words in the docx file': counts}
    except Exception as e:
        # Log the error for debugging
        logging.exception("Error processing DOCX file:")
        # Raise a detailed HTTP 500 error
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
