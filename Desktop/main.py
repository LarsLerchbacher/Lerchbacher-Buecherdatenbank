#
# Desktop/main.py
# ----------
#
#   The Lerchbacher book database project
#   © Lars Lerchbacher 2025
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


import argparse
import app_context
from database import prepare_db
import logging
from UI.App import App
from PIL import Image
import os
import requests
import sys
import traceback


global logger, formatter


class ErrorHandler(object):
    """Class to redirect stderr to the logger"""
    def write(self, data):
        logger.error(data)


def init_logger() -> None:
    """Function that creates a logger"""
    global logger, formatter, args

    # Preparing the logger
    app_context.logger = logging.getLogger()
    logger = app_context.logger
    logger.setLevel(logging.INFO)

    # Set the log format: datetime [LEVEL] name -- message
    app_context.formatter = logging.Formatter('[%(asctime)s] [%(levelname)-6s] %(message)s')
    formatter = app_context.formatter

    # Always log to log.txt
    logfile = open('log.txt', 'w')
    fileHandler = logging.StreamHandler(logfile)
    fileHandler.setLevel(logging.INFO)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    # Stop Pillow from logging debug messages
    logging.getLogger("PIL.PngImagePlugin").setLevel(logging.WARNING)

    # Stop requests from logging debug messages
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def process_args() -> None:
    """Function that processes the provided arguments"""
    global logger, formatter, args

    # Create an ArgumentParser Instance
    parser = argparse.ArgumentParser(
            prog=f"Lerchbacher Buecherdatenbank",
            description=f"Lerchbacher Bücherdatenbank v{app_context.version}")

    # Add the verbose flag to it
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help="Increase verbosity"
                        )

    # Parse the arguments
    args = parser.parse_args()

    # If the verbose flag is set, set the logger to also log to stdout
    if args.verbose:
        stdoutHandler = logging.StreamHandler(sys.stdout)
        stdoutHandler.setLevel(logging.DEBUG)
        stdoutHandler.setFormatter(formatter)
        logger.addHandler(stdoutHandler)

        logger.setLevel(logging.DEBUG)



def init_files() -> None:
    """Function that checks for the necesary files and folders and creates/downloads them if necesary"""
    global logger

    # Checking for the cache folder
    logger.info("Checking for image folder...")
    
    if not os.path.exists("./img"):
        logger.warning("No existing image folder found! Creating one...")
        os.mkdir("img")

    else:
        logger.info("Existing img folder found!")

    
    # Checking for the noCover.png file
    logger.info("Checking for noCover.png file...")

    if not os.path.exists("./img/noCover.png"):
        logger.warning("File not found! Downloading it...")

        # Downloading it from github
        request = requests.get("https://github.com/LarsLerchbacher/Lerchbacher-Buecherdatenbank/blob/master/Desktop/static/noCover.png?raw=true")
        file = open("./img/noCover.png", "wb")
        file.write(request.content)
        file.close()

    else:
        logger.info("File found!")

    
    # Checking for the database
    logger.info("Checking for database...")
    if not os.path.exists("./database.sqlite"):
        logger.warning("No existing database found! Creating a new one...")

        # Connecting to the database
        db, cur = prepare_db()

        # Creating the authors table
        cur.execute("""
        CREATE TABLE authors (
            author_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            author_name STRING NOT NULL,
            has_nobel_prize BOOLEAN,
            author_country STRING NOT NULL,
            date_of_birth TIMESTAMP NOT NULL,
            date_of_death TIMESTAMP NOT NULL
        );""")

        # Creating the books table
        cur.execute("""
            CREATE TABLE "books" (
                "book_id"	INTEGER,
                "book_title"	STRING NOT NULL,
                "author_ids"	BLOB,
                "book_publisher"	STRING,
                "book_isbn"	STRING,
                "book_edition"	INTEGER NOT NULL DEFAULT 1,
                "book_year"	INTEGER,
                "book_type"	INTEGER,
                "book_tags"	BLOB,
                "book_room"	STRING,
                "book_shelf"	STRING,
                "book_lend"	INTEGER,
                "lend_to" STRING,
                PRIMARY KEY("book_id" AUTOINCREMENT)
            );""")

        # Creating the rooms table
        cur.execute("""CREATE TABLE rooms (room_id INTEGER PRIMARY KEY AUTOINCREMENT, room_name STRING NOT NULL);""")

        # Creating the types table for book types
        cur.execute("""CREATE TABLE types (type_id INTEGER PRIMARY KEY AUTOINCREMENT, type_name STRING NOT NULL);""")

        # Commiting the changes
        db.commit()
        
        # Closing the db
        cur.close()

        db.close()

    else:
        logger.info("Existing database found!")


def main() -> None:
    global logger, formatter
    global mainWindow

    # Logging a welcome message
    logger.info("---------")
    logger.info(f"Lerchbacher book database desktop v{app_context.version}")
    logger.info("Starting application")

    # Check for the necesary files and folders
    init_files()

    # Starting the main application
    mainWindow = App()
    mainWindow.start()


if __name__ == "__main__":

    # Setting the application's version that is displayed
    app_context.version = "1.1.0" 

    # Init the logger and check for any flags
    init_logger()
    process_args()

    # Route error output to the logger's output
    errorHandler = ErrorHandler()
    sys.stderr = errorHandler

    # Catch every Exception and log it
    try:
        # Run the main part of the program
        main()

        # Logging a goodbye message
        logger.info("Closing application!")
        logger.info("Goodbye!")

    except Exception as e:
        # Logging the Exception including its traceback
        logger.error(traceback.format_exc())

