# Updates the database to a newer version

import app_context
from database import *
import sqlite3


# Defines which database format versions each program version supports
SUPPORTED_VERSIONS = \
{
    "1.2.0": ["1.2.0"]
}


def run_update(dbVersion, programVersion):
    if dbVersion == "1.1.2" and programVersion == "1.2.0":
        run_update_112_to_120()


def run_update_112_to_120():
    app_context.logger.info("Database format conversion tool for the Lerchbacher Buecherdatenbank")
    app_context.logger.info("----------------------------------------------------")
    app_context.logger.info("Opening database connection...")
    db, cur = prepare_db()
    app_context.logger.info("Success!")
    app_context.logger.info("Attempting to convert the database...")

    app_context.logger.debug("Creating tempomary authors table...")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tmp(
        author_id INTEGER PRIMARY KEY AUTOINCREMENT,
        firstName VARCHAR,
        lastName VARCHAR NOT NULL
    );""")

    db.commit()

    app_context.logger.debug("Fetching authors...")

    authors = cur.execute("SELECT author_id, author_name FROM authors;").fetchall()

    app_context.logger.debug("Transfering author data to tempomary table...")

    for author in authors:
        id = author[0]
        nameParts = author[1].split(" ")
        lastName = nameParts[-1]
        firstName = " ".join(nameParts[:-1])
        cur.execute("INSERT INTO tmp (author_id, firstName, lastName) VALUES (?, ?, ?);", (id, firstName, lastName))
    
    app_context.logger.debug("Deleting authors table...")

    cur.execute("DROP TABLE authors;")

    app_context.logger.debug("Renaming tempomary table to authors table...")

    cur.execute("ALTER TABLE tmp RENAME TO authors;")

    db.commit()

    app_context.logger.debug("Creating intermediate table for authors and books...")
    cur.execute("""CREATE TABLE author_books(
    ABID INTEGER PRIMARY KEY AUTOINCREMENT,
    abAuthorID INTEGER REFERENCES authors(author_id),
    abBookID INTEGER REFERENCES books(book_id)
);""")

    db.commit()

    app_context.logger.debug("Transfering author-book data to author books intermediate table...")
    books = cur.execute("SELECT book_id, author_ids FROM books;").fetchall()
    for book in books:
        for authorID in eval(book[1]):
            cur.execute("INSERT INTO author_books(abAuthorID, abBookID) VALUES (?, ?);", (authorID,book[0])) 
    
    app_context.logger.debug("Deleting author_ids column from books table...")
    cur.execute("ALTER TABLE books DROP COLUMN author_ids;")

    app_context.logger.debug("Adding language column to books table...")
    cur.execute("ALTER TABLE books ADD COLUMN book_language VARCHAR(50);")
    cur.execute("UPDATE books SET book_language = 'Unbekannt';")

    app_context.logger.debug("Creating database version table...")
    cur.execute("CREATE Table dbVersion (id INTEGER PRIMARY KEY, version VARCHAR);")

    db.commit()

    app_context.logger.debug("Setting database version...")
    cur.execute("INSERT INTO dbVersion (id, version) VALUES (0, '1.2.0');")

    app_context.logger.info("Success!")
    app_context.logger.info("Closing database")

    cur.close()

    db.close()


def check_if_update_is_needed():
    db, cur = prepare_db()

    app_context.logger.info("Checking if the database needs to be converted...")

    try:
            dbVersion = cur.execute("SELECT version from dbVersion WHERE id=0;").fetchone()[0]
            app_context.logger.info("Database format version: " + dbVersion)
            app_context.logger.info("Program version: " + app_context.version)
            if dbVersion in SUPPORTED_VERSIONS[app_context.version]:
                app_context.logger.info("Database has a supported format")
            else:
                app_context.logger.info("Database needs to be converted")
                run_update(dbVersion, app_context.version)
    except:
        app_context.logger.info("Database needs to be converted")
        run_update("1.1.2", app_context.version)


