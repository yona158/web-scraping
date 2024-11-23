from bs4 import BeautifulSoup
import requests
import csv

# To help us getting the rate by number
rating_conversion = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

min_price=input('Enter the minimum price of books : ')
max_price=input('Enter the maximum price of books : ')
print('Scraping...')
def find_books():
    # Request the webpage
    pageToScrape=requests.get("http://books.toscrape.com/catalogue/category/books_1/index.html")
    soup=BeautifulSoup(pageToScrape.content,'lxml')
    # Find all book articles
    books=soup.find_all("article",class_='product_pod')

    # open/creat a file to store data
    with open('books to scrape.csv','w') as file:
        writer=csv.writer(file)
        writer.writerow(['Name','Rating','Price','Link'])
        for book in books:
            price=book.find('p',class_='price_color').text
            # if min_price <= price <= max_price:
            # Extract the class that contains the star rating
            rating_tag = book.find('p', class_='star-rating')
            
            # Rating is the second element of the list of class attribute
            rating = rating_tag['class'][1] if rating_tag else 'No rating' 
            # Convert rating words to numbers
            stars = rating_conversion.get(rating, 0)
            # Get the book's name ,link and price
            book_name=book.h3.a.text
            more_info=book.h3.a['href']
            writer.writerow([book_name,stars,price,more_info])
    print("The process is done.")
    file.close()

find_books()

# if __name__=='__main__':     
#     while True:
#         find_books()
#         print("Waiting for 10 minutes...")
#         sleep(600)