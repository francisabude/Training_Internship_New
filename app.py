from wine_project.logger import logging
from wine_project.exception import WineException


logging.info("This is our first log")
try:
    x = 1/0
except WineException as e:
    logging.info(e)

logging.info("X value has been calculated")