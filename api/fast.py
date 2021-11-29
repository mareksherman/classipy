from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import joblib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
@app.get("/")
def index():
    return dict(greeting="hello")

@app.get("/summary_predict")
def summary_predict(user_data):

    #Dataframe from streamlit:
    #X = pd.DataFrame()
    X = user_data

    #Get pipeline
    #pipeline = joblib.load('')

    #Predict columns
    #results = pipeline.predict(X)

    return user_data


@app.get("/transform")
def transform():
    return dict(greeting="transform")
