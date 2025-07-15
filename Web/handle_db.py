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
from datetime import date, datetime
import requests


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
MODULE_VERSION = "0.0.5"



class Book:
    """
    ### Class Book

    **Use:** Is used for easier access of individual columns of a database row in the books table

    **Fields:**
        id - int
        title - str
        author_ids - list
        publisher - str
        isbn - str
        edition - int
        year - int
        type - int
        tags - list
        room - str
        shelf - str
        lend - int
    """
    def __init__(self, title:str, author_ids:list[int], publisher:str, isbn:str, edition:int, year:int, type:int, tags:list, room:str, shelf:str, lend:int=-1, id:int=-1):
        self.id = id
        self.title = title
        self.author_ids = author_ids
        self.publisher = publisher
        self.isbn = isbn
        self.edition = edition
        self.year = year
        self.type = type
        self.tags = tags
        self.room = room
        self.shelf = shelf
        self.lend = lend

    def __str__(self):
        authors = [fetch_author_by_id(id).name for id in self.author_ids]
        return f"{self.id} {self.title} {authors} {self.publisher} {self.isbn} {self.edition} {self.year} {self.type} {self.tags} {self.room} {self.shelf} {self.lend}"


class Author:
    """
    **Class Author**

    **Use:** Is used for easier access of individual columns of a database row in the authors table

    **Fields:**
        id - int
        name - str
        has_nobel_prize - bool
        country - str
        birthdate - date
        date_of_death - date, default = 2200-01-01 ==> still alive
    """
    def __init__(self, id:int, name:str, has_nobel_prize:bool, country:str, birthdate:date, date_of_death:date="2200-01-01"):
        self.id = id
        self.name = name
        self.has_nobel_prize = has_nobel_prize
        self.country = country
        self.birthdate = birthdate
        self.date_of_death = date_of_death

    def __str__(self) -> str:
        return f"{self.name} {self.id} {self.birthdate} {self.country} {self.has_nobel_prize} {self.date_of_death if self.date_of_death else ''}"


class User:
    """
    ### Class User

    **Use:** Is used for easier access of individual columns of a database row in the users table

    **Fields:**
        - id - int
        - name - sr
        - pw_hash - str
        - favourite_authors - list of ints
        - favourite_books - list of ints

    """

    def __init__(self, id:int, name:str, pw_hash:str, favourite_authors:list[int], favorite_books:list[int]):
        self.id = id
        self.name = name
        self.pw_hash = pw_hash
        self.favourite_authors = favourite_authors
        self.favourite_books = favorite_books

    def __str__(self):
        return f"{self.id} {self.name} {self.favourite_authors} {self.favourite_books}"


def fetch_covers(books:list) -> list:
    covers = []
    # Iterates through all books in the books list
    for book in books:
        print(book.isbn)

        # Tries to get a cover for the book using the Google books request API
        try:

            # Querries the API
            url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{str(book.isbn)}" 
            print(url)
            req = requests.get(url)

            # Reads all available images for the book
            imageEntries = req.json()["items"][0]["volumeInfo"]["imageLinks"]

            # Creates a new empty list to store all the book cover links
            imageLinks = []

            # Iterates through all entries in the imageEntries dict
            for key, value in imageEntries.items():
                # Adds the link of the current entry to the imageLinks list
                imageLinks.append(value)

            # Tries to get the smallest cover
            cover = imageLinks[0]

        # If there is an error with the api or no book cover available
        except Exception:
            # Sets the cover to the noCover file
            cover = "./static/noCover.png"

        # Adds the current cover to the covers list
        covers.append(cover)

    return covers


def prepare_db() -> tuple[Connection, Cursor]:
    """
    ### Function prepare_db

    **Use:** Establishes a connection with the Database and creates a Cursor

    **Returns:** The Database Connection db and the Cursor cur

    **Parameters:** None
    """

    # Stores the new connection to the database in the db variable
    db = connect(DATABASE)

    # Stores the new cursor in the cur variable
    cur = db.cursor()

    # Returns the db and cur variables
    return db, cur


def fetch_authors() -> list[Author]:
    """
    ### Function fetch_authors

    **Use:** Gets all authors stored in the database

    **Returns:** A list of all authors stored in the database file

    **Parameters:** None
    """

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
        authors[index] = Author(id=author[0], name=author[1], has_nobel_prize=author[2], country=author[3], birthdate=datetime.strptime(author[4], '%Y-%m-%d').date(), date_of_death=datetime.strptime(author[5], '%Y-%m-%d').date() if author[5] else "")

    # Returns the fetched and converted authors
    return authors


def does_author_exist(name) -> bool:
    """
    ### Function does_author_exist
    
    **Use:** Checks if there is already an existing author with the provided name
    
    **Returns:** A boolean that indicates if there is already an author with the provided name
    
    **Parameters:** name - The name that should be checked
    
    """

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


def delete_author(name, security_key) -> bool:
    """
    ### Function delete_author

    **Use:** deletes the author with the given name if the security key is correct

    **Returns:** True if it deleted the user, else False

    **Parameters:**
        name - The name of the author to be deleted
        security_key - the key which is checked with the saved one to authorize the action
    """

    # If the security key parameter and the predefined one match
    if security_key == SECURITY_KEY:

        # Initializes the db connection
        db, cur = prepare_db()

        # Deletes the author from the db
        cur.execute(f"DELETE FROM authors WHERE author_name == ?;", (name))

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


def create_author(author:Author) -> bool:
    """"
    ### Function create_author

    **Use:** Creates a new author with the give parameters

    **Returns:** True if the author was created, otherwise False

    **Parameters:**
    author - an Author object containing the data of the new author
    """

    # If the author doesn't exist
    if not does_author_exist(author.name):

        # Initializes the db connection
        db, cur = prepare_db()

        if author.date_of_death:
            # The author is added to the db
            cur.execute(f"INSERT INTO authors (author_name, has_nobel_prize, author_country, date_of_birth, date_of_death) VALUES (?, ?, ?, ?, ?);", (author.name, author.has_nobel_prize, author.country, author.birthdate, author.date_of_death))
        else:
            # The author is added to the db
            cur.execute(f"INSERT INTO authors (author_name, has_nobel_prize, author_country, date_of_birth) VALUES (?, ?, ?, ?);", (author.name, author.has_nobel_prize, author.country, author.birthdate))

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


def edit_author(author_id:int, new:Author) -> bool:
    """"
    ### Function edit_author

    **Use:** Edits the details of the author with the provided name

    **Returns:** True if the author was updated or Else if he/she wasn't updated

    **Parameters:**
    id - the id of the author to edit
    new - an Author object with the updated data
    """

    # If the author exists
    if fetch_author_by_id(author_id):

        # Initializes the db connection
        db, cur = prepare_db()

        if new.date_of_death:
            # Updates the author's details
            cur.execute("""
            UPDATE authors
            SET author_name = ?, has_nobel_prize = ?, author_country = ?, date_of_birth = ?, date_of_death = ?
            WHERE author_id == ?;
            """, (new.name, new.has_nobel_prize, new.country, str(new.birthdate), str(new.date_of_death), author_id))
        else:
            cur.execute("""
            UPDATE authors
            SET author_name = ?, has_nobel_prize = ?, author_country = ?, date_of_birth = ?
            WHERE author_id == ?;
            """, (new.name, new.has_nobel_prize, new.country, str(new.birthdate), author_id))

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


# TODO: Finish commenting fetch_author_by_id function
def fetch_author_by_id(author_id:int) -> Author | bool:
    """
    ### Function fetch_author_by_id

    **Use:** Checks if there is an author with the provided id and returns it

    **Returns:**
    author - the data from the found author
    False if there isn't an author with the provided id

    **Parameters:**
    author_id - the id which should be searched for
    """

    # Creates a connection with the database
    db, cur = prepare_db()

    # Tries to get the author with the id specified in author_id
    author = cur.execute(f"SELECT * FROM authors WHERE author_id = {author_id};").fetchone()

    if author:

        author = Author(id=author[0], name=author[1], has_nobel_prize=author[2], country=author[3], birthdate=datetime.strptime(author[4], '%Y-%m-%d').date(), date_of_death=datetime.strptime(author[5], '%Y-%m-%d').date() if not author[5] else "")

        # If there is one that has the same id as passed to the function as parameter, author is an author object
        # else it is false
        return author
    else:

        return False


def fetch_author_by_name(name:str) -> Author:
    """
    ### Function fetch_author_by_name

    **Use:** gets an author with the specified name

    **Returns:** author - the Author that was found

    **Parameters:** name - the name of the Author to get
    """

    # Creates a connection with the database
    db, cur = prepare_db()

    # Tries to get the author with the author_name specified in name
    author = cur.execute(f"SELECT * FROM authors WHERE author_name == \"{name}\";").fetchone()

    # Converts it to an author object
    new_author = Author(id=author[0], name=author[1], has_nobel_prize=author[2], country=author[3], birthdate=datetime.strptime(author[4], '%Y-%m-%d').date(), date_of_death=datetime.strptime(author[5], '%Y-%m-%d').date() if author[5] else "")

    # Returns the author as an Author object
    return new_author


def fetch_author_names() -> list[str]:

    authors = fetch_authors()

    names = [author.name for author in authors]

    return names


def fetch_books() -> list[Book]:
    """
    ### Function fetch_books

    **Use:** Gets all books stored in the db

    **Returns:** All found books

    **Parameters:** None
    """

    # Initializes the db connection
    db, cur = prepare_db()

    # Fetches all books stored in the Database
    books = cur.execute("SELECT * FROM books;").fetchall()

    # Closes the cursor
    cur.close()

    # Closes the database connection
    db.close()

    new_books = []

    # Converts each book into a Book object
    for index in range(0, len(books)):
        book = books[index]
        new_books.append(Book(id=book[0], title=book[1], author_ids=eval(book[2]), publisher=book[3], isbn=book[4], edition=book[5], year=book[6], type=book[7], tags=eval(book[8]), room=book[9], shelf=book[10], lend=book[11]))

    # Returns all found books
    return new_books


def create_book(book:Book) -> str | int:
    """
    ### Function create_book

    **Use:** Creates a new book with the given parameters

    **Returns:**
    - the id of the new book, if it was created
    - otherwise an error message

    **Parameters:**
    - book - a Book object containing the data for the new book
    """

    # Initializes the db connection
    db, cur = prepare_db()

    authors_existing = True
    for id in book.author_ids:
        if not fetch_author_by_id(id):
            return f"Autor mit der ID {id} existier nicht!"


    # Creates the book with the provided parameters
    cur.execute(f"INSERT INTO books (book_title, author_ids, book_publisher, book_isbn, book_edition, book_year, book_type, book_tags, book_room, book_shelf, book_lend) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (book.title, str(book.author_ids), book.publisher, book.isbn, book.edition, book.year, book.type, str(book.tags), book.room, book.room, book.shelf, book.lend))

    # Commits the changes to the db
    db.commit()
 
    # Closes the cursor
    cur.close()

    # Closes the db connection
    db.close()

    id = fetch_book_by_isbn(book.isbn).id

    # Returns True, because the book was successfully created
    return id


def delete_book(book_id:int, security_key:str) -> bool:
    """"
    ### Function delete_book

    **Use:** Deletes the book with the provided name if the security key is correct

    **Returns:**
    -   True if the book was deleted
    -   False if the book couldn't be deleted

    **Parameters:**
    -   name - The name of the book to be deleted
    -   security_key - The security key to check if the user performing the action is an admin
    """

    # If the security key matches the predefined one and the book with the provided name does exist
    if security_key == SECURITY_KEY and fetch_book_by_id(book_id):

        # Initializes db connection
        db, cur = prepare_db()

        # Deletes the book from the db
        cur.execute(f"DELETE FROM books WHERE book_id = ?;", (book_id))

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


def edit_book(book_id:int, new:Book) -> str:
    """
    ### Function edit_book

    **Use:** Edits the book with the provided title

    **Returns:**
    - "OK" if the book was edited successfully
    - otherwise an error message

    **Parameters:**
    -   id - the id of the book to edit
    -   new - a Book object containing the new data for the book
    """

    authors_existing = True
    for id in new.author_ids:
        if not fetch_author_by_id(id):
            return f"Autor mit der ID {id} existiert nicht!"

    if not fetch_book_by_id(book_id):
        return f"Das Buch mit der ID {book_id} existier nicht!"

    # Initializes the db connection
    db, cur = prepare_db()

    # Updates the book
    cur.execute(f"""
UPDATE books
SET book_title = ?, author_ids = ?, book_publisher = ?, book_isbn = ?, book_edition = ?, book_year = ?, book_type = ?, book_tags = ?, book_room = ?, book_shelf = ?, book_lend = ?
WHERE book_id = ?;
    """, (new.title, str(new.author_ids), new.publisher, new.isbn, new.edition, new.year, new.type, str(new.tags), new.room, new.shelf, new.lend, book_id))

    # Commits the changes to the db
    db.commit()

    # Closes the cursor
    cur.close()

    # Closes the db connection
    db.close()

    # Returns True because the book was edited successfully
    return "OK"


def fetch_book_by_id(book_id:int) -> Book|bool:
    """
    ### Function fetch_book_by_id

    **Use:** Checks if there is a book with the provided id and returns it

    **Returns:**
    -   book - the data of the book if one was found
    -   False - if no book with the provided id was found

    **Parameters:**
    -   book_id - the id to search for
    """

    # Initializes the db connection
    db, cur = prepare_db()

    # Fetches one book from the db where the id is equals to the book_id parameter
    book = cur.execute(f"SELECT * FROM books WHERE book_id = ?;", (book_id, )).fetchone()

    # Turns the fetched book into a Book object
    new_book = Book(id=book[0], title=book[1], author_ids=eval(book[2]), publisher=book[3], isbn=book[4], edition=book[5],
                year=book[6], type=book[7], tags=eval(book[8]), room=book[9], shelf=book[10], lend=book[11])

    # Returns the found book
    return new_book


def fetch_book_by_isbn(isbn:str) -> Book:
    """
    ### Function fetch_book_by_isbn 

    **Use:** gets a book with the isbn provided as an argument

    **Returns:**
    - book - the found book as a Book object

    **Parameters:**
    - isbn - the isbn to search for
    """

    # Initializes the db connection
    db, cur = prepare_db()

    # Fetches one book from the db where the title is equals to the name parameter
    book = cur.execute(f"SELECT * FROM books WHERE book_isbn = ?;", (isbn)).fetchone()

    # Turns the fetched book into a Book object
    book = Book(id=book[0], title=book[1], author_ids=eval(book[2]), publisher=book[3], isbn=book[4], edition=book[5],
                year=book[6], type=book[7], tags=eval(book[8]), room=book[9], shelf=book[10], lend=book[11])

    # Returns the found book
    return book


def change_lend_state(book_id:int, user_id:int) -> bool:
    """
    ### Function change_lend_state

    **Use:** changes the lend state of a book

    **Returns:**
    - True if the lend state could be changed
    - False if it could not be changed

    **Parameters:**
    - book_id - the id of the book to process
    - user_id - the id of the user trying to change the lend state
    """

    # Prevents the program from crashing on error
    try:

        # Creates a database connection
        db, cur = prepare_db()

        # If the book is already lend
        if fetch_book_by_id(book_id).lend != -1:
            # Sets it new state to not lend (-1)
            newState = -1
        
        # If the book is not lend
        else:
            # Set it to be lend by the user with user_id
            newState = user_id

        # Changes the book in the database
        cur.execute(f"""UPDATE books SET book_lend = ? WHERE book_id = ?;""", (newState, book_id))

        # Closes the cursor
        cur.close()

        # commits the changes to the database
        db.commit()

        # Returns True because the operation was successful
        return True

    # If something went wrong
    except:
        # Return false, because the book could not be changed
        return False


def fetch_users() -> list[User]:
    """
    ### Function fetch_users

    **Use:** Retrieves a list of all users in the database

    **Returns:**
    - users - a list of the users in the database
    """

    # Creates a connection to the database
    db, cur = prepare_db()

    # Retrieves all users in raw form from the database
    raw_users = cur.execute("SELECT * FROM users;").fetchall()

    # Creates a list for the processed users
    users = []

    # Converts the raw users (lists) into instances of the User class
    for user in raw_users:
        users.append(User(user[0], user[1], user[2], eval(user[3]), eval(user[4])))

    # Returns the converted users
    return users


def fetch_user_names():
    """
    ### Function fetch_user_names

    **Use:** Retrieves a list with the names of all the users in the database

    **Returns:**
    - names - the list of all the users in the database
    """

    # Gets all the users in the database
    users = fetch_users()

    # Stores their names in a list
    names = [user.name for user in users]

    # And returns the list
    return names


def fetch_user_by_id(user_id:int) -> User|None:
    """
    ### Function fetch_user_by_id

    **Use**: tries to fetch a user with the provided id from the database

    **Returns:**
    - False if no user with the provided id was found
    - result - the user with the provided id

    **Parameters:**
    - user_id - the id that should be searched for
    """

    # Fetches all users from the database
    users = fetch_users()

    # The result will be false if no user with the user_id parameter was found
    result = False

    # Searches the users for the id
    for user in users:
        if user.id == user_id:
            # Updates the result to the found user and exits the loop
            result = user
            break

    
    # Returns the result of the operation    
    return result


"""
Main program loop
Is executed when the module is run as a standalone python script
Contains some information to be printed and is used for testing functions
"""
if __name__ == "__main__":
    print("-------------------------------------------")
    print("Executing file 'handle_db.py'")
    print("This file is executed as the main process")
    print("To start the webserver, please rub 'python app.py'!")
    print(f"Module version {MODULE_VERSION}")
    print("-------------------------------------------")
