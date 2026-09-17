import logging

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.utils.http_client import request_with_retry
from app.utils.config import validate_config

from app.utils.exceptions import HTTPClientError


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


def scrape_product_details(product_url):
    try:
        response = request_with_retry(product_url)

    except HTTPClientError as error:
        logging.error(
            f"Failed to scrape {product_url}: {error}"
        )
        return None

    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").get_text(strip=True)
    price = soup.find("p", class_="price_color").get_text(strip=True)
    availability = soup.find("p", class_="instock").get_text(strip=True)
    available_quantity = int(availability.split()[2].replace("(", ""))
    rating = soup.find("p", class_="star-rating")["class"][1]

    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    rating = rating_map[rating]

    product_details = {
        "title": title,
        "price": price,
        "availability": availability,
        "quantity": available_quantity,
        "rating": rating,
        "url": product_url
    }

    return product_details


def scrape_books(max_products=None):
    url = "https://books.toscrape.com/"
    current_url = url
    product_urls = []

    while current_url:
        response = request_with_retry(current_url)

        response.encoding = "utf-8"

        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")

        for book in books:
            product_url = urljoin(
                current_url,
                book.find("h3").find("a")["href"]
            )

            product_urls.append(product_url)

            if max_products and len(product_urls) >= max_products:
                return product_urls

        next_page = soup.find("li", class_="next")

        if next_page:
            next_url = next_page.find("a")["href"]
            current_url = urljoin(current_url, next_url)
        else:
            current_url = None

    return product_urls


def main():
    validate_config()

    product_urls = scrape_books(max_products=5)

    all_product_details = []

    for product_url in product_urls:

        product_details = scrape_product_details(product_url)

        if product_details is not None:
            all_product_details.append(product_details)

    print("Total products:", len(all_product_details))

    if all_product_details:
        print(all_product_details[0])


if __name__ == "__main__":
    main()