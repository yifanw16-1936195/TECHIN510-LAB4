import os
import psycopg2
from psycopg2.extras import RealDictCursor
import requests
from bs4 import BeautifulSoup

def create_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title TEXT UNIQUE,
            price TEXT,
            rating TEXT,
            description TEXT
        )
    """)

def check_table_empty(cur):
    cur.execute("SELECT COUNT(*) FROM books")
    count = cur.fetchone()['count']
    return count == 0

def scrape_books():
    BASE_URL = 'https://books.toscrape.com/catalogue/'
    books = []

    for page in range(1, 51):
        url = f'{BASE_URL}page-{page}.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for book in soup.select('article.product_pod'):
            title = book.h3.a['title']
            price = book.select_one('p.price_color').text
            rating = book.select_one('p.star-rating')['class'][1]

            # Navigate to the product page to get the description
            product_url = BASE_URL + book.h3.a['href']
            product_response = requests.get(product_url)
            product_soup = BeautifulSoup(product_response.text, 'html.parser')

            description_element = product_soup.select('#product_description + p')
            description = description_element[0].text.strip() if description_element else 'No description available'

            books.append({
                'title': title,
                'price': price,
                'rating': rating,
                'description': description
            })

    return books

def store_books(cur, books):
    for book in books:
        price = book['price'].replace('Â', '').replace('£', '')
        cur.execute("""
            INSERT INTO books (title, price, rating, description)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (title) DO NOTHING""",
            (book['title'], price, book['rating'], book['description']))

def main():
    DATABASE_URL = os.environ('DATABASE_URL')
    con = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    cur = con.cursor()

    create_table(cur)

    if check_table_empty(cur):
        books = scrape_books()
        store_books(cur, books)
        print(f"{len(books)} books scraped and stored successfully!")
    else:
        print("Books have already been scraped. Skipping scraping.")

    con.commit()
    con.close()

if __name__ == '__main__':
    main()