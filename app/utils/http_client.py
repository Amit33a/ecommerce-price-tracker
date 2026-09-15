import logging
import time

import requests


logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

RETRYABLE_STATUS_CODES = {429, 502, 503, 504}

DEFAULT_TIMEOUT = 10
MAX_ATTEMPTS = 4
REQUEST_DELAY = 1


session = requests.Session()

session.headers.update(HEADERS)


def request_with_retry(url):

    time.sleep(REQUEST_DELAY)

    for attempt in range(1, MAX_ATTEMPTS + 1):

        try:
            response = session.get(
                url,
                timeout=DEFAULT_TIMEOUT
            )

            logger.info(
                f"HTTP {response.status_code}: {url}"
            )

            if response.status_code in RETRYABLE_STATUS_CODES:
                logger.warning(
                    f"Attempt {attempt}: "
                    f"HTTP {response.status_code}"
                )

            else:
                response.raise_for_status()
                return response

        except requests.Timeout as error:
            logger.error(
                f"Attempt {attempt}: timeout - {error}"
            )

        except requests.ConnectionError as error:
            logger.error(
                f"Attempt {attempt}: connection error - {error}"
            )

        except requests.RequestException as error:
            logger.error(
                f"Non-retryable request error: {error}"
            )
            return None

        if attempt < MAX_ATTEMPTS:
            wait_time = 2 ** (attempt - 1)

            logger.warning(
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)

        else:
            logger.error("All retry attempts failed.")

    return None 

