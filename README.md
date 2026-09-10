# E-commerce Price Tracker

A Python backend project for learning and building a product price tracking application.

The project is being developed step by step, starting with web scraping fundamentals.

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

## Current Implementation

The current scraper uses **Books to Scrape** as a practice website.

It can:

* Send HTTP requests using `requests`
* Handle HTTP errors using `raise_for_status()`
* Handle UTF-8 response encoding
* Parse HTML using BeautifulSoup
* Extract product information from individual product pages
* Follow pagination automatically
* Handle relative URLs using `urljoin()`
* Extract individual product URLs
* Separate product URL discovery from product detail scraping
* Extract product title, price, availability and rating
* Convert availability text into a numeric quantity
* Convert rating words into numeric values
* Handle request failures using `try/except`
* Limit the number of products processed during testing
* Return structured product data as Python dictionaries

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

The scraper also successfully handled an invalid product URL and reported the resulting HTTP 404 error without stopping the entire process.

## Project Structure

```text
ecommerce-price-tracker/
│
├── app/
│   └── scrapers/
│       └── books_scraper.py
│
├── practice/
│   ├── practice_requests.py
│   ├── practice_books_request.py
│   ├── practice_books_parse.py
│   └── practice_books_pagination.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

`practice/` contains learning exercises, while `app/` contains the professional implementation.

## Scraper Architecture

The scraper separates product URL discovery from product detail scraping.

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

This separation makes the scraper easier to test, maintain and extend as the project becomes more advanced.

## Technologies Used

* Python
* Requests
* BeautifulSoup
* Git

More technologies will be added as the project develops.
