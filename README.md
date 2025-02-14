**Overview**

This project is a Python-based web scraper designed to extract book data from the website [Books to Scrape](http://books.toscrape.com/). The scraper collects information about books including their names, ratings, prices, and links to their individual pages, and saves this data into a CSV file.

**Features**

Extracts the following details for each book on the page:
Book Name
Rating (converted to numerical format: 1 to 5 stars)
Price
Link to the book's detail page
Saves the scraped data into a CSV file (books to scrape.csv).

**Requirements**

Python 3.x
The following Python libraries:
requests for making HTTP requests.
BeautifulSoup from bs4 for parsing HTML content.

`pip install beautifulsoup4`

`pip install requests`

