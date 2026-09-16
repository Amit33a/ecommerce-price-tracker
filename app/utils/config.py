import os

from dotenv import load_dotenv


load_dotenv()


DEFAULT_TIMEOUT = int(
    os.getenv("DEFAULT_TIMEOUT", "10")
)

MAX_ATTEMPTS = int(
    os.getenv("MAX_ATTEMPTS", "4")
)

REQUEST_DELAY = int(
    os.getenv("REQUEST_DELAY", "1")
)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

RETRYABLE_STATUS_CODES = {429, 502, 503, 504}


def validate_config():
    if DEFAULT_TIMEOUT <= 0:
        raise ValueError("DEFAULT_TIMEOUT must be greater than 0")

    if MAX_ATTEMPTS <= 0:
        raise ValueError("MAX_ATTEMPTS must be greater than 0")

    if REQUEST_DELAY < 0:
        raise ValueError("REQUEST_DELAY cannot be negative")