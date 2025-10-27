import os, sys
import numpy as py
import pandas as pd

## common constant 

TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "networkSecurity"
ARTIFACT_DIR: str ="Artifacts"
FILE_NAME:str = "phisingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILE_PATH: str = os.path.join("data_schema", "schema.yaml")

SAVED_MODEL_DIR: str = os.path.join("saved_models")
MODEL_FILE_NAME: str = "model.pkl"

## data ingestion related constants start with DATA_INGESTION_VAR name

DATA_INGESTION_COLLECTION_NAME: str = "demoCollection"
DATA_INGESTION_DATABASE_NAME: str = "demo"
DATA_INGESTION_DIR_NAME: str = "data_ingetion"
DATA_INGESTION_FEATURE_STORE_DIR: str ='feature_store'
DATA_INGESTION_INGESTED_DIR: str = 'ingestion'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION = str = 0.2

## data validation related constants start with DATA_VALIDATION_VAR name

DATA_VALIDATION_DIR_NAME: str = 'data_validation' # type: ignore
DATA_VALIDATION_VALID_DIR: str = "validated" # type: ignore
DATA_VALIDATION_INVALID_DIR: str = "invalid" # type: ignore
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report" # type: ignore
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml" # type: ignore
PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessing.pkl" # type: ignore


## data transformation related constants start with DATA_TRANSFORMATION_VAR name
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation" # type: ignore
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed" # type: ignore
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object" # type: ignore

DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": py.nan,
    "n_neighbors": 3,
    "weights": "uniform"
}

#model trainer related constants start with MODEL_TRAINER_VAR name
MODEL_TRAINER_DIR_NAME: str = "model_trainer" # type: ignore
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model" # type: ignore
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl" # type: ignore
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6 # type: ignore
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD: float = 0.05 # type: ignore