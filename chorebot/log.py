import logging
from sys import stdout


def setup_logging():
    fmt = "%(asctime)s %(levelname)1.1s %(message)s"
    logging.basicConfig(format=fmt, level=logging.INFO, stream=stdout)
    logger = get_logger("chorebot")
    logger.info(" chorebot startup ".center(50, "="))


def get_logger(name):
    return logging.getLogger(name)
