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
from database import fetch_rooms, fetch_book_types
from tkinter import Frame, Label
from ttkwidgets.autocomplete import AutocompleteCombobox
from UI.Book.BookEditWidget import BookEditWidget


class SearchFilterBooks(BookEditWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title_label.config(text="Titel: ")
        self.authors_label.config(text="Autoren: ")
        self.type_label.config(text="Typ: ")
        self.room_label.config(text="Raum: ")

        self.lend = AutocompleteCombobox(self.lend_frame, completevalues=["Ja", "Nein"], width=25, postcommand=self.update)
        self.lend.grid(row=0, column=1)

        self.lend.bind("<<ComboboxSelected>>", self.update_lend_to)
    
    def update(self):
        app_context.logger.info("Updating Search filters for books")
        self.authors.update()
        self.all_rooms = fetch_rooms()
        self.all_types = fetch_book_types()
        self.room.config(completevalues=self.all_rooms)
        self.type_select.config(completevalues=self.all_types)


    def update_lend_to(self, event_object):
        if self.lend.get() == "Ja":
            self.lend_to_frame.pack(padx=20, pady=5)
        else:
            self.lend_to_frame.pack_forget()

