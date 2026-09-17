import logging
import time

import requests

from app.utils.config import (
    DEFAULT_TIMEOUT,
    MAX_ATTEMPTS,
    REQUEST_DELAY,
    HEADERS,
    RETRYABLE_STATUS_CODES
)


from app.utils.exceptions import (
    HTTPClientError,
    HTTPConnectionError,
    HTTPTimeoutError,
    HTTPResponseError,
    HTTPRetryExhaustedError
)


logger = logging.getLogger(__name__)


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
                try:
                    response.raise_for_status()
                    return response
                except requests.HTTPError as error:
                    raise HTTPResponseError(
                        f"HTTP {response.status_code} for {url}"
                    ) from error

        except requests.Timeout as error:
            logger.error(
                f"Attempt {attempt}: timeout - {error}"
            )
            raise HTTPTimeoutError(
                f"Request timed out after {DEFAULT_TIMEOUT} seconds for {url}"
            ) from error

        except requests.ConnectionError as error:
            logger.error(
                f"Attempt {attempt}: connection error - {error}"
            )
            raise HTTPConnectionError(
                f"Failed to connect to {url}: {error}"
            ) from error


        except requests.RequestException as error:
            logger.error(
                f"Non-retryable request error: {error}"
            )
            raise HTTPClientError(
                f"HTTP request failed for {url}: {error}"
            ) from error

        
        if attempt < MAX_ATTEMPTS:
            wait_time = 2 ** (attempt - 1)

            logger.warning(
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)

        else:
            logger.error("All retry attempts failed.")
            raise HTTPRetryExhaustedError(
                f"All retry attempts failed for {url} "
                f"with HTTP {response.status_code}"
            )

