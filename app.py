import os
import sys
import certifi
import pandas as pd
from dotenv import load_dotenv
from urllib.parse import urlparse

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from uvicorn import run as app_run

import pymongo
from src.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME
from src.utils.main_util.url_feature_extractor import extract_features_from_url
from src.utils.ml_utils.model.estimater import NetworkModel
from src.utils.main_util.util import load_object
from src.pipeline.training_pipeline import TrainingPipeline
from src.exception import CustomException
from src.logger import logging



ca = certifi.where()
load_dotenv()

mongo_db_url = os.getenv("MONGO_DB_URL")
print(f"Connected Mongo URL: {mongo_db_url}")

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI(title="Network Security API", description="Detect phishing URLs using ML", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="./templates")


@app.get("/", tags=["Root"])
async def index():
    return RedirectResponse(url="/docs")

# TRAINING
@app.get("/train", tags=["Training"])
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Model training completed successfully!")
    except Exception as e:
        raise CustomException(e, sys)

# BATCH PREDICTION (CSV)
@app.post("/predict", tags=["Batch Prediction"])
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=model)

        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred

        df.to_csv("batch_test/output.csv", index=False)
        table_html = df.to_html(classes="table table-striped")

        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
    except Exception as e:
        raise CustomException(e, sys)

# SINGLE PREDICTION (URL AUTO FEATURE EXTRACTION)
@app.get("/predict_url", tags=["Single URL Prediction"])
async def predict_url(url: str):
    try:
        features = extract_features_from_url(url)
        if not features:
            return {"error": "Could not extract features from the provided URL"}

        df = pd.DataFrame([features])

        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=model)

        y_pred = network_model.predict(df)[0]
        status = "phishing" if y_pred == -1 else "legitimate"

        return {
            "url": url,
            "prediction": int(y_pred),
            "status": status,
            "extracted_features": features
        }

    except Exception as e:
        raise CustomException(e, sys)



if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)
