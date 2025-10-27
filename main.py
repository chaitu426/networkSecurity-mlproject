from src.components.data_ingetion import DataIngestion
from src.components.data_validation import DataValidation
from src.exception import CustomException
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig
from src.entity.config_entity import TrainingPipelineConfig
from src.logger import logging
import sys

if __name__ == "__main__":
    try:
        logging.info("")

        trainingPipelineConfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingPipelineConfig)
        data_ingestion = DataIngestion(dataingestionconfig)

        artifact = data_ingestion.initiate_data_ingestion()
        print(artifact)
        logging.info(f"Data Ingestion artifact: {artifact}")
        data_validation_config = DataValidationConfig(trainingPipelineConfig)
        data_validation = DataValidation(artifact,data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info(f"Data Validation artifact: {data_validation_artifact}")
        

    except Exception as e:
        raise CustomException(e, sys)
