import logging
from pythonjsonlogger import jsonlogger


def init_logger(module_name: str) -> logging.Logger:
    logger = logging.getLogger(module_name)

    logHandler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(process)d] [%(levelname)s] [%(filename)s:%(lineno)d:%(funcName)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S %z",
    )
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    return logger


def init_json_logger(module_name: str) -> logging.Logger:
    logger = logging.getLogger(module_name)

    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    return logger
