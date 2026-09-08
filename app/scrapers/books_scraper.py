import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_books():
    url = "https://books.toscrape.com/"
    current_url = url
    all_book_details = []

    while current_url:
        response = requests.get(current_url, timeout=10)

        response.encoding = "utf-8"

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")

        for book in books:
          title = book.find("h3").find("a")["title"]
          price = book.find("p", class_="price_color").get_text(strip=True)
          availability = book.find("p", class_="instock").get_text(strip=True)
          product_url = urljoin(current_url, book.find("h3").find("a")["href"])

          book_details = {
            "title": title,
            "price": price,
            "availability": availability,
            "url": product_url
        }

          all_book_details.append(book_details)

        next_page = soup.find("li", class_="next")

        if next_page:
          next_url = next_page.find("a")["href"]
          current_url = urljoin(current_url, next_url)
        else:
          current_url = None

    return all_book_details     

books = scrape_books()

print("Total books:", len(books))
print(books[0])
