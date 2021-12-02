from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
from classipy.transformers.json_to_model_transformer import JSONtoModelTransformer
from classipy.models.voting_classifier import CustomVotingClassifier

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

    #Transform DataFrame to Model ready DataFrame
    X = JSONtoModelTransformer().fit_transform(user_data_df)

    #Feed Model Ready Dataframe to Predictor
    custom_voting_classifier = CustomVotingClassifier(user_data_df)
    y_preds = custom_voting_classifier.predict(X)

    #Return JSON with ColumnNames and Predictions
    y_preds_as_json = pd.DataFrame({'column_names':user_data_df['column_name'],
                           'y_preds_decoded': y_preds
                                }).to_json()

    return y_preds_as_json


@app.get("/transform")
def transform():
    return dict(greeting="transform")
