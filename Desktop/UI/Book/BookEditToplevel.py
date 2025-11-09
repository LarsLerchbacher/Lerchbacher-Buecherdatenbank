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
from database import Book, create_book, edit_book, fetch_authors, fetch_book, fetch_book_type, fetch_book_type_id, fetch_book_types, fetch_room, fetch_room_id, fetch_rooms
from images import update_image
from tkinter import *
from UI.Book.BookEditWidget import BookEditWidget


class BookEditToplevel(Toplevel):
    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = id
        if self.id != -1:
            app_context.logger.info(f"Opening book editing dialog for book with id {self.id}")
        else:
            app_context.logger.info("Opening empty book editing dialog")

        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)
        self.columnconfigure(index=2, weight=1)
        self.columnconfigure(index=3, weight=1)

        self.edit = BookEditWidget(self)
        self.edit.pack()

        self.edit.lend.config(command=self.edit.update_lend_to)

        self.button_frame = Frame(self)
        self.button_frame.pack(padx=20, pady=5)

        self.save_button = Button(self.button_frame, text='Speichern', command=self.save)
        self.cancel_button = Button(self.button_frame, text='Abbrechen', command=self.cancel)
        self.save_button.grid(row=0, column=0)
        self.cancel_button.grid(row=0, column=1, padx=10)

        if self.id != -1:
            self.update()

    def update(self):
        book = fetch_book(self.id)

        self.edit.title.delete(0, END)
        self.edit.title.insert(0, book.title)

        self.edit.authors.set(book.author_ids)

        self.edit.publisher.delete(0, END)
        self.edit.publisher.insert(0, book.publisher)

        self.edit.isbn.delete(0, END)
        isbn_value = str(book.isbn)
        if len(isbn_value) == 13:
            self.edit.isbn.insert(0, f"{isbn_value[0:3]}-{isbn_value[3]}-{isbn_value[4:7]}-{isbn_value[7:12]}-{isbn_value[12]}")
        else:
            self.edit.isbn.insert(0, "Unbekannt")

        self.edit.edition.set(book.edition)

        self.edit.year.set(book.year)

        self.all_types = fetch_book_types()
        self.edit.type_select.config(completevalues=self.all_types)

        self.edit.type_select.set(fetch_book_type(book.type))

        self.edit.room.set(fetch_room(book.room))

        self.edit.tags.delete(0, END)
        self.edit.tags.insert(0, "; ".join(book.tags))

        self.edit.shelf.delete(0, END)
        self.edit.shelf.insert(0, book.shelf)

        self.edit.lend_var.set(book.lend)

        self.edit.update_lend_to()

        if book.lend == 1:
            self.edit.lend_to.insert(0, book.lend_to)

    def save(self):
        # Code to save changes / create new book
        app_context.logger.info("Saving book: ")

        title = self.edit.title.get()
        app_context.logger.info(f"\tTitle: {title}")

        author_ids = self.edit.authors.get()
        authors = []
        all_authors = fetch_authors()
        for author in fetch_authors():
            if author.id in author_ids:
                authors.append(author.name)
        app_context.logger.info(f"\tAutoren: {authors} (Ids: {author_ids})")

        publisher = self.edit.publisher.get()
        app_context.logger.info(f"\tVerlag: {publisher}")

        isbn = self.edit.isbn.get()
        app_context.logger.info(f"\tISBN: {isbn}")

        edition = self.edit.edition.get()
        app_context.logger.info(f"\tAuflage: {edition}")

        year = self.edit.year.get()
        app_context.logger.info(f"\tJahr: {year}")

        book_type = self.edit.type_select.get()
        type_nr = fetch_book_type_id(book_type)
        app_context.logger.info(f"\tBuchtyp: {book_type} (Typ Nr. {type_nr})")

        tags = self.edit.tags.get().replace("; ", ";").split(";")
        app_context.logger.info(f"\tKategorien: {tags}")

        book_room = self.edit.room.get()
        room_nr = fetch_room_id(book_room)
        app_context.logger.info(f"\tRaum: {book_room} (Raum Nr. {room_nr})")

        shelf = self.edit.shelf.get()
        app_context.logger.info(f"\tRegal: {shelf}")

        lend = self.edit.lend_var.get()
        app_context.logger.info(f"\tVerliehen: {"ja" if lend else "nein"} (lend_var: {lend})")

        lend_to = self.edit.lend_to.get()
        if lend_to != "":
            app_context.logger.info(f"\tVerliehen an: {lend_to}")

        book = Book(id=self.id, title=title, author_ids=author_ids, publisher=publisher, isbn=isbn, edition=edition, year=year, type=type_nr, tags=tags, room=room_nr, shelf=shelf, lend=lend, lend_to=lend_to)

        if self.id != -1:
            response = edit_book(self.id, book)
            if response != "OK":
                app_context.logger.info(f"Speicher nicht möglich\n{response}")
                messagebox.showerror(title="Speichern nicht möglich!", message=response)
            else:
                app_context.logger.info("Erfolgreich gespeichert!")

                update_image(book)

                app_context.mainWindow.update()
                self.destroy()
        else:
            response = create_book(book)
            if type(response) == str:
                app_context.logger.info(f"Speicher nicht möglich\n{response}")
                messagebox.showerror(title="Speichern nicht möglich!", message=response)
            else:
                self.id = response
                book.id = response
                app_context.logger.info("Erfolgreich gespeichert!")

                update_image(book)

                app_context.mainWindow.update()
                self.destroy()


    def cancel(self):
        self.destroy()

