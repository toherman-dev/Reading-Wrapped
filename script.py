import requests
import json
import numpy as np
import statistics as st


def get_books(isbns):
    """ Return books given a list of ISBNs
    """
    books = [get_book(isbn) for isbn in isbns]

    return list(filter(None, books))


def get_book(isbn):
    """ Return dict with information about book given ISBN
    """

    url = "https://openlibrary.org/isbn/{}.json".format(isbn)
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    
def get_author_name(author_key):
    """ Return name of author given a author_key
    """
    
    name = ""
    url = "https://openlibrary.org{}.json".format(author_key)
    response = requests.get(url)
    
    try:
        name = response.json().get("name")
    except KeyError:
        pass

    return name


# Main Script

# open booklist file as "booklist"
with open("booklist") as booklist:
	books = booklist.read()

# remove linefeeds and whitespace
books = books.replace("\n", "")
books = books.replace(" ", "")

# split individual books into strings
books = books.split(",")

books_info = get_books(books)

# get titles
titles = np.array([book.get("title") for book in books_info])

# get pages
pages = [book.get("number_of_pages") for book in books_info]
pages = list(filter(None, pages))
pages = np.array(pages)

# get genres
genres = [book.get("genres") for book in books_info]
# remove NoneType elements
genres = list(filter(None, genres))
# flatten list to list of individual elements
genres = sum(genres,[])
genres = np.array(genres)

# get subjects
subjects = [book.get("subjects") for book in books_info]
subjects = list(filter(None, subjects))
subjects = sum(subjects,[])
subjects = np.array(subjects)

# get authors
authors = [book.get("authors") for book in books_info]
authors = list(filter(None, authors))
authors = sum(authors,[])
authors = [get_author_name(author.get("key")) for author in authors]
authors = np.array(authors)

# print the report
print("\nYour Reading Wrapped")
print("------------------------------")
print("These are the books you have read:")
for title in titles:
	print("-", title)
print("On average, you have read {0:0.2f} pages per book.".format(np.mean(pages)))
print("Your favorite author was {}.".format(st.mode(authors)))
print("Your favorite genre was {}.".format(st.mode(genres)))
print("Your favorite subject was {}.".format(st.mode(subjects)))


