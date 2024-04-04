from bas_val.component.data_transformation import DataTransformation
from bas_val.utils.main_utils import detect_language,load_model, load_vectorizer,docx_to_text
from bas_val.constant import LABELS
from bas_val.utils.word_counts import FileOperation_word_count
from bas_val.logger import logging

# import nltk
# nltk.download('punkt')


def checking(contents):
    texts=docx_to_text(contents)
    language = detect_language(texts)
    logging.info("language detection is completed")
    if language !='en':
        return {"content ": 'doc_file is garbage'}

    counts=FileOperation_word_count(contents)
    print('length of the texts: ',counts.file_process())

    texts=DataTransformation(texts)
    cleaned_text=texts.clean_text()

    

    vectorizer=load_vectorizer()
    model=load_model()
    text_vector=vectorizer.transform([cleaned_text])
    topic=model.transform(text_vector)

    topic_index = topic.argmax()
    label='doc_file is {}'.format(LABELS[topic_index])

    return label

file ='6373694492.docx'
print(checking(file))
            

