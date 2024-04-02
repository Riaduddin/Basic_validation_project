import os

DATABASE_NAME:str="bas_val"
LABELS: str=["garbage","valid"]

MODEL_DIR: str="model"

MODEL_NAME: str="lda_model.pkl"

MODEL_PATH: str=os.path.join(DATABASE_NAME,MODEL_DIR, MODEL_NAME)

VECTORIZER_NAME: str="count_vectorizer.pkl"

VECTORIZER_PATH: str=os.path.join(DATABASE_NAME,MODEL_DIR, VECTORIZER_NAME)