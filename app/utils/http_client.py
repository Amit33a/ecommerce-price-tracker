import time

import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

RETRYABLE_STATUS_CODES = {429, 502, 503, 504}

DEFAULT_TIMEOUT = 10
MAX_ATTEMPTS = 4


session = requests.Session()

session.headers.update(HEADERS)


def request_with_retry(url):
    for attempt in range(1, MAX_ATTEMPTS + 1):

        try:
            response = session.get(
                url,
                timeout=DEFAULT_TIMEOUT
            )

            if response.status_code in RETRYABLE_STATUS_CODES:
                print(
                    f"Attempt {attempt}: "
                    f"HTTP {response.status_code}"
                )

            else:
                response.raise_for_status()
                return response

        except requests.Timeout as error:
            print(
                f"Attempt {attempt}: timeout - {error}"
            )

        except requests.ConnectionError as error:
            print(
                f"Attempt {attempt}: connection error - {error}"
            )

        except requests.RequestException as error:
            print(
                f"Non-retryable request error: {error}"
            )
            return None

        if attempt < MAX_ATTEMPTS:
            wait_time = 2 ** (attempt - 1)

            print(
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)

        else:
            print("All retry attempts failed.")

    return None 



