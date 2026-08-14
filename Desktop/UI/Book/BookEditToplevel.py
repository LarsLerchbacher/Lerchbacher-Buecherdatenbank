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


import app_context
from database import Book, create_book, edit_book, fetch_author, fetch_authors, fetch_authors_for_book, fetch_book, fetch_book_type, fetch_book_type_id, fetch_book_types, fetch_room, fetch_room_id, fetch_rooms
from images import update_image
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from UI.Author.AuthorEditToplevel import AuthorEditToplevel
from UI.Book.BookEditWidget import BookEditWidget


class BookEditToplevel(CTkToplevel):
    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.minsize(600, 800)

        self.id = id
        if self.id != -1:
            app_context.logger.info(f"Opening book editing dialog for book with id {self.id}")
        else:
            app_context.logger.info("Opening empty book editing dialog")

        self.columnconfigure(index=0)
        self.columnconfigure(index=1)
        self.columnconfigure(index=2)
        self.columnconfigure(index=3)

        self.edit = BookEditWidget(self)
        self.edit.pack(expand=True, fill="both")

        self.edit.lend.configure(command=self.edit.update_lend_to)

        self.createCTkButton = CTkButton(self.edit.authors, text="Autor hinzufügen", command=self.create_author)
        self.createCTkButton.grid(row=0, column=3)

        self.button_frame = CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(padx=20, pady=5)

        self.save_button = CTkButton(self.button_frame, text='Speichern', command=self.save)
        self.cancel_button = CTkButton(self.button_frame, text='Abbrechen', command=self.cancel)
        self.save_button.grid(row=0, column=0)
        self.cancel_button.grid(row=0, column=1, padx=10)

        self.edit.title.focus_set()
        self.bind("<Return>", lambda e: self.save())

        if self.id != -1:
            self.refresh()

    def refresh(self):
        book = fetch_book(self.id)

        self.edit.title.delete(0, END)
        self.edit.title.insert(0, book.title)

        selected_ids = [ row.id for row in fetch_authors_for_book(self.id) ]
        self.edit.authors.set(selected_ids)

        self.edit.language.delete(0, END)
        self.edit.language.insert(0, book.language)

        self.edit.publisher.delete(0, END)
        self.edit.publisher.insert(0, book.publisher)

        self.edit.isbn.delete(0, END)
        isbn_value = str(book.isbn)
        if len(isbn_value) == 13:
            self.edit.isbn.insert(0, f"{isbn_value[0:3]}-{isbn_value[3]}-{isbn_value[4:7]}-{isbn_value[7:12]}-{isbn_value[12]}")
        else:
            self.edit.isbn.insert(0, "Unbekannt")

        self.edit.edition.set(int(book.edition) or 0)

        self.edit.year.set(book.year)

        self.all_types = fetch_book_types()
        self.edit.type_select.configure(values=self.all_types)

        self.edit.type_select.set(fetch_book_type(book.book_type))

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
        if not self.edit.check_is_filled():
            app_context.logger.warning("Trying to save, but not all necesary fields are filled.")
            CTkMessagebox(title="Pflichtfelder ausfuellen", message="Bitte fuellen Sie alle Felder die mit einem * markiert sind aus.")
        else:
            if self.id == -1:
                app_context.logger.info("Creating new book...")
            else:
                # Code to save changes / create new book
                app_context.logger.info(f"Saving book: {self.id}")

            title = self.edit.title.get()
            author_ids = self.edit.authors.get()
            authors = []
            for id in author_ids:
                author = fetch_author(id)
                authors.append(author.getName())
            language = self.edit.language.get()
            publisher = self.edit.publisher.get()
            isbn = self.edit.isbn.get()
            edition = self.edit.edition.get()
            year = self.edit.year.get()
            book_type = self.edit.type_select.get()
            type_nr = fetch_book_type_id(book_type)
            tags = self.edit.tags.get().replace("; ", ";").split(";")
            book_room = self.edit.room.get()
            room_nr = fetch_room_id(book_room)
            shelf = self.edit.shelf.get()
            lend = self.edit.lend_var.get()
            lend_str = "ja" if lend else "nein"
            lend_to = self.edit.lend_to.get()

            book = Book(id=self.id, title=title, author_ids=author_ids, publisher=publisher, isbn=isbn, edition=edition, year=year, book_type=type_nr, tags=tags, room=room_nr, shelf=shelf, lend=lend, lend_to=lend_to, language=language)

            if self.id != -1:
                response = edit_book(self.id, book)
                if response != "OK":
                    app_context.logger.info(f"Speicher nicht möglich\n{response}")
                    CTkMessagebox(title="Speichern nicht möglich!", message=response, icon="error")
                else:
                    app_context.logger.info("Saved successfully!")

                    update_image(book)

                    app_context.mainWindow.refresh()
                    self.destroy()
            else:
                response = create_book(book)
                if type(response) == str:
                    app_context.logger.info(f"Speicher nicht möglich\n{response}")
                    CTkMessagebox(title="Speichern nicht möglich!", message=response, icon="error")
                else:
                    self.id = response
                    book.id = response
                    app_context.logger.info("Saved successfully!")

                    update_image(book)

                    app_context.mainWindow.refresh()
                    self.destroy()


    def cancel(self):
        self.destroy()

    def create_author(self):
        self.wait_window(AuthorEditToplevel(-1))
        self.edit.authors.set(self.edit.authors.get())
