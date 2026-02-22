import os
import pandas as pd
import pyodbc

from wine_ml.entity.config_entity import DataIngestionConfig
from wine_ml.entity.artifact_entity import DataIngestionArtifact
from wine_ml.logger import logging
from wine_ml.exception import WineException


class DataIngestion:
    def __init__(self, config: DataIngestionConfig=DataIngestionConfig()):
        self.config = config


    def ingest_data(self):

        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=LAPTOP-Q9V35JK6\SQLEXPRESS;"
            "DATABASE=ML;"
            "Trusted_Connection=yes;"
        )

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM wine_quality_classification")

        rows = cursor.fetchall()

        for row in rows:
            print(row)
        conn.close()

        


X = DataIngestion().ingest_data()
print(X)