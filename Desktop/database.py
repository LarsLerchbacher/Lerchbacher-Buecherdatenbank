#
# Desktop/database.py and Web/database.py (symlink)
# ----------
#
#   The Lerchbacher book database project
#   © Lars Lerchbacher 2025-2026
#
#   This file is part of the Lerchbacher book database
#
#   The Lerchbacher book database is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation,
#   either version 3 of the License, or (at your option) any later version.
#
#   The Lerchbacher book database is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#   See the GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License along with the Lerchabcher book database. If not, see <https://www.gnu.org/licenses/>. 
#


#
# Importing all needed modules, packages and libraries
#
import app_context
from datetime import date, datetime
from images import get_image
import requests
from sqlite3 import *
import os


#
# Defines all constants for the project
#
# Constants:
#   DATABASE - is used to store the filename for the database file
#
DATABASE = "database.sqlite"



class Book:
    """
    ### Class Book

    **Use:** Is used for easier access of individual columns of a database row in the books table

    **Fields:**
        id - int
        title - str
        language - str
        publisher - str
        isbn - str
        edition - int
        year - int
        book_type - int
        tags - list
        room - str
        shelf - str
        lend - int
        lend_to - str
    """
    def __init__(self, title:str, author_ids:list[int], language:str, publisher:str, isbn:str, edition:int, year:int, book_type:int, tags:list, room:str, shelf:str, lend_to: str, lend:int=-1, id:int=-1):
        self.id = id
        self.title = title
        self.author_ids = author_ids
        if language:
            self.language = str(language)
        else:
            self.language = "Unbekannt"
        self.publisher = publisher
        self.isbn = isbn
        self.edition = edition
        self.year = year
        self.book_type = book_type
        self.tags = tags
        self.room = room
        self.shelf = shelf
        self.lend = lend
        self.lend_to = lend_to

    def __str__(self):
        authors = [fetch_author(id).getName() for id in self.author_ids]
        return f"{self.id},, {self.title},, {authors},, {self.publisher},, {self.isbn},, {self.edition},, {self.year},, {self.book_type},, {self.tags},, {self.room},, {self.shelf},, {self.lend},, {self.lend_to},, {self.language}"


class Author:
    """
    **Class Author**

    **Use:** Is used for easier access of individual columns of a database row in the authors table

    **Fields:**
        id - int
        firstName - str
        lastName - str
    """
    def __init__(self, id:int, firstName:str, lastName:str):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName

    def __str__(self) -> str:
        return f"{self.id},, {self.firstName},, {self.lastName}"

    def getName(self) -> str:
        return self.firstName + " " + self.lastName


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
    app_context.logger.info("Fetching all authors from the database")
    db, cur = prepare_db()

    try:
        # Fetches all the author from the db
        authors = cur.execute("SELECT * FROM authors ORDER BY lastName ASC;").fetchall()
        
        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()

        # Loops through all authors in the authors list
        for index in range(0, len(authors)):
            author = authors[index]
            # Updates the list element at the current index to a new Author object with all the data filled in
            authors[index] = Author(id=author[0], firstName=author[1], lastName=author[2])
        # Returns the fetched and converted authors
        app_context.logger.debug(f"Fetched {len(authors)} authors")
        return authors
    except Exception as e:
        app_context.logger.error(f"Failed to fetch authors: {e}")
        raise


def search_authors(string: str) -> list[Author]:
    """
    ### Function fetch_authors

    **Use:** Gets all authors that contain the given str

    **Returns:** A list of all authors stored in the database file

    **Parameters:**
    - string: the string to search for
    """

    # The db connections is initialized
    db, cur = prepare_db()

    # Fetches all the author from the db
    authors = cur.execute("SELECT * FROM authors WHERE firstName LIKE ? OR lastName LIKE ? ORDER BY lastName ASC;", (f"%{string}%", f"%{string}%")).fetchall()

    # Closes the cursor
    cur.close()

    # Closes the db connection
    db.close()

    # Loops through all authors in the authors list
    for index in range(0, len(authors)):
        author = authors[index]
        # Updates the list element at the current index to a new Author object with all the data filled in
        authors[index] = Author(id=author[0], firstName=author[1], lastName=author[2])
    # Returns the fetched and converted authors
    return authors


def delete_author(id) -> bool:
    """
    ### Function delete_author

    **Use:** deletes the author with the given name if the security key is correct

    **Returns:** True if it deleted the author, else False

    **Parameters:**
        name - The name of the author to be deleted
    """


    # Initializes the db connection
    db, cur = prepare_db()

    # Deletes the author from the db
    cur.execute(f"DELETE FROM authors WHERE author_id == ?;", (id,))

    # Commits the changes to the db
    db.commit()

    # Closes the cursor
    cur.close()

    # Closes the db connection
    db.close()

    # Returns True because the author was deleted
    return True


def create_author(author:Author) -> str | bool | Exception:
    """"
    ### Function create_author

    **Use:** Creates a new author with the give parameters

    **Returns:** True if the author was created, otherwise False

    **Parameters:**
    author - an Author object containing the data of the new author
    """
    try:

        # Initializes the db connection
        db, cur = prepare_db()

        # The author is added to the db
        cur.execute(f"INSERT INTO authors (firstName, lastName) VALUES (?, ?);", (author.firstName, author.lastName))
        # Commits the changes to the db
        db.commit()

        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()

        # Returns True because the author was created successfully
        return "OK"

    # If an error occurs, return it, so it can be displayed
    except Exception as e:

        return e


def edit_author(author_id:int, new:Author) -> str | bool | Exception:
    """"
    ### Function edit_author

    **Use:** Edits the details of the author with the provided name

    **Returns:** True if the author was updated or Else if he/she wasn't updated

    **Parameters:**
    id - the id of the author to edit
    new - an Author object with the updated data
    """

    try:

        # Initializes the db connection
        db, cur = prepare_db()

        # Updates the author's details
        cur.execute("UPDATE authors SET firstName = ?, lastName = ? WHERE author_id == ?;", (new.firstName, new.lastName, author_id))
        
        # Commits the changes to the db
        db.commit()

        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()

        # Returns True because the author was successfully edited
        return "OK"

    # If an error occurs, return it, so it can be displayed
    except Exception as e:

        return e


def fetch_author(author_id:int) -> Author | bool:
    """
    ### Function fetch_author

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
    author = cur.execute(f"SELECT * FROM authors WHERE author_id = ?;", (author_id,)).fetchone()

    if author:
        author = Author(id=author[0], firstName=author[1], lastName=author[2])

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

    nameParts = name.split(" ")
    lastName = nameParts[-1]
    firstName = " ".join(nameParts[:-1])

    # Tries to get the author with the author_name specified in name
    author = cur.execute(f"SELECT * FROM authors WHERE firstName == ? AND lastName == ?;", (firstName, lastName)).fetchone()

    # Converts it to an author object
    new_author = Author(id=author[0], firstName=author[1], lastName=author[2])

    # Returns the author as an Author object
    return new_author

def fetch_author_ids() -> list[int]:

    db, cur = prepare_db()
    
    ids = [ row[0] for row in cur.execute("SELECT author_id FROM authors;").fetchall() ]

    return ids


def fetch_author_names() -> list[str]:

    authors = fetch_authors()

    names = [author.firstName + " " + author.lastName for author in authors]

    return names


def fetch_authors_for_book(book_id: int) -> list[int]:

    db, cur = prepare_db()

    authors = [ row[0] for row in cur.execute("SELECT abAuthorID FROM author_books WHERE abBookID = ?;", (book_id,)).fetchall() ]

    # results are packed in lists/tuples
    ids = []
    for author in authors:
        ids.append(fetch_author(author))

    cur.close()
    db.close()

    return ids 


def fetch_books() -> list[Book]:
    """
    ### Function fetch_books

    **Use:** Gets all books stored in the db

    **Returns:** All found books

    **Parameters:** None
    """

    # Initializes the db connection
    app_context.logger.info("Fetching all books from the database")
    db, cur = prepare_db()

    try:
        # Fetches all books stored in the Database
        books = cur.execute("SELECT * FROM books ORDER BY book_title ASC;").fetchall()

        new_books = []

        # Converts each book into a Book object
        for index in range(0, len(books)):
            book = books[index]
            authorIDs = cur.execute("SELECT abAuthorID FROM author_books WHERE abBookID = ?;", (book[0],)).fetchall()
            new_books.append(Book(id=book[0], title=book[1], author_ids=authorIDs, publisher=book[2], isbn=book[3], edition=book[4], year=book[5], book_type=book[6], tags=eval(book[7]),
                                  room=book[8], shelf=book[9], lend=book[10], lend_to=book[11], language=book[12]))


        # Closes the cursor
        cur.close()

        # Closes the database connection
        db.close()
        # Returns all found books
        app_context.logger.debug(f"Fetched {len(new_books)} books")
        return new_books
    except Exception as e:
        app_context.logger.error(f"Failed to fetch books: {e}")
        raise

def fetch_book_ids() -> list[int]:

    db, cur = prepare_db()

    ids = [ row[0] for row in cur.execute("SELECT book_id FROM books;").fetchall() ]

    cur.close()
    db.close()

    return ids;

def fetch_book_ids() -> list[int]:

    db, cur = prepare_db()

    ids = [ row[0] for row in cur.execute("SELECT book_id FROM books;").fetchall() ]

    cur.close()
    db.close()

    return ids;


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
    app_context.logger.info(f"Creating a new book: {book.title}")
    db, cur = prepare_db()

    try:
        authors_existing = True
        for id in book.author_ids:
            if not fetch_author(id):
                return f"Autor mit der ID {id} existier nicht!"
        
        # Creates the book with the provided parameters
        cur.execute(f"INSERT INTO books (book_title, book_publisher, book_isbn, book_edition, book_year, book_type, book_tags, book_room, book_shelf, book_lend, lend_to, book_language) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (book.title, book.publisher, book.isbn, book.edition, book.year, book.book_type, str(book.tags), book.room, book.shelf, book.lend, book.lend_to, book.language))

        # get the id of the newest entry
        id = cur.lastrowid

        for author in book.author_ids:
            cur.execute("INSERT INTO author_books (abAuthorID, abBookID) VALUES (?, ?);", (author, id))

        # Commits the changes to the db
        db.commit()
      
        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()

        # Returns True, because the book was successfully created
        app_context.logger.info(f"Successfully created book with ID: {id}")
        return id
    except Exception as e:
        app_context.logger.error(f"Failed to create book: {e}")
        raise


def delete_book(book_id:int) -> bool:
    """"
    ### Function delete_book

    **Use:** Deletes the book with the provided name if the security key is correct

    **Returns:**
    -   True if the book was deleted
    -   False if the book couldn't be deleted

    **Parameters:**
    -   name - The name of the book to be deleted
    """

    # If a book with the provided name does exist
    if fetch_book(book_id):
        
        app_context.logger.info(f"Deleting book with id {book_id}") 

        # Initializes db connection
        db, cur = prepare_db()
        
        try:
            isbn = cur.execute("SELECT isbn FROM books WHERE book_id = ?;", (book_id,)).fetchone()[0]
            app_context.logger.info(f"Deleting cover for book with isbn {isbn}")
            os.remove(os.path.join(os.curdir), "img", isbn)
            app_context.logger.info("Successfully deleted cover!")
        except Exception as e:
            app_context.logger.error(f"An error occurred while deleting the cover: {e}")

        # Deletes the book from the db
        cur.execute(f"DELETE FROM books WHERE book_id = ?;", (book_id,))

        # Commits the changes to the db
        db.commit()

        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()
        
        app_context.logger.info("Successfully deleted book")

        # Returns True because the book was successfully deleted
        return True

    else:
        app_context.logger.warn("Could not delete book: doesn't exist.")

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

    if not fetch_book(book_id):
        return f"Das Buch mit der ID {book_id} existiert nicht!"

    # Initializes the db connection
    app_context.logger.info(f"Editing book with ID: {book_id}")
    db, cur = prepare_db()

    try:
        old = fetch_book(book_id)

        # Transfere authors
        for author in old.author_ids:
            if not author in new.author_ids:
                cur.execute("DELETE FROM author_books WHERE abAuthorID = ? AND abBookID = ?;", (author, old.id))

        for author in new.author_ids:
            if not author in old.author_ids:
                cur.execute("INSERT INTO author_books (abAuthorID, abBookID) VALUES (?, ?);", (author, new.id))    # Updates the book

        cur.execute(f"""
UPDATE books
SET book_title = ?, book_publisher = ?, book_isbn = ?, book_edition = ?, book_year = ?, book_type = ?, book_tags = ?, book_room = ?, book_shelf = ?, book_lend = ?, lend_to = ?, book_language = ?
WHERE book_id = ?;
    """, (new.title, new.publisher, new.isbn, new.edition, new.year, new.book_type, str(new.tags), new.room, new.shelf, new.lend, new.lend_to, new.language, book_id))

        # Commits the changes to the db
        db.commit()

        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()

        # Returns True because the book was edited successfully
        app_context.logger.info(f"Successfully edited book with ID: {book_id}")
        return "OK"
    except Exception as e:
        app_context.logger.error(f"Failed to edit book: {e}")
        raise


def fetch_book(book_id:int) -> Book|bool:
    """
    ### Function fetch_book

    **Use:** Checks if there is a book with the provided id and returns it

    **Returns:**
    -   book - the data of the book if one was found
    -   False - if no book with the provided id was found

    **Parameters:**
    -   book_id - the id to search for
    """

    # Initializes the db connection
    app_context.logger.debug(f"Fetching book with ID: {book_id}")
    db, cur = prepare_db()

    try:
        # Fetches one book from the db where the id is equals to the book_id parameter
        book = cur.execute(f"SELECT * FROM books WHERE book_id = ?;", (book_id, )).fetchone()

        authorIDs = [ row[0] for row in cur.execute("SELECT abAuthorID FROM author_books WHERE abBookID = ?;", (book_id,)).fetchall() ]


        # Turns the fetched book into a Book object
        new_book = Book(id=book[0], title=book[1], author_ids=authorIDs, publisher=book[2], isbn=book[3], edition=book[4],
                    year=book[5], book_type=book[6], tags=eval(book[7]), room=book[8], shelf=book[9], lend=book[10], lend_to=book[11], language=book[12])

        # Returns the found book
        app_context.logger.debug(f"Successfully fetched book with ID: {book_id}")
        return new_book
    except Exception as e:
        app_context.logger.error(f"Failed to fetch book with ID {book_id}: {e}")
        raise


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
    app_context.logger.debug(f"Fetching book by ISBN: {isbn}")
    db, cur = prepare_db()

    try:
        # Fetches one book from the db where the title is equals to the name parameter
        book = cur.execute(f"SELECT * FROM books WHERE book_isbn = ?;", (isbn,)).fetchone()
        
        authorIDs = cur.execute("SELECT abAuthorID FROM author_books WHERE abBookID = ?;", (book[0],)).fetchall()

        # Turns the fetched book into a Book object
        book = Book(id=book[0], title=book[1], author_ids=authorIDs, publisher=book[2], isbn=book[3], edition=book[4],
                    year=book[5], book_type=book[6], tags=eval(book[7]), room=book[8], shelf=book[9], lend=book[10], lend_to=book[11])

        # Returns the found book
        app_context.logger.debug(f"Successfully fetched book by ISBN: {isbn}")
        return book
    except Exception as e:
        app_context.logger.error(f"Failed to fetch book by ISBN {isbn}: {e}")
        raise


def fetch_book_types() -> list[str]:
    app_context.logger.info("Fetching all book types from the database")
    db, cur = prepare_db()
    try:
        raw_types = cur.execute("SELECT * FROM types;").fetchall()
        book_types = []

        for raw_type in raw_types:
            book_types.append(raw_type[1])

        cur.close()
        db.close()

        app_context.logger.debug(f"Fetched {len(book_types)} book types")
        return book_types
    except Exception as e:
        app_context.logger.error(f"Failed to fetch book types: {e}")
        raise


def fetch_book_type_ids() -> list[str]:
    app_context.logger.info("Fetching all book type IDs from the database")
    db, cur = prepare_db()
    try:
        raw_types = cur.execute("SELECT * FROM types;").fetchall()
        type_ids = []

        for raw_type in raw_types:
            type_ids.append(raw_type[0])

        cur.close()
        db.close()

        app_context.logger.debug(f"Fetched {len(type_ids)} book type IDs")
        return type_ids
    except Exception as e:
        app_context.logger.error(f"Failed to fetch book type IDs: {e}")
        raise 

def fetch_book_type_id(name) -> int:
    app_context.logger.debug(f"Fetching book type ID for: {name}")
    db, cur = prepare_db()
    try:
        id = cur.execute(f"SELECT * FROM types WHERE type_name == ?;", (name,)).fetchone()[0]

        cur.close()
        db.close()

        app_context.logger.debug(f"Successfully fetched book type ID for: {name}")
        return id
    except Exception as e:
        app_context.logger.error(f"Failed to fetch book type ID for {name}: {e}")
        raise


def fetch_book_type(type_id) -> str:
    app_context.logger.debug(f"Fetching book type for ID: {type_id}")
    db, cur = prepare_db()
    try:
        name = cur.execute(f"SELECT * FROM types WHERE type_id == ?", (type_id,)).fetchone()[1]
    except Exception as e:
        name = "Unbekannt"
        app_context.logger.error(f"Failed to fetch book type for ID {type_id}: {e}")

    cur.close()
    db.close()

    app_context.logger.debug(f"Successfully fetched book type for ID: {type_id}")
    return name


def edit_book_type(type_id: int, new_type_name: str) -> str:
    app_context.logger.info(f"Editing book type with ID: {type_id}")
    db, cur = prepare_db()

    try:
        cur.execute(f"UPDATE types SET type_name = ? WHERE type_id = ?;", (new_type_name, type_id))
        db.commit()
        cur.close()
        db.close()

        app_context.logger.info(f"Successfully edited book type with ID: {type_id}")
        return "OK"
    except Exception as e:
        app_context.logger.error(f"Failed to edit book type with ID {type_id}: {e}")
        return e


def create_book_type(type_name: str) -> str:
    app_context.logger.info(f"Creating new book type: {type_name}")
    db, cur = prepare_db()

    try:
        cur.execute(f"INSERT INTO types (type_name) VALUES (?);", (type_name,))
        db.commit()
        cur.close()
        db.close()

        app_context.logger.info(f"Successfully created book type: {type_name}")
        return "OK"
    except Exception as e:
        app_context.logger.error(f"Failed to create book type {type_name}: {e}")
        return e

def delete_book_type(type_id: int):
    db, cur = prepare_db()

    try:
        cur.execute(f"DELETE FROM types WHERE type_id == ?", (type_id))
        db.commit()
        cur.close()
        db.close()

    except Exception as e:
        return e

    return "OK"


def fetch_rooms() -> list[str]:
    app_context.logger.info("Fetching all rooms from the database")
    db, cur = prepare_db()
    try:
        raw_rooms = cur.execute("SELECT * FROM rooms;").fetchall()
        rooms = []

        for raw_room in raw_rooms:
            rooms.append(raw_room[1])

        cur.close()
        db.close()

        app_context.logger.debug(f"Fetched {len(rooms)} rooms")
        return rooms
    except Exception as e:
        app_context.logger.error(f"Failed to fetch rooms: {e}")
        raise


def fetch_room_ids() -> list[str]:
    app_context.logger.info("Fetching all room IDs from the database")
    db, cur = prepare_db()
    try:
        raw_rooms = cur.execute("SELECT * FROM rooms;").fetchall()
        room_ids = []

        for raw_room in raw_rooms:
            room_ids.append(raw_room[0])

        cur.close()
        db.close()

        app_context.logger.debug(f"Fetched {len(room_ids)} room IDs")
        return room_ids
    except Exception as e:
        app_context.logger.error(f"Failed to fetch room IDs: {e}")
        raise


def fetch_room_id(name) -> int:
    app_context.logger.debug(f"Fetching room ID for: {name}")
    db, cur = prepare_db()
    try:
        id = cur.execute(f"SELECT * FROM rooms WHERE room_name == ?;", (name,)).fetchone()[0]
        cur.close()
        db.close()

        app_context.logger.debug(f"Successfully fetched room ID for: {name}")
        return id
    except Exception as e:
        app_context.logger.error(f"Failed to fetch room ID for {name}: {e}")
        raise



def fetch_room(room_id) -> str:
    app_context.logger.debug(f"Fetching room for ID: {room_id}")
    db, cur = prepare_db()
    try:
        name = cur.execute(f"SELECT * FROM rooms WHERE room_id == ?;", (room_id,)).fetchone()[1]
    except Exception as e:
        name = "Unbekannt"
        app_context.logger.error(f"Failed to fetch room for ID {room_id}: {e}")

    cur.close()
    db.close()

    app_context.logger.debug(f"Successfully fetched room for ID: {room_id}")
    return name


def edit_room(room_id: int, new_room_name: str) -> str:
    app_context.logger.info(f"Editing room with ID: {room_id}")
    db, cur = prepare_db()

    try:
        cur.execute(f"UPDATE rooms SET room_name = ? WHERE room_id == ?;", (new_room_name, room_id))
        db.commit()
        cur.close()
        db.close()

        app_context.logger.info(f"Successfully edited room with ID: {room_id}")
        return "OK"
    except Exception as e:
        app_context.logger.error(f"Failed to edit room with ID {room_id}: {e}")
        return e 


def create_room(room_name: str) -> str:
    app_context.logger.info(f"Creating new room: {room_name}")
    db, cur = prepare_db()

    try:
        cur.execute(f"INSERT INTO rooms (room_name) VALUES (?);", (room_name,))
        db.commit()
        cur.close()
        db.close()

        app_context.logger.info(f"Successfully created room: {room_name}")
        return "OK"
    except Exception as e:
        app_context.logger.error(f"Failed to create room {room_name}: {e}")
        return e


def delete_room(room_id: int):
    app_context.logger.info(f"Deleting room with ID: {room_id}")
    db, cur = prepare_db()

    try:
        cur.execute(f"DELETE FROM rooms WHERE room_id = ?;", (room_id,))
        db.commit()
        cur.close()
        db.close()

        app_context.logger.info(f"Successfully deleted room with ID: {room_id}")
        return "OK"
    except Exception as e:
        app_context.logger.error(f"Failed to delete room with ID {room_id}: {e}")
        return e


def get_author_count():
    app_context.logger.info("Fetching author count from the database")
    db, cur = prepare_db()
    try:
        count = cur.execute("SELECT COUNT(author_id) FROM authors;").fetchone()[0]

        cur.close()
        db.close()

        app_context.logger.debug(f"Author count: {count}")
        return count
    except Exception as e:
        app_context.logger.error(f"Failed to fetch author count: {e}")
        raise


def get_book_count():
    app_context.logger.info("Fetching book count from the database")
    db, cur = prepare_db()
    try:
        count = cur.execute("SELECT COUNT(book_id) FROM books;").fetchone()[0]

        cur.close()
        db.close()

        app_context.logger.debug(f"Book count: {count}")
        return count
    except Exception as e:
        app_context.logger.error(f"Failed to fetch book count: {e}")
        raise

