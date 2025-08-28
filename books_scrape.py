from __future__ import annotations
import csv
import json
import time
import logging
import argparse
from dataclasses import dataclass, asdict
from typing import Iterable, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup




BASE = "http://books.toscrape.com/"
START_URL = urljoin(BASE, "catalogue/category/books_1/index.html")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; BooksScraper/1.0; +https://example.com)"
}
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


@dataclass
class Book:
    name: str
    rating: int
    price: float
    link: str


# --------------------------- Utilities ---------------------------

def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format="%(levelname)s | %(message)s",
        level=level
    )


def fetch(url: str, timeout: float = 15.0) -> Optional[BeautifulSoup]:
    """GET page and return BeautifulSoup object, or None on failure."""
    try:
        logging.debug(f"GET {url}")
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        return BeautifulSoup(resp.content, "lxml")
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None


def parse_price(price_text: str) -> float:
    """Convert '£53.74' -> 53.74 (float)."""
    cleaned = "".join(ch for ch in price_text if ch.isdigit() or ch == ".")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def parse_rating(tag) -> int:
    """Extract rating from star-rating class."""
    if not tag or "class" not in tag.attrs:
        return 0
    classes = tag["class"]
    for c in classes:
        if c in RATING_MAP:
            return RATING_MAP[c]
    return 0


def parse_books_from_page(soup: BeautifulSoup) -> List[Book]:
    """Parse all books from a single page soup."""
    books: List[Book] = []
    for art in soup.select("article.product_pod"):
        name = art.h3.a.get("title") or art.h3.a.text.strip()
        rating = parse_rating(art.select_one("p.star-rating"))
        price_text = art.select_one("p.price_color").text.strip()
        price = parse_price(price_text)

        relative_link = art.h3.a.get("href", "").replace("../../../", "catalogue/")
        link = urljoin(BASE, relative_link)

        books.append(Book(name=name, rating=rating, price=price, link=link))
    return books


def find_next_page(soup: BeautifulSoup, current_url: str) -> Optional[str]:
    """Return absolute URL of next page if exists, else None."""
    next_li = soup.select_one("li.next > a")
    if not next_li:
        return None
    href = next_li.get("href")
    return urljoin(current_url, href)


# --------------------------- Scraping ---------------------------

def scrape_all_pages(start_url: str, pause: float = 0.5, max_pages: Optional[int] = None) -> Iterable[Book]:
    """Iterate over all pages starting from start_url, yielding Book objects."""
    url = start_url
    page_count = 0
    while url:
        page_count += 1
        logging.info(f"[{page_count}] Scraping: {url}")
        soup = fetch(url)
        if not soup:
            logging.warning("Skipping page due to fetch error.")
            break

        yield from parse_books_from_page(soup)

        url = find_next_page(soup, url)

        if max_pages and page_count >= max_pages:
            logging.info(f"Reached max_pages={max_pages}, stopping.")
            break

        time.sleep(pause) 


def filter_by_price(books: Iterable[Book], min_price: Optional[float], max_price: Optional[float]) -> List[Book]:
    """Filter books by inclusive price range."""
    results: List[Book] = []
    for b in books:
        if (min_price is not None and b.price < min_price):
            continue
        if (max_price is not None and b.price > max_price):
            continue
        results.append(b)
    return results


# --------------------------- Output ---------------------------

def save_csv(books: List[Book], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Rating", "Price", "Link"])
        for b in books:
            writer.writerow([b.name, b.rating, b.price, b.link])
    logging.info(f"CSV saved: {path} ({len(books)} rows)")


def save_json(books: List[Book], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(b) for b in books], f, ensure_ascii=False, indent=2)
    logging.info(f"JSON saved: {path} ({len(books)} items)")

# --------------------------- CLI ---------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Scrape book data from Books to Scrape with pagination and price filtering."
    )
    p.add_argument("--min-price", type=float, default=None, help="Minimum price (inclusive).")
    p.add_argument("--max-price", type=float, default=None, help="Maximum price (inclusive).")
    p.add_argument("--csv", default="books.csv", help="Output CSV path. Default: books.csv")
    p.add_argument("--json", default="books.json", help="Output JSON path. Default: books.json")
    p.add_argument("--start-url", default=START_URL, help="Start URL (category index).")
    p.add_argument("--pause", type=float, default=0.5, help="Pause seconds between pages. Default: 0.5")
    p.add_argument("--max-pages", type=int, default=None, help="Limit number of pages (for testing).")
    p.add_argument("-v", "--verbose", action="store_true", help="Verbose logging.")
    return p.parse_args()


def main():
    args = parse_args()
    setup_logging(args.verbose)

    logging.info("Starting scrape...")
    all_books = list(scrape_all_pages(args.start_url, pause=args.pause, max_pages=args.max_pages))
    logging.info(f"Total scraped: {len(all_books)}")

    filtered = filter_by_price(all_books, args.min_price, args.max_price)
    logging.info(f"After price filter: {len(filtered)}")

    save_csv(filtered, args.csv)
    save_json(filtered, args.json)


    logging.info("Done.")


if __name__ == "__main__":
    main()
