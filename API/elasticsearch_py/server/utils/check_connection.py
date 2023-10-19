import logging
from settings.constants import module_name

from elasticsearch import Elasticsearch

from elasticsearch.exceptions import (
    ConnectionError,
    NotFoundError,
    RequestError,
)


def check_connection(es: Elasticsearch) -> bool:
    logger = logging.getLogger(module_name)
    try:
        # Try to get info from Elasticsearch, which essentially checks the connection.
        es.info()
        return True
    except ConnectionError as e:
        logger.error(f"CONNECTION ERROR TRIGGERED: Make sure Elasticsearch is running!")
        raise e
    except NotFoundError as e:
        logger.error(f"NotFoundError: {e}", exc_info=True)
        raise e
    except RequestError as e:
        logger.error(f"NotFoundError: {e}", exc_info=True)
        raise e
    except Exception as e:
        # This is a catch-all for any other exceptions.
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        raise e
