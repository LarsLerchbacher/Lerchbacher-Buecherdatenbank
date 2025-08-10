#
# Lerchbacher Buecherdatenbank - helper functions module
# Copyright 2025 Lars Lerchbacher
#


import app_context
import requests
import sqlite3
from handle_db import *
from pathlib import Path
from PIL import Image
from datetime import datetime


IMAGE_SIZE = 175


def check_flags() -> bool:
    verbose = False
    for flag in app_context.flags:
        if flag == "":
            continue
        elif flag == "-v" or flag == "--verbose":
            if not verbose:
                verbose = True
            else:
                raise Exception(f"Duplicate flag {flag}")
        elif flag in ["-h", "--help"]:
            print("""Lerchbacher book database v0.0.1
                  Arguments:
                    -h --help       Show this help
                    -v --verbose    Show log output in console 
                """)
            quit()
        else:
            raise Exception(f"Unknown Flag {flag}")

    return (verbose,)


def log(log_text: str, *args) -> None:
    if len(args) == 1:
        type = args[0]
    else:
        type = "INFO "

    with open("log.txt", mode="a") as file:
        file.write(f"\n[{datetime.now()}] [{type}] {log_text}")

    verbose = check_flags()[0]

    if verbose:
        print(f"[{datetime.now()}] [{type}] {log_text}")


def log_line() -> None:
    with open("log.txt", mode="a") as file:
        file.write("\n----------")


def update_images():
    log("Getting covers...")
    books = fetch_books()
    covers = fetch_covers(books)

    for index, cover in enumerate(covers):
        log(f"Processing item nr. {index}: {cover}")
        if not cover == "./static/noCover.png":
            cacheName = f"./cache/{books[index].id}.jpg"
            cachePath = Path(cacheName)
            staticName = f"./static/{books[index].id}"
            staticPath = Path(staticName)
            if cachePath.is_file() or staticPath.is_file():
                log("Cover found, skipping...")
                continue
            else:
                log("Downloading cover...")
                response = requests.get(cover)
                file = open(cacheName, mode="wb+")
                file.write(response.content)
                file.close()


def get_cover(book):
        cacheName = f"./cache/{book.id}.jpg"
        cachePath = Path(cacheName)
        staticName = f"./static/{book.id}.jpg"
        staticPath = Path(staticName)

        if staticPath.is_file():
            filename = staticName

        elif cachePath.is_file():
            filename = cacheName

        else:
            filename = "./static/noCover.png"

        image = Image.open(filename)

        w, h = image.size
        if h != IMAGE_SIZE:
            ratio = IMAGE_SIZE / h
            new_size = (int(w * ratio), IMAGE_SIZE)
            image = image.resize(new_size, Image.BILINEAR)

        return image


def get_image(book):
        cacheName = f"./cache/{book.id}.jpg"
        cachePath = Path(cacheName)
        staticName = f"./static/{book.id}.jpg"
        staticPath = Path(staticName)

        if staticPath.is_file():
            filename = staticName

        elif cachePath.is_file():
            filename = cacheName

        else:
            filename = "./static/noCover.png"

        return filename


def fetch_images(books: list) -> list: 

    covers = []

    # Iterates through all books in the books list
    for book in books:

        # Gets the filename of the image to be displayed for the book
        cover = get_image(book)

        # Adds the current cover to the covers list
        covers.append(cover)

    return covers


def fetch_covers(books:list) -> list:
    covers = []
    # Iterates through all books in the books list
    for book in books:

        # Tries to get the smallest cover
        cover = get_cover(book)

        # Adds the current cover to the covers list
        covers.append(cover)

    return covers

