import requests

from functools import wraps
from typing import Callable
import sys
import logging

TIMEOUT_EXCEPTION = "Time has been limit reached"
CONNECTION_EXCEPTION = "Connection hang out"
BAD_REQUEST_EXCEPTION = "Bad request"
INTERNAL_SERVER_EXCEPTION = "Internal Server Error"

class InterestFactException(Exception):
    ...

def create_default_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(f"lesson0/{name}.log", encoding='utf-8', mode='a')

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

logger = create_default_logger("JustMyLogger")

def log_and_handle_errors(func: Callable):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            exc_type, exc_value, _ = sys.exc_info()

            if exc_type:
                logger.error(f"Ошибка: {exc_value}")

            logger.exception(f"Исключение в функции {func.__name__}: {e}")
            raise e
    
    return wrapper

def get_interest_fact() -> str:
    url = "http://numbersapi.com/34"
    timeout = 10

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise InterestFactException(TIMEOUT_EXCEPTION)
    except requests.exceptions.ConnectionError:
        raise InterestFactException(CONNECTION_EXCEPTION)
    except requests.exceptions.HTTPError:
        raise InterestFactException(BAD_REQUEST_EXCEPTION)
    else:
        return response.text

@log_and_handle_errors
def count_word_in_interest_fact(word: str) -> int:
    try:
        word = word.lower()
        interest_fact = get_interest_fact()
        interest_fact = ' '.join([i.lower() for i in interest_fact.split(" ")])
        
        return interest_fact.count(word)
    except InterestFactException as e:
        raise e
    except Exception as e:
        raise InterestFactException(INTERNAL_SERVER_EXCEPTION)