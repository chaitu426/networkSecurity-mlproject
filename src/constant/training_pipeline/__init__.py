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

## data ingestion related constants start with DATA_INGESTION_VAR name

DATA_INGESTION_COLLECTION_NAME: str = "demoCollection"
DATA_INGESTION_DATABASE_NAME: str = "demo"
DATA_INGESTION_DIR_NAME: str = "data_ingetion"
DATA_INGESTION_FEATURE_STORE_DIR: str ='feature_store'
DATA_INGESTION_INGESTED_DIR: str = 'ingestion'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION = str = 0.2