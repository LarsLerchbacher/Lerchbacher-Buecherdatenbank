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


from database import fetch_book_types, fetch_rooms
from tkinter import *
from tkinter.ttk import Spinbox
from ttkwidgets.autocomplete import AutocompleteCombobox
from UI.Author.AuthorSelectWidget import AuthorSelectWidget
from UI.ISBNWidget import ISBNWidget


class BookEditWidget(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title_frame = Frame(self)
        self.title_frame.pack(padx=20, pady=20)

        self.title_label = Label(self.title_frame, text="Titel: ")
        self.title = Entry(self.title_frame, width=75)
        self.title_label.grid(row=0, column=0)
        self.title.grid(row=0, column=1, columnspan=4)

        self.authors_frame = Frame(self)
        self.authors_frame.pack(padx=20, pady=5)

        self.authors_label = Label(self.authors_frame, text="Autoren: ")
        self.authors = AuthorSelectWidget(self.authors_frame, [])
        self.authors_label.grid(row=0, column=0)
        self.authors.grid(row=1, column=0, pady=20)

        self.publisher_frame = Frame(self)
        self.publisher_frame.pack(padx=20, pady=5)

        self.publisher_label = Label(self.publisher_frame, text="Verlag: ")
        self.publisher = Entry(self.publisher_frame, width=50)
        self.publisher_label.grid(row=0, column=0)
        self.publisher.grid(row=0, column=1, columnspan=3)

        self.isbn_frame = Frame(self)
        self.isbn_frame.pack(padx=20, pady=5)

        self.isbn_label = Label(self.isbn_frame, text="  ISBN: ")
        self.isbn = ISBNWidget(self.isbn_frame, width=50)
        self.isbn_label.grid(row=0, column=0)
        self.isbn.grid(row=0, column=1, columnspan=3)

        self.edition_frame = Frame(self)
        self.edition_frame.pack(padx=20, pady=5)

        self.edition_label = Label(self.edition_frame, text='Auflage: ')
        self.edition = Spinbox(self.edition_frame, increment=1, from_=1, to=20, wrap=True, width=25)
        self.edition_label.grid(row=0, column=0)
        self.edition.grid(row=0, column=1)

        self.year_frame = Frame(self)
        self.year_frame.pack(padx=20, pady=5)

        self.year_label = Label(self.year_frame, text="Jahr: ")
        self.year = Spinbox(self.year_frame, increment=1, from_=1800, to=2099, wrap=True, width=25)
        self.year_label.grid(row=0, column=0)
        self.year.grid(row=0, column=1)

        self.type_frame = Frame(self)
        self.type_frame.pack(padx=20, pady=5)

        self.all_types = fetch_book_types()
        self.type_label = Label(self.type_frame, text="Typ: ")
        self.type_select = AutocompleteCombobox(self.type_frame, completevalues=self.all_types, width=25)
        self.type_label.grid(row=0, column=0)
        self.type_select.grid(row=0, column=1)

        self.tags_frame = Frame(self)
        self.tags_frame.pack(padx=20, pady=5)

        self.tags_label = Label(self.tags_frame, text="Kategorien (durch ';' getrennt): ")
        self.tags = Entry(self.tags_frame, width=50)
        self.tags_label.grid(row=0, column=0)
        self.tags.grid(row=0, column=1)

        self.room_frame = Frame(self)
        self.room_frame.pack(padx=20, pady=5)

        self.all_rooms = fetch_rooms()
        self.room_label = Label(self.room_frame, text='Raum: ')
        self.room = AutocompleteCombobox(self.room_frame, completevalues=self.all_rooms, width=25)
        self.room_label.grid(row=0, column=0)
        self.room.grid(row=0, column=1)

        self.shelf_frame = Frame(self)
        self.shelf_frame.pack(padx=20, pady=5)
        
        self.shelf_label = Label(self.shelf_frame, text='Regal: ')
        self.shelf = Entry(self.shelf_frame, width=25)
        self.shelf_label.grid(row=0, column=0)
        self.shelf.grid(row=0, column=1)

        self.lend_frame = Frame(self)
        self.lend_frame.pack(padx=20, pady=5)

        self.lend_label = Label(self.lend_frame, text='Verliehen : ')
        self.lend_var = IntVar()
        self.lend = Checkbutton(self.lend_frame, variable=self.lend_var)
        self.lend_label.grid(row=0, column=0)
        self.lend.grid(row=0, column=1)

        self.lend_to_frame = Frame(self)

        self.lend_to_label = Label(self.lend_to_frame, text="Verliehen an: ")
        self.lend_to = Entry(self.lend_to_frame)
        self.lend_to_label.grid(row=1, column=0)
        self.lend_to.grid(row=1, column=1)

    def update_lend_to(self):
        print(self.lend_var.get())
        if self.lend_var.get() == 1:
            self.lend_to_frame.pack(padx=20, pady=5)
        else:
            self.lend_to_frame.pack_forget()
