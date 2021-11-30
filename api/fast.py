from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import joblib
from api.data-type-prediction.heuristic import test_dataset_heuristic


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

@app.post("/summary_predict")
async def summary_predict(info: Request):
    #Dataframe from streamlit:
    user_data = await info.json()

    #Get pipeline
    #pipeline = joblib.load('')

    #Predict columns
    #results = pipeline.predict(X)

    #return to streamlit
    return {"status": "SUCCESS", "data": user_data}

@app.get("/transform")
def transform():
    return dict(greeting="transform")
