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
requests for making HTTP requests.
BeautifulSoup from bs4 for parsing HTML content.

`pip install beautifulsoup4`

`pip install requests`

