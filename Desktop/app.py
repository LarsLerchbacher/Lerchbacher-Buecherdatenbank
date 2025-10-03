#
# Desktop/app.py
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


import app_context
import logging
from UIClasses import *
from PIL import Image
import os
import sys
import traceback


global logger, formatter
IMAGE_SIZE = 175


class ErrorHandler(object):
    def write(self, data):
        logger.error(data)


def init_logger() -> None:
    global logger, formatter, args

    # Preparing the logger
    app_context.logger = logging.getLogger(__name__)
    logger = app_context.logger
    logger.setLevel(logging.INFO)

    # Set the log format: datetime [LEVEL] name -- message
    app_context.formatter = logging.Formatter('[%(asctime)s] [%(levelname)-6s] %(message)s')
    formatter = app_context.formatter

    # Always log to log.txt
    logfile = open('log.txt', 'w')
    fileHandler = logging.StreamHandler(logfile)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)


def process_args() -> None:
    global logger, formatter, args

    # Process arguments
    args = sys.argv

    for arg in args:
        # If the verbose flag is set, also log to stdout
        if arg in ["-v", "--verbose"]:
            stdoutHandler = logging.StreamHandler(sys.stdout)
            stdoutHandler.setLevel(logging.DEBUG)
            stdoutHandler.setFormatter(formatter)
            logger.addHandler(stdoutHandler)

            logger.setLevel(logging.DEBUG)

        # The -h or --help flag print a small help text to the console
        elif flag in ["-h", "--help"]:
            print(f"""Lerchbacher book database v{app_context.version}
                  Arguments:
                    -h --help       Show this help
                    -v --verbose    Show log output in console 
                """)
            quit()
        else:
            raise Exception(f"Unknown Flag {flag}")


def update_image(book):
    app_context.logger.info(f"Looking for a cover for the book {book.title} (ID: {book.id})")
    filename = get_image_src(book)

    if filename != "./static/noCover.png":            
        app_context.logger.info("Existing found")

    else:
        app_context.logger.info("Downloading cover...")
        try:
            response = requests.get("https://covers.openlibrary.org/b/isbn/{book.isbn}-S.jpg")
            file = open(cacheName, mode="wb+")
            file.write(response.content)
            file.close()
        except Exception as e:
            app_context.logger.info("Could not download cover")


def get_image(book):
    filename = get_image_src(book)

    image = Image.open(filename)

    w, h = image.size
    if h != IMAGE_SIZE:
        ratio = IMAGE_SIZE / h
        new_size = (int(w * ratio), IMAGE_SIZE)
        image = image.resize(new_size, Image.BILINEAR)

    return image


def get_image_src(book):
    cachePath = os.path.join(os.getcwd(), 'cache', f'{book.id}.jpg')
    staticPath = os.path.join(os.getcwd(), 'static', f'{book.id}.jpg')

    if os.path.exists(staticPath):
        filename = str(staticPath)

    elif os.path.exists(cachePath):
        filename = str(cachePath)

    else:
        filename = "./static/noCover.png"

    return filename


def main() -> None:
    global logger, formatter
    global mainWindow

    # Logging a welcome message
    logger.info("---------")
    logger.info(f"Lerchbacher book database desktop v{app_context.version}")
    logger.info("Starting application")

    mainWindow = App()
    mainWindow.mainloop()




if __name__ == "__main__":

    # Setting the application's version that is displayed
    app_context.version = "DEV" 

    # Proces the arguments
    args = sys.argv
    if len(args) > 1:
        del args[0]
        app_context.flags = args
    else:
        app_context.flags = []

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
        logger.info("Peacefully terminating application")
        logger.info("Goodbye!")

    except Exception as e:
        # Logging the Exception including its traceback
        logger.error(traceback.format_exc())

