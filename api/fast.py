from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import joblib
from classipy.models.heuristic import Heuristic

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
    user_data_json = await info.json()
    user_data_df = pd.DataFrame(user_data_json)
    print(user_data_df)
    #Get heusristic prediction
    heuristic_model = Heuristic()
    heuristic_pred = heuristic_model.test_dataset_heuristic(user_data_df)
    #heuristic_pred = heuristic_pred.to_frame()
    heuristic_pred = pd.DataFrame.to_json(heuristic_pred)
    #heuristic_pred = pd.DataFrame.to_json(user_data_df)


    #Get model prediction pipeline
    #pipeline = joblib.load('models.model')
    #Predict columns with models
    #model_pred = pipeline.predict(X)

    #Build result data frame by evaluating which pred is better (heuristic or model)
    #result_df =
    #for every row in heuristiv_pred and model_pred


    return heuristic_pred

@app.get("/transform")
def transform():
    return dict(greeting="transform")
