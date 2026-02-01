import os

ARTIFACT_DIR = "artifact"
MODEL_FILE_NAME = "model.pkl"

TARGET_COLUMN = "quality_label"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
SCHEMA_FILE_PATH: str = os.path.join("config", "schema.yaml")
PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessing.pkl"

"""
Data Ingestion related constants
"""
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_NGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2