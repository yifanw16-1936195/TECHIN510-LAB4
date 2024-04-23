# TECHIN 510 Lab 4: Accessing Web Resources with Python

## Author: Yifan Wang

## Hosted Link

[Book Scraper](https://techin510-lab4.streamlit.app/)
[Weather App](https://techin510-lab4-weather.streamlit.app/)

## Overview

This lab focuses on creating a web scraper using Python and BeautifulSoup to extract book data from the website "https://books.toscrape.com/". The scraped data is then stored in a PostgreSQL database and displayed in a Streamlit web app. Users can search, filter, and sort the scraped book data based on various criteria.

## Features

- Web Scraping: The app scrapes book data from all 50 pages of "https://books.toscrape.com/", extracting information such as title, price, rating, and description.
- Database Storage: The scraped book data is stored in a PostgreSQL database, ensuring persistent storage and efficient retrieval.
- Search Functionality: Users can search for books by title or description, making it easy to find specific books.
- Filtering: Books can be filtered based on price range and rating, allowing users to narrow down their search results.
- Sorting: The app supports sorting books by price in ascending order, enabling users to view books from lowest to highest price.
- Scraping Control: The app prevents unnecessary scraping by checking if the database already contains book data. If data exists, the scraping button is disabled, and users are informed accordingly.

## Reflections

Learning to use BeautifulSoup for web scraping offered invaluable insights into HTML structure analysis, element selection, and adapting to varied page layouts. This project involved navigating multiple pages and extracting data such as book descriptions, highlighting the importance of understanding website navigation and pagination. Cleaning and transforming the scraped data, including price adjustments and managing missing descriptions, was crucial for data integrity. Integrating this data with a PostgreSQL database underscored the importance of database management skills, such as creating tables and handling data insertion. Moreover, developing a Streamlit app with functionalities for search, filtering, and sorting using dynamic SQL queries demonstrated how database interactions can enhance user experiences. Adding controls to minimize unnecessary scraping and improve user feedback further emphasized efficient resource use and user interface design in web scraping projects, providing a comprehensive understanding of the practical applications of data extraction, storage, and presentation.
