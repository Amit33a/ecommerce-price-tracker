# E-commerce Price Tracker

A Python backend project for learning and building a production-oriented product price tracking application.

The project is being developed step by step, starting with web scraping fundamentals and gradually introducing backend engineering concepts such as HTTP clients, error handling, retries, rate limiting, logging, configuration management, structured exceptions, testing, data storage, scheduling and APIs.

## Current Progress

### Stage 1 — Web Scraping Foundations

* [x] 1.1 Web Fundamentals
* [x] 1.2 Python `requests`
* [x] 1.3 BeautifulSoup
* [x] 1.4 Product Listing Page Scraping
* [x] 1.5 Individual Product Page Scraping
* [x] 1.6 Pagination
* [x] 1.7 Individual Product URLs
* [x] 1.8 Product Detail Pages
* [x] 1.9 HTTP Headers & User-Agent
* [x] 1.10 `requests.Session`
* [x] 1.11 Cookies & Session State
* [x] 1.12 Retry Strategy & Transient Network Failures
* [x] 1.13 Rate Limiting & Polite Scraping
* [x] 1.14 Logging
* [x] 1.15 Request Configuration & Environment Variables
* [x] 1.16 Structured HTTP Exceptions

## Current Implementation

The current scraper uses **Books to Scrape** as a practice website.

It can:

* Send HTTP requests using a reusable `requests.Session`
* Use shared HTTP headers
* Configure a User-Agent
* Configure request timeouts
* Apply a configurable request delay
* Handle HTTP errors
* Retry selected temporary HTTP failures
* Retry connection errors and timeouts
* Use exponential backoff between retry attempts
* Follow pagination automatically
* Handle relative URLs using `urljoin()`
* Discover individual product URLs
* Scrape individual product detail pages
* Separate product URL discovery from product detail scraping
* Extract product title, price, availability and rating
* Convert availability text into a numeric quantity
* Convert rating words into numeric values
* Handle failed product requests without stopping the entire batch
* Limit the number of products processed during testing
* Return structured product data as Python dictionaries
* Log HTTP activity and request failures using Python's `logging` module
* Load runtime configuration from environment variables
* Load local development configuration from a `.env` file
* Validate configuration before starting scraping
* Translate Requests-specific exceptions into application-specific exceptions
* Distinguish between timeout, connection, HTTP response and retry-exhaustion failures

## Configuration Management

Application configuration is centralised in:

```text
app/
├── scrapers/
│   └── books_scraper.py
│
└── utils/
    ├── config.py
    ├── exceptions.py
    └── http_client.py
```

The project uses environment variables to keep operational configuration separate from application logic.

Current configuration values include:

```text
DEFAULT_TIMEOUT
MAX_ATTEMPTS
REQUEST_DELAY
HEADERS
RETRYABLE_STATUS_CODES
```

The configuration layer provides default values for environment variables:

```python
DEFAULT_TIMEOUT = int(
    os.getenv("DEFAULT_TIMEOUT", "10")
)

MAX_ATTEMPTS = int(
    os.getenv("MAX_ATTEMPTS", "4")
)

REQUEST_DELAY = int(
    os.getenv("REQUEST_DELAY", "1")
)
```

Configuration is validated before the application starts:

```python
def validate_config():
    if DEFAULT_TIMEOUT <= 0:
        raise ValueError("DEFAULT_TIMEOUT must be greater than 0")

    if MAX_ATTEMPTS <= 0:
        raise ValueError("MAX_ATTEMPTS must be greater than 0")

    if REQUEST_DELAY < 0:
        raise ValueError("REQUEST_DELAY cannot be negative")
```

This allows the application to fail early when invalid configuration is supplied.

## Environment Configuration

Local development configuration is stored in a `.env` file.

Example:

```text
DEFAULT_TIMEOUT=10
MAX_ATTEMPTS=4
REQUEST_DELAY=3
```

The project uses `python-dotenv` to load these values into the environment.

The configuration flow is:

```text
.env
  ↓
python-dotenv
  ↓
Environment variables
  ↓
config.py
  ↓
Configuration validation
  ↓
Application
```

The real `.env` file is excluded from Git using `.gitignore`.

A safe `.env.example` file is included in the project to document the required configuration:

```text
DEFAULT_TIMEOUT=10
MAX_ATTEMPTS=4
REQUEST_DELAY=1
```

The `.env` file should not be committed to GitHub because it may contain environment-specific values or secrets in future stages.

## HTTP Client

HTTP communication is centralised in:

```text
app/
├── scrapers/
│   └── books_scraper.py
│
└── utils/
    ├── config.py
    ├── exceptions.py
    └── http_client.py
```

The scraper uses the reusable HTTP client instead of making direct HTTP requests throughout the scraping code.

The HTTP client currently provides:

* Shared User-Agent configuration
* Reusable `requests.Session`
* Request timeout
* Request rate limiting
* Retryable HTTP status handling
* Connection error handling
* Timeout handling
* Exponential backoff
* Maximum retry attempts
* Non-retryable HTTP error handling
* HTTP request logging
* Application-specific exception translation

Current retryable status codes:

```python
{429, 502, 503, 504}
```

The current retry schedule uses exponential backoff:

```text
Attempt 1 → wait 1 second
Attempt 2 → wait 2 seconds
Attempt 3 → wait 4 seconds
Attempt 4 → stop
```

Normal request pacing is controlled through:

```text
REQUEST_DELAY
```

The HTTP client waits before making each request to avoid unnecessarily rapid request patterns during normal scraping.

### HTTP Client Contract

The HTTP client follows a clear success/failure contract:

```text
Successful request
        ↓
return Response


Failed request
        ↓
raise application-specific exception
```

It no longer uses `None` to represent HTTP-client failures.

This makes failures explicit and gives the calling application useful information about what went wrong.

## Structured HTTP Exceptions

The project defines application-specific HTTP exceptions in:

```text
app/utils/exceptions.py
```

The exception hierarchy is:

```text
HTTPClientError
├── HTTPTimeoutError
├── HTTPConnectionError
├── HTTPResponseError
└── HTTPRetryExhaustedError
```

### `HTTPClientError`

Base exception for HTTP-client failures.

### `HTTPTimeoutError`

Raised when a request exceeds the configured timeout.

Example:

```text
Request timed out after 10 seconds for <url>
```

### `HTTPConnectionError`

Raised when a connection cannot be established.

The original Requests exception is preserved as the underlying cause.

### `HTTPResponseError`

Raised for non-retryable unsuccessful HTTP responses.

For example:

```text
404 Not Found
403 Forbidden
400 Bad Request
```

### `HTTPRetryExhaustedError`

Raised when a retryable HTTP failure continues after all configured attempts have been exhausted.

For example:

```text
503
 ↓
retry
 ↓
503
 ↓
retry
 ↓
503
 ↓
retry
 ↓
503
 ↓
HTTPRetryExhaustedError
```

This creates a clear boundary between the external `requests` library and the rest of the application.

The architecture is:

```text
Requests library
       ↓
Requests-specific exception
       ↓
http_client.py
       ↓
Application-specific exception
       ↓
Scraper/application
```

This reduces coupling between the scraper and the underlying HTTP library.

## Logging

The project uses Python's built-in `logging` module instead of relying on `print()` statements for operational HTTP messages.

Logging configuration is currently defined by the application entry point in `books_scraper.py`:

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
```

The HTTP client creates a module-specific logger:

```python
logger = logging.getLogger(__name__)
```

This allows log messages to identify the module that generated them.

Current logging levels are used as follows:

```text
INFO
    Normal HTTP activity

WARNING
    Temporary/retryable HTTP failures
    Retry attempts

ERROR
    Non-retryable request failures
    Timeouts
    Connection errors
    Exhausted retry attempts
```

Example successful request log:

```text
2026-09-15 21:26:44,669 | INFO | app.utils.http_client | HTTP 200: https://books.toscrape.com/
```

The project separates:

```text
Logger creation
      ↓
http_client.py

Logging configuration
      ↓
Application entry point
```

This prevents individual utility modules from controlling the application's global logging configuration.

## Scraper Architecture

The scraper separates HTTP communication, product URL discovery and product detail extraction.

```text
                    books_scraper.py
                           │
             ┌─────────────┴─────────────┐
             ↓                           ↓
       Listing page                 Product page
             │                           │
             └─────────────┬─────────────┘
                           ↓
                  request_with_retry()
                           │
                           ↓
                    http_client.py
                           │
                    requests.Session
                           │
                           ↓
                        Website
```

The product scraping flow is:

```text
Books listing pages
        ↓
scrape_books()
        ↓
Product URLs
        ↓
scrape_product_details()
        ↓
Detailed product dictionaries
```

The HTTP client is responsible for common HTTP behaviour such as:

```text
Headers
Session
Timeout
Rate limiting
Retry
Exponential backoff
Logging
Exception translation
```

The configuration module is responsible for:

```text
Environment variables
Default values
Configuration loading
Configuration validation
```

The exceptions module is responsible for:

```text
Application-specific HTTP error definitions
```

The scraper is responsible for website-specific behaviour such as:

```text
HTML parsing
Pagination
Product URL discovery
Product data extraction
```

This separation makes the scraper easier to test, maintain and extend as the project becomes more advanced.

## Error Handling

The project distinguishes between different types of failures.

### Retryable HTTP Failures

The following status codes are currently considered temporary:

```text
429 Too Many Requests
502 Bad Gateway
503 Service Unavailable
504 Gateway Timeout
```

These can be retried using exponential backoff.

### Non-Retryable HTTP Failures

For example:

```text
404 Not Found
```

is not automatically retried because repeatedly requesting a missing page is unlikely to fix the problem.

Other non-retryable HTTP responses are translated into `HTTPResponseError`.

### Network Failures

The HTTP client also handles:

* Connection errors
* Request timeouts

These are translated into application-specific exceptions.

### Retry Exhaustion

When a retryable HTTP failure continues after all configured attempts, the HTTP client raises:

```text
HTTPRetryExhaustedError
```

For example:

```text
HTTP 503
    ↓
Attempt 1
    ↓
Attempt 2
    ↓
Attempt 3
    ↓
Attempt 4
    ↓
HTTPRetryExhaustedError
```

### Configuration Failures

Invalid configuration is detected before scraping begins.

For example:

```text
REQUEST_DELAY=-1
```

causes configuration validation to fail before any HTTP requests are made.

This is an example of **fail-fast configuration validation**.

### Partial Batch Failures

If an individual product cannot be retrieved after the configured retry attempts, the scraper catches the application-level `HTTPClientError` and skips that product rather than adding invalid data such as `None` to the final results.

This allows the rest of the batch to continue processing.

## Rate Limiting

The project includes basic request rate limiting to make normal scraping more controlled and polite.

The delay is configured through:

```text
REQUEST_DELAY
```

Rate limiting and retry backoff serve different purposes:

```text
Rate limiting
      ↓
Controls normal request frequency


Retry backoff
      ↓
Controls waiting after temporary failures
      ↓
1 second → 2 seconds → 4 seconds
```

The project aims to avoid unnecessarily aggressive request patterns while developing responsible scraping behaviour.

The current implementation is intentionally simple and will be improved later if more advanced request management becomes necessary.

## Test Results

The scraper successfully discovered:

```text
Total books: 1000
```

Product detail scraping was successfully tested with 5 products.

Example detailed record:

```python
{
    "title": "A Light in the Attic",
    "price": "£51.77",
    "availability": "In stock (22 available)",
    "quantity": 22,
    "rating": 3,
    "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
}
```

The HTTP client has been tested with:

```text
HTTP 200 → successful response
HTTP 503 → retry with exponential backoff
HTTP 503 after all attempts → HTTPRetryExhaustedError
HTTP 404 → HTTPResponseError without retry
Connection failure → HTTPConnectionError
Timeout → HTTPTimeoutError
Invalid product → skipped without stopping the batch
Rate limiting → delay applied before HTTP requests
```

A controlled retry-exhaustion test using `httpbin.org/status/503` verified:

```text
Attempt 1 → HTTP 503
Attempt 2 → HTTP 503
Attempt 3 → HTTP 503
Attempt 4 → HTTP 503
        ↓
HTTPRetryExhaustedError
```

Configuration has been tested with:

```text
Environment variable → configuration loaded
.env → configuration loaded
Invalid REQUEST_DELAY → application stopped before HTTP requests
```

Logging has been verified for normal successful HTTP requests.

Example:

```text
INFO | app.utils.http_client | HTTP 200: https://books.toscrape.com/
```

## Project Structure

```text
ecommerce-price-tracker/
│
├── app/
│   ├── scrapers/
│   │   └── books_scraper.py
│   │
│   └── utils/
│       ├── config.py
│       ├── exceptions.py
│       └── http_client.py
│
├── practice/
│   ├── practice_requests.py
│   ├── practice_books_request.py
│   ├── practice_books_parse.py
│   ├── practice_books_pagination.py
│   ├── practice_headers.py
│   ├── practice_cookies.py
│   ├── practice_retry.py
│   ├── practice_environment.py
│   └── practice_retry_exhaustion.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

The local `.env` file is intentionally excluded from version control.

The `practice/` directory contains learning exercises and experiments, while `app/` contains the reusable project implementation.

## Technologies Used

* Python
* Requests
* BeautifulSoup
* Python `logging`
* python-dotenv
* Git
* GitHub

More technologies will be added as the project develops, including:

* PostgreSQL
* pytest
* Docker
* Scheduling
* REST APIs
* Data persistence
* Production configuration

## Development Approach

The project follows a milestone-based development process:

```text
Learn concept
      ↓
Practice concept
      ↓
Transfer useful implementation into app/
      ↓
Test implementation
      ↓
Refactor and document
      ↓
Git commit
      ↓
Move to next milestone
```

The goal is not simply to build a scraper, but to gradually turn the project into a professional backend application.

Future development will focus on making the system more reliable, testable, maintainable and suitable for real-world backend engineering.
