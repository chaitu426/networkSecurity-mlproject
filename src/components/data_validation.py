from src.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from src.entity.config_entity import DataValidationConfig
from src.exception import CustomException
from src.logger import logging
from src.constant.training_pipeline import SCHEMA_FILE_PATH
from src.utils.main_util.util import read_yaml_file, write_yaml_file

from scipy.stats import ks_2samp
import pandas as pd
import os, sys


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e, sys) from e

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys) from e

    def validate_number_of_columns(self, df: pd.DataFrame) -> bool:
        try:
            expected_cols = len(self._schema_config["columns"])
            actual_cols = len(df.columns)
            logging.info(f"Expected columns: {expected_cols}, Found: {actual_cols}")
            return expected_cols == actual_cols
        except Exception as e:
            raise CustomException(e, sys) from e

    def check_numerical_columns(self, df: pd.DataFrame) -> list:
        try:
            numerical_columns = self._schema_config["numerical_columns"]
            missing_cols = [col for col in numerical_columns if col not in df.columns]
            if missing_cols:
                logging.warning(f"Missing numerical columns: {missing_cols}")
            return missing_cols
        except Exception as e:
            raise CustomException(e, sys) from e

    def detect_data_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.05) -> bool:
        try:
            status = True
            report = {}

            for column in base_df.columns:
                if column not in current_df.columns:
                    continue
                stat, p_value = ks_2samp(base_df[column], current_df[column])
                drift_found = p_value < threshold
                if drift_found:
                    status = False
                report[column] = {"p_value": float(p_value), "drift_detected": drift_found}

            os.makedirs(os.path.dirname(self.data_validation_config.drift_report_file_path), exist_ok=True)
            write_yaml_file(self.data_validation_config.drift_report_file_path, report)

            return status
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("Starting data validation...")

            train_df = self.read_data(self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)

            if not self.validate_number_of_columns(train_df):
                raise CustomException("Train data column mismatch", sys)

            if not self.validate_number_of_columns(test_df):
                raise CustomException("Test data column mismatch", sys)

            if missing := self.check_numerical_columns(train_df):
                raise CustomException(f"Missing train numerical columns: {missing}", sys)

            if missing := self.check_numerical_columns(test_df):
                raise CustomException(f"Missing test numerical columns: {missing}", sys)

            drift_status = self.detect_data_drift(train_df, test_df)

            # Save validated data
            os.makedirs(os.path.dirname(self.data_validation_config.valid_train_file_path), exist_ok=True)
            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False)

            artifact = DataValidationArtifact(
                validation_status=True,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(f"✅ Data validation completed successfully: {artifact}")
            return artifact

        except Exception as e:
            raise CustomException(e, sys)
