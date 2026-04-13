import json
import sys
import yaml

import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset


from wine_ml.entity.config_entity import DataValidationConfig
from wine_ml.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from wine_ml.logger import logging
from wine_ml.exception import WineException
from wine_ml.constants import *
from wine_ml.constants import SCHEMA_FILE_PATH
from wine_ml.utils.main_utils import *
print([m for m in dir(Report) if not m.startswith('_')])



class DataValidation:
        def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
            """
            :param data_ingestion_artifact: Output reference of data ingestion artifact stage
            :param data_validation_config: configuration for data validation
            """
            try:
                self.data_ingestion_artifact = data_ingestion_artifact
                self.data_validation_config = data_validation_config
                self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
            except Exception as e:
                raise WineException(e,sys)

        def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
            try:
                schema_columns = [
                    list(col.keys())[0] if isinstance(col, dict) else col
                    for col in self._schema_config["columns"]
                ]
                status = len(dataframe.columns) == len(schema_columns)
                logging.info(f"Is required column present: [{status}]")
                return status
            except Exception as e:
                raise WineException(e, sys)
            
        def is_column_exist(self, df: DataFrame) -> bool:
            try:
                dataframe_columns = df.columns
                missing_numerical_columns = []
                missing_categorical_columns = []

                for column in self._schema_config["numerical_columns"]:
                    col_name = list(column.keys())[0] if isinstance(column, dict) else column
                    if col_name not in dataframe_columns:
                        missing_numerical_columns.append(col_name)

                if len(missing_numerical_columns) > 0:
                    logging.info(f"Missing numerical column: {missing_numerical_columns}")

                for column in self._schema_config["categorical_columns"]:
                    col_name = list(column.keys())[0] if isinstance(column, dict) else column
                    if col_name not in dataframe_columns:
                        missing_categorical_columns.append(col_name)

                if len(missing_categorical_columns) > 0:
                    logging.info(f"Missing categorical column: {missing_categorical_columns}")

                return False if len(missing_categorical_columns) > 0 or len(missing_numerical_columns) > 0 else True
            except Exception as e:
                raise WineException(e, sys) from e
            
        @staticmethod
        def read_data(file_path) -> DataFrame:
            try:
                return pd.read_csv(file_path)
            except Exception as e:
                raise WineException(e, sys)
            
            
        def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame) -> bool:
            try:
                report = Report([DataDriftPreset()])
                result = report.run(reference_data=reference_df, current_data=current_df)

                # Export methods are on the result, not the report
                json_report = json.loads(result.json())

                write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=json_report)

                n_features = json_report["metrics"][0]["result"]["number_of_columns"]
                n_drifted_features = json_report["metrics"][0]["result"]["number_of_drifted_columns"]

                logging.info(f"{n_drifted_features}/{n_features} drift detected.")
                drift_status = json_report["metrics"][0]["result"]["dataset_drift"]
                return drift_status
            except Exception as e:
                raise WineException(e, sys) from e
            
        def initiate_data_validation(self) -> DataValidationArtifact:
            """
            Method Name :   initiate_data_validation
            Description :   This method initiates the data validation component for the pipeline
            
            Output      :   Returns bool value based on validation results
            On Failure  :   Write an exception log and then raise an exception
            """

            try:
                validation_error_msg = ""
                logging.info("Starting data validation")
                train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                                    DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))

                status = self.validate_number_of_columns(dataframe=train_df)
                logging.info(f"All required columns present in training dataframe: {status}")
                if not status:
                    validation_error_msg += f"Columns are missing in training dataframe."
                status = self.validate_number_of_columns(dataframe=test_df)

                logging.info(f"All required columns present in testing dataframe: {status}")
                if not status:
                    validation_error_msg += f"Columns are missing in test dataframe."

                status = self.is_column_exist(df=train_df)

                if not status:
                    validation_error_msg += f"Columns are missing in training dataframe."
                status = self.is_column_exist(df=test_df)

                if not status:
                    validation_error_msg += f"columns are missing in test dataframe."

                validation_status = len(validation_error_msg) == 0

                if validation_status:
                    drift_status = self.detect_dataset_drift(train_df, test_df)
                    if drift_status:
                        logging.info(f"Drift detected.")
                        validation_error_msg = "Drift detected"
                    else:
                        validation_error_msg = "Drift not detected"
                else:
                    logging.info(f"Validation_error: {validation_error_msg}")
                    

                data_validation_artifact = DataValidationArtifact(
                    validation_status=validation_status,
                    message=validation_error_msg,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path
                )
                logging.info(f"Data validation artifact: {data_validation_artifact}")
                return data_validation_artifact
            except Exception as e:
                raise WineException(e, sys) from e
        
        
