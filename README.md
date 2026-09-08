# E-commerce Price Tracker

A Python backend project for learning and building a product price tracking application.

The project is being developed step by step, starting with web scraping fundamentals.

## Current Progress

### Stage 1 — Web Scraping Foundations

* [x] Web fundamentals
* [x] Python `requests`
* [x] BeautifulSoup
* [x] Product listing page scraping
* [x] Individual product page scraping
* [x] Pagination

## Current Implementation

The current scraper uses **Books to Scrape** as a practice website.

It can:

* Send HTTP requests using `requests`
* Parse HTML using BeautifulSoup
* Extract product title, price and availability
* Follow pagination automatically
* Handle relative URLs using `urljoin()`
* Collect scraped products as Python dictionaries
* Return the collected product data

### Test Result

The scraper successfully collected:

```text
Total books: 1000
```

Example record:

```python
{
    "title": "A Light in the Attic",
    "price": "£51.77",
    "availability": "In stock"
}
```

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

## Technologies Used

* Python
* Requests
* BeautifulSoup
* Git

More technologies will be added as the project develops.
