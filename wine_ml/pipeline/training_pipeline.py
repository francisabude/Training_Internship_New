from wine_ml.entity.config_entity import (DataIngestionConfig, DataValidationConfig)
from wine_ml.entity.artifact_entity import (DataIngestionArtifact, DataValidationArtifact)
from wine_ml.components.data_ingestion import DataIngestion
from wine_ml.components.data_validation import DataValidation
from wine_ml.constants import *
from wine_ml.exception import WineException
from wine_ml.logger import logging
import sys

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()

    def start_ingest_data(self) -> DataIngestionArtifact:
        """
        This method of TrainPipeline class is responsible for starting data ingestion component
        """
        try:
            logging.info("======Entered the start_data_ingestion method of TrainPipeline class======")
            logging.info("Getting the data from notebooks")
            data_ingestion = DataIngestion(config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.ingest_data()
            logging.info("Got the train_set and test_set from feature store")
            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )
            return data_ingestion_artifact
        except Exception as e:
            raise WineException(e, sys) from e
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        This method of TrainPipeline class is responsible for starting data validation component
        """
        logging.info("======Entered the start_data_validation method of TrainPipeline class======")

        try:
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=self.data_validation_config
                                             )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")
            logging.info("Exited the start_data_validation method of TrainPipeline class")
            return data_validation_artifact

        except Exception as e:
            raise WineException(e, sys) from e


    def run_pipeline(self) -> None:
        """
        This method of TrainPipeline class is responsible for running complete pipeline
        """
        try:
            data_ingestion_artifact = self.start_ingest_data()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
    
        
        except Exception as e:
            raise WineException(e, sys)