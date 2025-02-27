#
# handle_db.py
# ----------
# Book database Project
# (c)2025 Lars Lerchbacher
#

#
# Importing all needed modules, packages and libraries
#
# Imports:
# sqlite3 for the database handling and operations
# datetime datatype from the datetime module for timestamp handling
#
from sqlite3 import *
from datetime import date
#
# Defines all constants for the project
#
# Constants:
#   DATABASE - is used to store the filename for the database file
#   SECURITY_KEY - stores the security key that is used to authenticate an admin when deleting something
#   MODULE_VERSION - indicates the current version of the file
#
DATABASE = "database.sqlite"
SECURITY_KEY = "Alpha Delta Omicron 37 45 Blau"
MODULE_VERSION = "0.0.3"


#
# Class Book
#
# Is used for easier access of individual columns of a database row in the books table
#
class Book:
    def __init__(self, id:int, title:str, author_ids:list, publisher:str, isbn:str, edition:int, year:int, types:list, tags:list, room:str, shelf:str, lend:bool):
        self.id = id
        self.title = title
        self.author_ids = author_ids
        self.publisher = publisher
        self.isbn = isbn
        self.edition = edition
        self.year = year
        self.types = types
        self.tags = tags
        self.room = room
        self.shelf = shelf
        self.lend = lend


#
# Class Author
#
# Is used for easier access of individual columns of a database row in the authors table
#
class Author:
    def __init__(self, id:int, name:str, has_nobel_prize:bool, country:str, birthdate:date, date_of_death:date="2200-01-01"):
        self.id = id
        self.name = name
        self.has_nobel_prize = has_nobel_prize
        self.country = country
        self.birthdate = birthdate
        self.date_of_death = date_of_death


#
# Function prepare_db
#
# Use: Establishes a connection with the Database and creates a Cursor
#
# Returns: The db Object which is the Database Connection and the cur Object which is the Cursor
#
# Parameters: None
#
def prepare_db():

    # Stores the new connection to the database in the db variable
    db = connect(DATABASE)

    # Stores the new cursor in the cur variable
    cur = db.cursor()

    # Returns the db and cur variables
    return db, cur


#
# Function fetch_authors
#
# Use: Gets all authors stored in the database
#
# Returns: A list of all authors stored in the database file
#
# Parameters: None
#
def fetch_authors():

    # The db connections is initialized
    db, cur = prepare_db()

    # Fetches all the author from the db
    authors = cur.execute("SELECT * FROM authors;").fetchall()

    # Closes the cursor
    cur.close()

    # Closes the db connection
    db.close()

    # Loops through all authors in the authors list
    for index in range(0, len(authors)):
        author = authors[index]
        # Updates the list element at the current index to a new Author object with all the data filled in
        authors[index] = Author(id=author[0], name=author[1], has_nobel_prize=author[2], country=author[3], birthdate=author[4], date_of_death=author[5])

    # Returns the fetched and converted authors
    return authors


# TODO: Comment fetch_author_ids function
def fetch_author_ids():

    authors = fetch_authors()

    ids = []

    for author in authors:
        ids.append(author.id)
    
    return ids


# TODO: Comment fetch_author_ids function
def fetch_author_names():

    authors = fetch_authors()

    names = []

    for author in authors:
        names.append(author.name)
    
    return names


#
# Function does_author_exist
#
# Use: Checks if there is already an existing author with the provided name
#
# Returns: A boolean that indicates if there is already an author with the provided name
#
# Parameters: name - The name that should be checked
#
def does_author_exist(name):

    # Fetches all authors from the db
    authors = fetch_authors()

    # Creates the is_existent variable to store the checks result
    is_existent = False

    # Iterates over all authors in the db
    for author in authors:

        # If the authors name and the name parameter match
        if author.name == name:

            # The is_existent variable is set to True
            is_existent = True

            # Breaks out of the loop
            break

    # Returns if the authors is existent
    return is_existent


#
# Function delete_author
#
# Use: deletes the author with the given name if the security key is correct
#
# Returns: True if it deleted the user, else False
#
# Parameters:
#   name - The name of the author to be deleted
#   security_key - the key which is checked with the saved one to authorize the action
#
def delete_author(name, security_key):

    # If the security key parameter and the predefined one match
    if security_key == SECURITY_KEY:

        # Initializes the db connection
        db, cur = prepare_db()

        # Deletes the author from the db
        cur.execute(f"DELETE FROM authors WHERE author_name == '{name}';")

        # Commits the changes to the db
        db.commit()

        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()

        # Returns True because the author was deleted
        return True

    # If the security keys don't match
    else:

        # Returns False, because the action wasn't authenticated
        return False


#
# Function create_author
#
# Use: Creates a new author with the give parameters
#
# Returns: True if the author was created, otherwise False
#
# Parameters:
#   author - an Author object containing the data of the new author
#
def create_author(author:Author):

    # If the author doesn't exist
    if not does_author_exist(author.name):

        # Initializes the db connection
        db, cur = prepare_db()

        if author.date_of_death:
            # The author is added to the db
            cur.execute(f"INSERT INTO authors (author_name, has_nobel_prize, author_country, date_of_birth, date_of_death) VALUES ('{author.name}', {author.has_nobel_prize}, '{author.country}', '{author.birthdate}', '{author.date_of_death}');")
        else:
            # The author is added to the db
            cur.execute(f"INSERT INTO authors (author_name, has_nobel_prize, author_country, date_of_birth) VALUES ('{author.name}', {author.has_nobel_prize}, '{author.country}', '{author.birthdate}');")

        # Commits the changes to the db
        db.commit()

        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()

        # Returns True because the author was created successfully
        return True

    # If the author already exists
    else:

        # Returns False because you mustn't override an existing author to create a new one
        return False


#
# Function edit_author
#
# Use: Edits the details of the author with the provided name
#
# Returns: True if the author was updated or Else if he/she wasn't updated
#
# Parameters:
#   id - the id of the author to edit
#   new - an Author object with the updated data
#
def edit_author(id, new:Author):

    # If the author exists
    if fetch_author_by_id(id):

        # Initializes the db connection
        db, cur = prepare_db()

        # Updates the author's details
        cur.execute(f"""
UPDATE authors
SET author_name = '{new.name}', has_nobel_prize = {new.has_nobel_prize}, author_country = '{new.country}', date_of_birth = {new.birthdate}, date_of_death = {new.date_of_death}
WHERE author_id == {id};
""" if new.date_of_death else f"""
UPDATE authors
SET author_name = '{new.name}', has_nobel_prize = {new.has_nobel_prize}, author_country = '{new.country}', date_of_birth = {new.birthdate}
WHERE author_id == {id};
                    """)

        # Commits the changes to the db
        db.commit()

        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()

        # Returns True because the author was successfully edited
        return True

    # If the author doesn't exist
    else:

        # Returns False, because you can't alter the details of a not existing author
        return False


#
# Function fetch_author_by_id
#
# Use: Checks if there is an author with the provided id and returns it
#
# Returns:
#   author - the data from the found author
#   False if there isn't an author with the provided id
#
# Parameters:
#   author_id - the id which should be searched for
# TODO: Finish commenting fetch_author_by_id function
def fetch_author_by_id(author_id):

    db, cur = prepare_db()

    # Fetches all authors from the db
    author = cur.execute(f"SELECT * FROM authors WHERE author_id == {author_id};").fetchone()

    # Converts the fetched author into an Author object
    author = Author(id=author[0], name=author[1], has_nobel_prize=author[2], country=author[3], birthdate=author[4], date_of_death=author[5])

    return author


# TODO: Comment fetch_author_by_name function
def fetch_author_by_name(name):

    db, cur = prepare_db()

    author = cur.execute(f"SELECT * FROM authors WHERE author_name == '{name}';").fetchone()

    author = Author(id=author[0], name=author[1], has_nobel_prize=author[2], country=author[3], birthdate=author[4], date_of_death=author[5])

    return author


#
# Function fetch_books
#
# Use: Gets all books stored in the db
#
# Returns: All found books
#
# Parameters: None
#
def fetch_books():

    # Initializes the db connection
    db, cur = prepare_db()

    # Fetches all books stored in the Database
    books = cur.execute("SELECT * FROM books;").fetchall()

    # Closes the cursor
    cur.close()

    # Closes the database connection
    db.close()

    # Converts each book into a Book object
    for index in range(0, len(books)):
        book = books[index]
        books[index] = Book(id=book[0], title=book[1], author_ids=eval(book[2]), publisher=book[3], isbn=book[4], edition=book[5], year=book[6], types=eval(book[7]), tags=eval(book[8]), room=book[9], shelf=book[10], lend=book[11])

    # Returns all found books
    return books


#
# Function create_book
#
# Use: Creates a new book with the given parameters
#
# Returns:
#   True if the book was created
#   False if it wasn't created
#
# Parameters:
#   book - a Book object containing the data for the new book
#
def create_book(book:Book):

    # Initializes the db connection
    db, cur = prepare_db()

    authors_existing = True
    for id in book.author_ids:
        if not fetch_author_by_id(id):
            authors_existing = False

    # If there is an author with the selected author_id
    if authors_existing:

        # Creates the book with the provided parameters
        cur.execute(f"INSERT INTO books (book_title, author_ids, book_publisher, book_isbn, book_edition, book_year, book_types, book_tags, book_room, book_shelf, book_lend) VALUES ('{book.title}', '{book.author_ids}', '{book.publisher}', '{book.isbn}', {book.edition}, {book.year}, \"{book.types}\", \"{book.tags}\", '{book.room}', '{book.shelf}', {book.lend});")

        # Commits the changes to the db
        db.commit()

        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()

        # Returns True, because the book was successfully created
        return True

    # If there is no author with the provided author id
    else:
        return False


#
# Function delete_book
#
# Use: Deletes the book with the provided name if the security key is correct
#
# Returns:
#   True if the book was deleted
#   False if the book couldn't be deleted
#
# Parameters:
#   name - The name of the book to be deleted
#   security_key - The security key to check if the user performing the action is an admin
#
def delete_book(id, security_key):

    # If the security key matches the predefined one and the book with the provided name does exist
    if security_key == SECURITY_KEY and fetch_book_by_id(id):

        # Initializes db connection
        db, cur = prepare_db()

        # Deletes the book from the db
        cur.execute(f"DELETE FROM books WHERE book_id = {id};")

        # Commits the changes to the db
        db.commit()

        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()

        # Returns True because the book was successfully deleted
        return True

    # If the conditions for the deletion aren't met
    else:

        # Returns False, because the book couldn't be deleted
        return False


#
# Function edit_book
#
# Use: Edits the book with the provided title
#
# Returns:
#   True if the book was edited
#   False if it wasn't edited
#
# Parameters:
#   id - the id of the book to edit
#   new - a Book object containing the new data for the book
#
def edit_book(book_id:int, new:Book):

    authors_existing = True
    for id in new.author_ids:
        if not fetch_author_by_id(id):
            authors_existing = False

    # If the book exists and there is an author with the new id
    if fetch_book_by_id(book_id) and authors_existing:

        # Initializes the db connection
        db, cur = prepare_db()

        # Updates the book
        cur.execute(f"""
UPDATE books
SET book_title = '{new.title}', author_ids = '{new.author_ids}', book_publisher = '{new.publisher}', book_isbn = '{new.isbn}', book_edition = {new.edition}, book_year = {new.year}, book_types = \"{new.types}\", book_tags = \"{new.tags}\", book_room = '{new.room}', book_shelf = '{new.shelf}', book_lend = {new.lend}
WHERE book_id = {book_id};
        """)

        # Commits the changes to the db
        db.commit()

        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()

        # Returns True because the book was edited successfully
        return True

    # If the book doesn't exist or there is no author with the new id
    else:
        # Returns False because the book wasn't updated
        return


#
# Function fetch_book_by_id
#
# Use: Checks if there is a book with the provided id and returns it
#
# Returns:
#   book - the data of the book if one was found
#   False - if no book with the provided id was found
#
# Parameters:
#   book_id - the id to search for
#
def fetch_book_by_id(book_id:int):

    # Initializes the db connection
    db, cur = prepare_db()

    # Fetches one book from the db where the id is equals to the book_id parameter
    book = cur.execute(f"SELECT * FROM books WHERE book_id = {book_id};").fetchone()

    # Turns the fetched book into a Book object
    new_book = Book(id=book[0], title=book[1], author_ids=eval(book[2]), publisher=book[3], isbn=book[4], edition=book[5],
                year=book[6], types=eval(book[7]), tags=eval(book[8]), room=book[9], shelf=book[10], lend=book[11])

    # Returns the found book
    return new_book


def fetch_book_by_title(title:str):

    # Initializes the db connection
    db, cur = prepare_db()

    # Fetches one book from the db where the title is equals to the name parameter
    book = cur.execute(f"SELECT * FROM books WHERE book_title = '{title}';").fetchone()

    # Turns the fetched book into a Book object
    new_book = Book(id=book[0], title=book[1], author_ids=eval(book[2]), publisher=book[3], isbn=book[4], edition=book[5],
                year=book[6], types=eval(book[7]), tags=eval(book[8]), room=book[9], shelf=book[10], lend=book[11])

    # Returns the found book
    return new_book


def change_lend_state(id:int, state:bool):

    if fetch_book_by_id(id):

        db, cur = prepare_db()

        cur.execute(f"""UPDATE books
    SET book_lend = {state}
    WHERE book_id = {id};
    """)
        cur.close()

        db.commit()

        return True

    else:
        return False


#
# Main program loop
# Is executed when the module is run as a standalone python script
# Contains some information to be printed and is used for testing functions
#
if __name__ == "__main__":
    print("-------------------------------------------")
    print("Executing file 'handle_db.py'")
    print("This file is executed as the main process")
    print(f"Module version {MODULE_VERSION}")
    print("-------------------------------------------")
