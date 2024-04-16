import os
import datetime
import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv()

con = psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=RealDictCursor)
cur = con.cursor()

def scrape_books():
    URL = 'https://books.toscrape.com/'
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    books = []
    for book in soup.select('article.product_pod'):
        title = book.h3.a['title']
        price = book.select_one('p.price_color').text
        rating = book.select_one('p.star-rating')['class'][1]
        description = book.select_one('p.product_description')
        description = description.text.strip() if description else 'No description available'

        books.append({
            'title': title,
            'price': price,
            'rating': rating,
            'description': description
        })

    return books

def store_books(books):
    for book in books:
        cur.execute("""
            INSERT INTO books (title, price, rating, description)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (title) DO NOTHING""",
            (book['title'], book['price'], book['rating'], book['description']))
    con.commit()

def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title TEXT UNIQUE,
            price TEXT,
            rating TEXT,
            description TEXT
        )
    """)
    con.commit()

st.title("Book Scraper")
st.subheader("A simple app to scrape and query book data")

create_table()

if st.button("Scrape Books"):
    books = scrape_books()
    store_books(books)
    st.success(f"{len(books)} books scraped and stored successfully!")

# Filtering and sorting options
search_query = st.text_input("Search by title or description")
min_price = st.number_input("Minimum price", min_value=0.0, value=0.0, step=0.01)
max_price = st.number_input("Maximum price", min_value=0.0, value=100.0, step=0.01)
rating_filter = st.selectbox('Filter by rating', ('All', 'One', 'Two', 'Three', 'Four', 'Five'))

# Applying the filter and sort query
cur.execute("""
    SELECT * FROM books
    WHERE (title ILIKE %s OR description ILIKE %s)
    AND CAST(REPLACE(price, '£', '') AS FLOAT) BETWEEN %s AND %s
    AND (%s = 'All' OR rating = %s)
    ORDER BY CAST(REPLACE(price, '£', '') AS FLOAT) ASC""",
    (f'%{search_query}%', f'%{search_query}%', min_price, max_price, rating_filter, rating_filter.lower()))

books = cur.fetchall()

# Displaying books
for book in books:
    with st.expander(f"{book['title']} - {book['price']}"):
        st.write(f"Rating: {book['rating'].capitalize()}")
        st.write(book['description'])