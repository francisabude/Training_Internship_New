import json
import sys
import yaml

import pandas as pd
from evidently.model_profile import Profile #type: ignore
from evidently.model_profile.sections import DataDriftProfileSection #type:ignore

from wine_ml.entity.config_entity import DataValidationConfig
from wine_ml.entity.artifact_entity import DataIngestionArtifact
from wine_ml.logger import logging
from wine_ml.exception import WineException
from wine_ml.constants import *
from wine_ml.constants import SCHEMA_FILE_PATH
from wine_ml.utils.main_utils import *


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
        
        
