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
from images import rescale_image, get_image
from database import delete_book, fetch_author, fetch_book, fetch_room, fetch_book_type
import PIL
from PIL import ImageTk
from tkinter import *
from tkinter import messagebox
from UI.Book.BookEditToplevel import BookEditToplevel


class BookWidget(Frame):
    def __init__(self, parent, id: int, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.id = id

        self.preview = Frame(self, relief=SUNKEN, bd=1)
        self.details = Frame(self.preview)
        self.preview.pack()

        self.title = Label(self.preview, text = "", font="Arial 16 bold", wraplength=500, justify='center')
        self.author = Label(self.preview, text = "", font = "Arial 12")

        image_data = PIL.Image.open("./img/noCover.png")
        image_data = rescale_image(image_data)
        self.image_tk = ImageTk.PhotoImage(image_data)
        self.image = Label(self.details, image = self.image_tk)

        self.publisher = Label(self.details, text = 'Verlag: ')
        self.publisher.pack(pady = 5, padx = 50)

        self.isbn = Label(self.details, text = 'ISBN: ')
        self.isbn.pack(pady = 5, padx = 50)

        self.edition = Label(self.details, text = 'Auflage Nr.:')
        self.edition.pack(pady = 5, padx = 50)        

        self.year = Label(self.details, text = 'Jahr: ')
        self.year.pack(pady = 5, padx = 50)

        self.type = Label(self.details, text = 'Buchtyp: ')
        self.type.pack(pady = 5, padx = 50)

        self.tags = Label(self.details, text = 'Kategorie(n): ')
        self.tags.pack(pady = 5, padx = 50)

        self.room = Label(self.details, text = 'Raum: ')
        self.room.pack(pady = 5, padx = 50)

        self.shelf = Label(self.details, text = 'Regal: ')
        self.shelf.pack(pady = 5, padx = 50)

        self.lend = Label(self.details, text = 'Verliehen: ')
        self.lend.pack(pady = 5, padx = 50)

        self.lend_to = Label(self.details, text = 'Verliehen an: ')
        self.lend_to.pack(pady = 5, padx = 50)

        self.button_frame = Frame(self.preview)
        
        self.button = Button(self.button_frame, text='Mehr anzeigen', command = self.expand)
        self.edit = Button(self.button_frame, text = 'Bearbeiten', command = self.open_edit)
        self.delete = Button(self.button_frame, text = 'Löschen', command = self.delete_book)

        self.title.pack(pady = 10, padx = 50)
        self.author.pack(pady = 10, padx = 50)
        self.image.pack(pady = 10, padx = 50)
        self.button_frame.pack(pady = 10, padx = 250)
        self.button.grid(padx = 10, row = 0, column = 0)

        self.update()


    def open_edit(self):
        edit = BookEditToplevel(self.id)


    def update(self):
        book = fetch_book(self.id)
        self.title.config(text=book.title)
        authors = [fetch_author(id) for id in book.author_ids] 
        self.author.config(text="")
        if len(authors) > 1:
            while len(authors) > 2:
                self.author.config(text = self.author["text"] + authors.pop().name)
                self.author.config(text = self.author["text"] + ", ")
            self.author.config(text = self.author["text"] + authors.pop().name)
            self.author.config(text = self.author["text"] + " und ")
        self.author.config(text = self.author["text"] + authors.pop().name)

        image = get_image(book)

        self.image_data = PIL.ImageTk.PhotoImage(image)
        self.image.config(image = self.image_data)

        self.publisher.config(text = f'Verlag: {book.publisher}')

        self.isbn.config(text = 'ISBN: ')
        isbn_value = str(book.isbn)
        if len(isbn_value) == 13:
            self.isbn.config(text = f"ISBN: {isbn_value[0:3]}-{isbn_value[3]}-{isbn_value[4:7]}-{isbn_value[7:12]}-{isbn_value[12]}")
        else:
            self.isbn.config(text = "ISBN: Unbekannt")

        self.edition.config(text = f'Auflage: {book.edition}')

        self.year.config(text = f'Jahr: {book.year}')

        self.type.config(text = f'Buchtyp: {fetch_book_type(book.type)}')

        tag_string = ""
        tag_loop = book.tags
        while len(tag_loop) > 1:
            tag_string += f" {tag_loop.pop()};"
        tag_string += f" {tag_loop.pop()}"
        self.tags.config(text = f'Kategorie(n): {tag_string}')

        self.room.config(text = f'Raum: {fetch_room(book.room)}')

        self.shelf.config(text = f'Regal: {book.shelf}')

        self.lend.config(text = f'Verliehen: {"Ja" if book.lend else "Nein"}')

        if book.lend == 1:
            self.lend_to.config(text=f'Verliehen an: {book.lend_to}')
            self.lend_to.pack(pady=5, padx=20)
        else:
            self.lend_to.pack_forget()

    

    def expand(self):
        self.button_frame.pack_forget()
        self.details.pack()

        self.button.configure(text = 'Weniger anzeigen', command = self.shrink)
        self.edit.grid(row = 0, column = 1)
        self.delete.grid(row = 0, column = 2, padx = 10)
        self.button_frame.pack(pady = 10, padx = 250)


    def shrink(self):
        self.button_frame.pack_forget()
        self.details.pack_forget()
        self.button.configure(text = 'Mehr anzeigen', command = self.expand)
        self.edit.grid_forget()
        self.delete.grid_forget()
        self.button_frame.pack(pady = 10, padx = 250)


    def delete_book(self):
        book = fetch_book(self.id)
        decision = messagebox.askquestion("Bestaetigen", f"Moechten Sie das Buch {book.title} wirklich löschen?\n Diese Aktion kann NICHT rückgaengig gemacht werden!")
        if decision == "yes":
            app_context.logger.info(f"Deleting book with id {self.id}...")
            delete_book(self.id)
            app_context.mainWindow.update()
        

