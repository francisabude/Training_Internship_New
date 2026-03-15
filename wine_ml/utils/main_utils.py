import os
import sys

import numpy as np
import dill
import yaml
from pandas import DataFrame
from wine_ml.exception import WineException
from wine_ml.logger import logging


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise WineException(e, sys) from e