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
from customtkinter import *
from CTkSpinbox import CTkSpinbox
from ttkwidgets.autocomplete import AutocompleteCombobox
from UI.Author.AuthorSelectWidget import AuthorSelectWidget
from UI.ISBNWidget import ISBNWidget


class BookEditWidget(CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(*args, **kwargs)
        
        # Configure the scrollable frame to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_frame = CTkFrame(self, fg_color="transparent")
        self.title_frame.pack(padx=20, pady=20, expand=True, fill="x")

        self.title_label = CTkLabel(self.title_frame, text="Titel*: ")
        self.title = CTkEntry(self.title_frame)
        self.title_label.grid(row=0, column=0, sticky="w")
        self.title.grid(row=0, column=1, columnspan=4, sticky="ew", padx=10)
        
        # Configure grid weights for the title frame
        self.title_frame.grid_columnconfigure(1, weight=1)

        self.authors_frame = CTkFrame(self, fg_color="transparent")
        self.authors_frame.pack(padx=20, pady=5, expand=True)

        self.authors_label = CTkLabel(self.authors_frame, text="Autoren*: ")
        self.authors = AuthorSelectWidget(self.authors_frame, [])
        self.authors_label.grid(row=0, column=0)
        self.authors.grid(row=1, column=0, pady=20)

        self.language_frame = CTkFrame(self, fg_color="transparent")
        self.language_frame.pack(padx=20, pady=5, expand=True)

        self.language_label = CTkLabel(self.language_frame, text="Sprache: ")
        self.language = CTkEntry(self.language_frame)
        self.language_label.grid(row=0, column=0, sticky="w")
        self.language.grid(row=0, column=1, sticky="ew", padx=10)
        
        # Configure grid weights for the language frame
        self.language_frame.grid_columnconfigure(1, weight=1)

        self.publisher_frame = CTkFrame(self, fg_color="transparent")
        self.publisher_frame.pack(padx=20, pady=5, expand=True)

        self.publisher_label = CTkLabel(self.publisher_frame, text="Verlag: ")
        self.publisher = CTkEntry(self.publisher_frame)
        self.publisher_label.grid(row=0, column=0, sticky="w")
        self.publisher.grid(row=0, column=1, columnspan=3, sticky="ew", padx=10)
        
        # Configure grid weights for the publisher frame
        self.publisher_frame.grid_columnconfigure(1, weight=1)

        self.isbn_frame = CTkFrame(self, fg_color="transparent")
        self.isbn_frame.pack(padx=20, pady=5, expand=True)

        self.isbn_label = CTkLabel(self.isbn_frame, text="  ISBN: ")
        self.isbn = ISBNWidget(self.isbn_frame)
        self.isbn_label.grid(row=0, column=0, sticky="w")
        self.isbn.grid(row=0, column=1, columnspan=3, sticky="ew", padx=10)
        
        # Configure grid weights for the ISBN frame
        self.isbn_frame.grid_columnconfigure(1, weight=1)

        self.edition_frame = CTkFrame(self, fg_color="transparent")
        self.edition_frame.pack(padx=20, pady=5, expand=True)

        self.edition_label = CTkLabel(self.edition_frame, text='Auflage: ')
        self.edition = CTkSpinbox(self.edition_frame, step_value=1, min_value=1, max_value=20, font=("Arial", 12))
        self.edition_label.grid(row=0, column=0, sticky="w")
        self.edition.grid(row=0, column=1, sticky="ew", padx=10)
        
        # Configure grid weights for the edition frame
        self.edition_frame.grid_columnconfigure(1, weight=1)

        self.year_frame = CTkFrame(self, fg_color="transparent")
        self.year_frame.pack(padx=20, pady=5, expand=True)

        self.year_label = CTkLabel(self.year_frame, text="Jahr: ")
        self.year = CTkSpinbox(self.year_frame, step_value=1, min_value=1800, max_value=2099, font=("Arial", 12))
        self.year_label.grid(row=0, column=0, sticky="w")
        self.year.grid(row=0, column=1, sticky="ew", padx=10)
        
        # Configure grid weights for the year frame
        self.year_frame.grid_columnconfigure(1, weight=1)

        self.type_frame = CTkFrame(self, fg_color="transparent")
        self.type_frame.pack(padx=20, pady=5, expand=True)

        self.all_types = fetch_book_types()
        self.type_label = CTkLabel(self.type_frame, text="Typ*: ")
        self.type_select = CTkComboBox(self.type_frame, values=self.all_types)
        self.type_label.grid(row=0, column=0, sticky="w")
        self.type_select.grid(row=0, column=1, sticky="ew", padx=10)
        
        # Configure grid weights for the type frame
        self.type_frame.grid_columnconfigure(1, weight=1)

        self.tags_frame = CTkFrame(self, fg_color="transparent")
        self.tags_frame.pack(padx=20, pady=5, expand=True)

        self.tags_label = CTkLabel(self.tags_frame, text="Stichwörter (durch ';' getrennt): ")
        self.tags = CTkEntry(self.tags_frame)
        self.tags_label.grid(row=0, column=0, sticky="w")
        self.tags.grid(row=0, column=1, sticky="ew", padx=10)
        
        # Configure grid weights for the tags frame
        self.tags_frame.grid_columnconfigure(1, weight=1)

        self.room_frame = CTkFrame(self, fg_color="transparent")
        self.room_frame.pack(padx=20, pady=5, expand=True)

        self.all_rooms = fetch_rooms()
        self.room_label = CTkLabel(self.room_frame, text='Raum*: ')
        self.room = CTkComboBox(self.room_frame, values=self.all_rooms)
        self.room_label.grid(row=0, column=0, sticky="w")
        self.room.grid(row=0, column=1, sticky="ew", padx=10)
        
        # Configure grid weights for the room frame
        self.room_frame.grid_columnconfigure(1, weight=1)

        self.shelf_frame = CTkFrame(self, fg_color="transparent")
        self.shelf_frame.pack(padx=20, pady=5, expand=True)
        
        self.shelf_label = CTkLabel(self.shelf_frame, text='Regal: ')
        self.shelf = CTkEntry(self.shelf_frame)
        self.shelf_label.grid(row=0, column=0, sticky="w")
        self.shelf.grid(row=0, column=1, sticky="ew", padx=10)
        
        # Configure grid weights for the shelf frame
        self.shelf_frame.grid_columnconfigure(1, weight=1)

        self.lend_frame = CTkFrame(self, fg_color="transparent")
        self.lend_frame.pack(padx=20, pady=5, expand=True)

        self.lend_var = IntVar()
        self.lend = CTkCheckBox(self.lend_frame, variable=self.lend_var, text="Verliehen?")
        self.lend.grid(row=0, column=0, columnspan=2)

        self.lend_to_frame = CTkFrame(self, fg_color="transparent")

        self.lend_to_label = CTkLabel(self.lend_to_frame, text="Verliehen an: ")
        self.lend_to = CTkEntry(self.lend_to_frame)
        self.lend_to_label.grid(row=1, column=0, sticky="w")
        self.lend_to.grid(row=1, column=1, sticky="ew", padx=10)
        
        # Configure grid weights for the lend_to frame
        self.lend_to_frame.grid_columnconfigure(1, weight=1)

    def update_lend_to(self):
        if self.lend_var.get() == 1:
            self.lend_to_frame.pack(padx=20, pady=5, expand=True)
        else:
            self.lend_to_frame.pack_forget()

    def check_is_filled(self):
        filled = True

        if self.title.get() == "":
            filled = False

        elif self.authors.get() == []:
            filled = False

        elif self.type_select.get() == "":
            filled = False

        elif self.room.get() == "":
            filled = False

        return filled


