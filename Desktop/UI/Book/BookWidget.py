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
from images import rescale_image, get_image
from database import delete_book, fetch_author, fetch_book, fetch_room, fetch_book_type, fetch_authors_for_book
import PIL
from PIL import ImageTk
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from UI.Book.BookEditToplevel import BookEditToplevel


class BookWidget(CTkFrame):
    def __init__(self, parent, id: int, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.id = id

        self.preview = CTkFrame(self, fg_color="transparent")
        self.details = CTkFrame(self.preview, fg_color="transparent")
        self.preview.pack()

        self.title = CTkLabel(self.preview, text = "", font=("Arial", 16, "bold"), wraplength=500, justify='center')
        self.author = CTkLabel(self.preview, text = "", font=("Arial", 12))

        image_data = PIL.Image.open("./img/noCover.png")
        image_data = rescale_image(image_data)
        self.image_tk = CTkImage(light_image=image_data, dark_image=image_data, size=image_data.size)
        self.image = CTkLabel(self.details, image = self.image_tk, text="")

        self.publisher = CTkLabel(self.details, text = 'Verlag: ')
        self.publisher.pack(pady = 5, padx = 50)

        self.isbn = CTkLabel(self.details, text = 'ISBN: ')
        self.isbn.pack(pady = 5, padx = 50)

        self.edition = CTkLabel(self.details, text = 'Auflage Nr.:')
        self.edition.pack(pady = 5, padx = 50)        

        self.year = CTkLabel(self.details, text = 'Jahr: ')
        self.year.pack(pady = 5, padx = 50)

        self.type = CTkLabel(self.details, text = 'Buchtyp: ')
        self.type.pack(pady = 5, padx = 50)

        self.tags = CTkLabel(self.details, text = 'Stichwörter: ')
        self.tags.pack(pady = 5, padx = 50)

        self.room = CTkLabel(self.details, text = 'Raum: ')
        self.room.pack(pady = 5, padx = 50)

        self.shelf = CTkLabel(self.details, text = 'Regal: ')
        self.shelf.pack(pady = 5, padx = 50)

        self.language = CTkLabel(self.details, text = 'Sprache: ')
        self.language.pack(pady = 5, padx = 50)

        self.lend = CTkLabel(self.details, text = 'Verliehen: ')
        self.lend.pack(pady = 5, padx = 50)

        self.lend_to = CTkLabel(self.details, text = 'Verliehen an: ')
        self.lend_to.pack(pady = 5, padx = 50)

        self.button_frame = CTkFrame(self.preview, fg_color="transparent")
        
        self.button = CTkButton(self.button_frame, text='Mehr anzeigen', command = self.expand)
        self.edit = CTkButton(self.button_frame, text='Bearbeiten', command = self.open_edit)
        self.delete = CTkButton(self.button_frame, text='Löschen', command = self.delete_book)

        self.title.pack(pady = 10, padx = 50)
        self.author.pack(pady = 10, padx = 50)
        self.image.pack(pady = 10, padx = 50)
        self.button_frame.pack(pady = 10)
        self.button.grid(padx = 10, row = 0, column = 0)

        self.refresh()


    def open_edit(self):
        edit = BookEditToplevel(self.id)


    def refresh(self):
        book = fetch_book(self.id)
        self.title.configure(text=book.title)
        authors = fetch_authors_for_book(book.id)
        self.author.configure(text="")
        if len(authors) > 1:
            while len(authors) > 2:
                self.author.configure(text = self.author.cget("text") + authors.pop().getName())
                self.author.configure(text = self.author.cget("text") + ", ")
            self.author.configure(text = self.author.cget("text") + authors.pop().getName())
            self.author.configure(text = self.author.cget("text") + " und ")
        if len(authors) >= 1:
            self.author.configure(text = self.author.cget("text") + authors.pop().getName())
        else:
            self.author.configure(text = self.author.cget("text") + "Unbekannt")

        self.language.configure(text = "Sprache : " + book.language)

        image = get_image(book)

        self.image_data = CTkImage(light_image=image, dark_image=image, size=image.size)
        self.image.configure(image = self.image_data)

        self.publisher.configure(text = f'Verlag: {book.publisher}')

        self.isbn.configure(text = 'ISBN: ')
        isbn_value = str(book.isbn)
        if len(isbn_value) == 13:
            self.isbn.configure(text = f"ISBN: {isbn_value[0:3]}-{isbn_value[3]}-{isbn_value[4:7]}-{isbn_value[7:12]}-{isbn_value[12]}")
        else:
            self.isbn.configure(text = "ISBN: Unbekannt")

        self.edition.configure(text = f'Auflage: {book.edition}')

        self.year.configure(text = f'Jahr: {book.year}')

        self.type.configure(text = f'Buchtyp: {fetch_book_type(book.book_type)}')

        tag_string = ""
        tag_loop = book.tags
        while len(tag_loop) > 1:
            tag_string += f" {tag_loop.pop()};"
        tag_string += f" {tag_loop.pop()}"
        self.tags.configure(text = f'Stichwörter: {tag_string}')

        self.room.configure(text = f'Raum: {fetch_room(book.room)}')

        self.shelf.configure(text = f'Regal: {book.shelf}')

        self.lend.configure(text = f'Verliehen: {"Ja" if book.lend else "Nein"}')

        if book.lend == 1:
            self.lend_to.configure(text=f'Verliehen an: {book.lend_to}')
            self.lend_to.pack(pady=5, padx=20)
        else:
            self.lend_to.pack_forget()

    

    def expand(self):
        self.button_frame.pack_forget()
        self.details.pack()

        self.button.configure(text = 'Weniger anzeigen', command = self.shrink)
        self.edit.grid(row = 0, column = 1, padx=10)
        self.delete.grid(row = 0, column = 2, padx = 10)
        self.button_frame.pack(pady = 10)


    def shrink(self):
        self.button_frame.pack_forget()
        self.details.pack_forget()
        self.button.configure(text = 'Mehr anzeigen', command = self.expand)
        self.edit.grid_forget()
        self.delete.grid_forget()
        self.button_frame.pack(pady = 10)


    def delete_book(self):
        book = fetch_book(self.id)
        decision = CTkMessagebox(title="Bestaetigen", message=f"Möchten Sie das Buch {book.title} wirklich löschen?\n Diese Aktion kann NICHT rückgängig gemacht werden!", icon="question", option_1="Nein", option_2="Ja").get()
        if decision == "Ja":
            app_context.logger.info(f"Deleting book with id {self.id}...")
            delete_book(self.id)
            app_context.mainWindow.refresh()
        

