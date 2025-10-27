# from src.components.data_ingetion import DataIngestion
# from src.components.data_validation import DataValidation
# from src.components.data_transformation import DataTransformation
# from src.components.model_trainer import ModelTrainer
# from src.exception import CustomException
# from src.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelTrainerConfig
# from src.entity.config_entity import TrainingPipelineConfig
# from src.logger import logging
# import sys

# if __name__ == "__main__":
#     try:
#         logging.info("")

#         trainingPipelineConfig = TrainingPipelineConfig()
#         dataingestionconfig = DataIngestionConfig(trainingPipelineConfig)
#         data_ingestion = DataIngestion(dataingestionconfig)

#         artifact = data_ingestion.initiate_data_ingestion()
#         print(artifact)
#         logging.info(f"Data Ingestion artifact: {artifact}")
#         data_validation_config = DataValidationConfig(trainingPipelineConfig)
#         data_validation = DataValidation(artifact,data_validation_config)
#         data_validation_artifact = data_validation.initiate_data_validation()
#         logging.info(f"Data Validation artifact: {data_validation_artifact}")

#         data_transformation_config = DataTransformationConfig(trainingPipelineConfig)
#         logging.info(f"Data Transformation confign: {data_transformation_config}")
#         data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
#         data_transformation_artifact = data_transformation.initiate_data_transformation()
#         logging.info(f"Data Transformation artifact: {data_transformation_artifact}")
#         print("data_transformation_artifact")

#         logging.info("model training started")
#         model_config = ModelTrainerConfig(trainingPipelineConfig)
#         Model_trainer = ModelTrainer(model_config, data_transformation_artifact)
#         model_trainer_artifact = Model_trainer.initiate_model_trainer()

#         logging.info(f"Model Trainer artifact: {model_trainer_artifact}")

#     except Exception as e:
#         raise CustomException(e, sys)
