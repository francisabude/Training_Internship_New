import os

ARTIFACT_DIR = "artifact"
MODEL_FILE_NAME = "model.pkl"
PIPELINE_NAME = "wine_ds"

TARGET_COLUMN = "quality_label"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
SCHEMA_FILE_PATH: str = os.path.join("config", "schema.yaml")
PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessing.pkl"

"""
Data Ingestion related constants
"""
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_INGESTED_DIR = "data_ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2