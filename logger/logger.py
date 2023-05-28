
"""
Contains a function that specifies a logger for
every module(python file) where it's called from
"""

import logging

def get_logger(logger_name, file_name): 
    """
    Sets up loggers for the files where it's called from
    All the '.log' files are the 'logger' folder
    """

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    fh = logging.FileHandler(file_name)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
