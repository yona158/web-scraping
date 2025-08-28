**Overview**

This project is a Python-based web scraper that extract book data from the website [Books to Scrape](http://books.toscrape.com/).

The scraper automatically traverses all pages, collects detailed information about each book, and allows filtering by price.

The results can be saved into both CSV and JSON formats.

**Features**

Scrapes across multiple pages starting from a given URL.

Extracts the following details for each book:

Book Name

Rating (converted into a numerical format: 1 to 5 stars)

Price

Link to the book's detail page

Filters results based on a minimum and maximum price range.

Saves the data into:

A CSV file

A JSON file (with UTF-8 encoding and pretty formatting)

Built-in logging with optional verbose mode


**Requirements**

Python 3.x

The following Python libraries:

requests → for making HTTP requests

beautifulsoup4 + lxml → for parsing HTML content

argparse → for command-line interface

dataclasses (standard in Python 3.7+)

Install requirements:

`pip install requests beautifulsoup4 lxml`


**Usage**

Run the scraper from the command line:

```
python scraper.py --start-url "http://books.toscrape.com/catalogue/category/books_1/index.html" \
                  --min-price 10 \
                  --max-price 50 \
                  --csv output.csv \
                  --json output.json \
                  --verbose
```

**Arguments**

--start-url → The URL of the first page to start scraping (default: books homepage).

--min-price → Minimum book price (optional).

--max-price → Maximum book price (optional).

--csv → Path to save results in CSV format (default: books.csv).

--json → Path to save results in JSON format (default: books.json).

--pause → Pause (in seconds) between requests (default: 0.5s).

--max-pages → Maximum number of pages to scrape (optional).

--verbose → Enable detailed logging (DEBUG mode).

**Output**
Example CSV file:
Name	Rating	Price	Link

A Light in the Attic	3	51.77	http://books.toscrape.com/a-light-in-the-attic_1000/index.html

Tipping the Velvet	1	53.74	http://books.toscrape.com/tipping-the-velvet_999/index.html

Example JSON file:
```
[
  {
    "name": "A Light in the Attic",
    "rating": 3,
    "price": 51.77,
    "link": "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
  },
  ...
]
```

**Disclaimer**
This project is for educational purposes only.
The target site Books to Scrape is a demo website specifically created for practicing web scraping.
