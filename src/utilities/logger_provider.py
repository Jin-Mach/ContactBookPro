import logging
import pathlib
from logging.handlers import RotatingFileHandler


def get_logger() -> logging.Logger:
    log_path = pathlib.Path(__file__).parent.parent.joinpath("logs")
    log_path.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("ContactBookLogger")
    logger.setLevel(logging.WARNING)
    handler = RotatingFileHandler(log_path.joinpath("contact_book_logs"), maxBytes=5*1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s - %(funcName)s - %(lineno)d',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(handler)
    return logger