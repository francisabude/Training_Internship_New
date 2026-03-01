import os
import pandas as pd
import pyodbc
import sys

from sklearn.model_selection import train_test_split

from wine_ml.entity.config_entity import DataIngestionConfig
from wine_ml.entity.artifact_entity import DataIngestionArtifact
from wine_ml.logger import logging
from wine_ml.exception import WineException
from wine_ml.constants import *


class DataIngestion:
    def __init__(self, config: DataIngestionConfig=DataIngestionConfig()):
        """
        configuration for th data ingstion
        """
        try:
            self.config = config
            logging.info(f"Data  Ingestion initialized with config {self.config}")
        except Exception as e:
            raise Exception(e, sys)


    def ingest_data(self):
        """
        Method to get data from the database
        """
        try:
            os.makedirs(os.path.dirname(self.config.training_file_path), exist_ok=True)
            
            logging.info("Starting the data ingestion process from the DB...")
            # Getting data from the database
            conn = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={SERVER};"
                f"DATABASE={DATABASE};"
                f"Trusted_Connection=yes;"
            )

            query = f"SELECT * FROM {TABLE}"
            df = pd.read_sql(query, conn)
            conn.close()
            logging.info(f"Data of {df.shape} rows and columns successfully loaded from the database...")


            # Split data into train and test 
            train_df, test_df = train_test_split(
                df,
                test_size = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO,
                random_state=42
            )
            logging.info("Train Test splitting mechanism successfully done.")

            # Save splitted files into their directory
            train_df.to_csv(self.config.training_file_path, index=False)
            test_df.to_csv(self.config.testing_file_path, index=False)

            # Artifact foldder
            artifact = DataIngestionArtifact(
                trained_file_path=self.config.training_file_path,
                test_file_path=self.config.testing_file_path
            ) 
            logging.info("Data succesfully splitted into artifact directory..")
            return artifact
    


        except Exception as e:
            raise Exception(e, sys)

        


X = DataIngestion().ingest_data()
print(X)