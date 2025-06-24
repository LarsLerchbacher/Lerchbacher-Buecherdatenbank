#
# Lerchbacher Buecherdatenbank - helper functions module
# Copyright 2025 Lars Lerchbacher
#


import requests
import sqlite3
from handle_db import *
from pathlib import Path
from PIL import Image


IMAGE_SIZE = 175


def update_images():
    books = fetch_books()
    covers = fetch_covers([books])

    for index, cover in enumerate(covers):
        if not cover == "/static/noCover.png":
            filename = f"./cache/images/{books[index].id}.jpg"
            filePath = Path(filename)
            if not filePath.is_file():
                response = requests.get(cover)
                file = open(filename, mode="wb+")
                file.write(response.content)
                file.close()


def get_cover(book: Book):
        filename = f"./cache/images/{book.id}.jpg"
        filePath = Path(filename)
        if not filePath.is_file():
            filename = "./static/noCover.png"

        image = Image.open(filename)

        w, h = image.size
        if h != IMAGE_SIZE:
            ratio = IMAGE_SIZE / h
            new_size = (int(w * ratio), IMAGE_SIZE)
            image = image.resize(new_size, Image.BILINEAR)

        return image


def read_book_types() -> list[str]:
    db, cur = prepare_db()
    raw_types = cur.execute("SELECT * FROM types;").fetchall()
    book_types = []

    for raw_type in raw_types:
        book_types.append(raw_type[1])

    cur.close()
    db.close()

    return book_types


def set_book_types(types: list[str]) -> None:
    db, cur = prepare_db()

    cur.execute("DROP TABLE types;")

    db.commit()

    cur.execute("CREATE TABLE types (type_id INTEGER PRIMARY KEY AUTOINCREMENT, type_name STRING NOT NULL);")

    db.commit()

    for book_type in types:
        cur.execute(f"INSERT INTO types (type_name) VALUES ('{book_type}');")

    db.commit()

    cur.close()
    db.close()
