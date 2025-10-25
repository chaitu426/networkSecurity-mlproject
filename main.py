from src.components.data_ingetion import DataIngestion
from src.exception import CustomException
from src.entity.config_entity import DataIngestionConfig
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
    except Exception as e:
        raise CustomException(e, sys)
