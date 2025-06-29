#
# Lerchbacher Buecherdatenbank - helper functions module
# Copyright 2025 Lars Lerchbacher
#


import requests
import sqlite3
from handle_db import *
from pathlib import Path
from PIL import Image
from datetime import datetime


IMAGE_SIZE = 175


def check_flags() -> bool:
    verbose = False
    with open("flags.txt", mode="r") as file:
        flags = file.readlines()
        for flag in flags:
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

    return verbose


def log(log_text: str) -> None:
    with open("log.txt", mode="a") as file:
        file.write(f"\n[{datetime.now()}] {log_text}")

    verbose = check_flags()

    if verbose:
        print(f"[{datetime.now()}] {log_text}")


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


def get_cover(book: Book):
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


def read_rooms() -> list[str]:
    db, cur = prepare_db()
    raw_rooms = cur.execute("SELECT * FROM rooms;").fetchall()
    book_rooms = []

    for raw_room in raw_rooms:
        book_rooms.append(raw_room[1])

    cur.close()
    db.close()

    return book_rooms


def set_rooms(rooms: list[str]) -> None:
    db, cur = prepare_db()

    cur.execute("DROP TABLE rooms;")

    db.commit()

    cur.execute("CREATE TABLE rooms (room_id INTEGER PRIMARY KEY AUTOINCREMENT, room_name STRING NOT NULL);")

    db.commit()

    for room in rooms:
        cur.execute(f"INSERT INTO rooms (room_name) VALUES ('{room}');")

    db.commit()

    cur.close()
    db.close()
