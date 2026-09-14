# E-commerce Price Tracker

A Python backend project for learning and building a production-oriented product price tracking application.

The project is being developed step by step, starting with web scraping fundamentals and gradually introducing backend engineering concepts such as HTTP clients, error handling, retries, rate limiting, testing, data storage, scheduling and APIs.

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

## HTTP Client

HTTP communication is centralised in:

```text
app/
├── scrapers/
│   └── books_scraper.py
│
└── utils/
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

Normal request pacing is currently controlled through:

```python
REQUEST_DELAY = 1
```

This introduces a delay between HTTP client calls to avoid making requests unnecessarily quickly during normal scraping.

The HTTP client returns:

```text
Response → successful request
None     → request ultimately failed
```

This keeps HTTP concerns separate from website-specific scraping logic.

## Scraper Architecture

The scraper separates HTTP communication, product URL discovery and product detail extraction.

```text
                    books_scraper.py
                           │
             ┌─────────────┴─────────────┐
             ↓                           ↓
      Listing page                  Product page
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

### Retryable HTTP failures

The following status codes are currently considered temporary:

```text
429 Too Many Requests
502 Bad Gateway
503 Service Unavailable
504 Gateway Timeout
```

These can be retried using exponential backoff.

### Non-retryable HTTP failures

For example:

```text
404 Not Found
```

is not automatically retried because repeatedly requesting a missing page is unlikely to fix the problem.

### Network failures

The HTTP client also handles:

* Connection errors
* Request timeouts

These can be retried because the failure may be temporary.

### Partial batch failures

If an individual product cannot be retrieved after the configured retry attempts, the scraper skips that product rather than adding invalid data such as `None` to the final results.

This allows the rest of the batch to continue processing.

## Rate Limiting

The project includes basic request rate limiting to make normal scraping more controlled and polite.

The delay is currently configured centrally in the HTTP client:

```python
REQUEST_DELAY = 1
```

This means the HTTP client waits before making each request.

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

The current implementation is intentionally simple and will be improved later if more advanced scheduling or request management becomes necessary.

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

The HTTP client has also been tested with:

```text
HTTP 200 → successful response
HTTP 503 → retry with exponential backoff
HTTP 404 → no retry
Invalid product → skipped without stopping the batch
Rate limiting → delay applied before HTTP requests
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
│   └── practice_rate_limit.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

`practice/` contains learning exercises and experiments, while `app/` contains the reusable project implementation.

The `practice/` directory is excluded from version control and is kept for learning and experimentation.

## Technologies Used

* Python
* Requests
* BeautifulSoup
* Git
* GitHub

More technologies will be added as the project develops, including:

* PostgreSQL
* pytest
* Docker
* Logging
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
