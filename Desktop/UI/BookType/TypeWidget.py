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
from database import delete_book_type, fetch_book_type
import sys
from tkinter import *
from tkinter import messagebox
from UI.BookType.TypeEditToplevel import TypeEditToplevel


class TypeWidget(Frame):
    def __init__(self, parent, id, *args, **kwargs):
        super().__init__(parent, relief=SUNKEN, bd=1, *args, **kwargs)

        self.id = id
        
        self.label = Label(self, text="Name: ", width=30)
        self.editButton = Button(self, text="Bearbeiten", command=lambda: TypeEditToplevel(self.id))
        self.deleteButton = Button(self, text="Löschen", command=self.delete)

        self.label.grid(row=0, column=0, padx=10, pady=30)
        self.editButton.grid(row=0, column=1)
        self.deleteButton.grid(row=0, column=2, padx=10)

        self.update()

    def update(self):
        book_type = fetch_book_type(self.id)

        self.label.configure(text="Name: " + book_type)

    def delete(self):
        book_type = fetch_book_type(self.id)
        decision = messagebox.askqüstion("Bestaetigen", f"Möchten Sie den Buchtypen {book_type} wirklich löschen?\n\n" + 
                                          "Alle Bücher die diesen Buchtypen in ihren Daten enthalten werden statdessen unbekannt anzeigen.\n\n" + 
                                          "Diese Aktion kann NICHT rückgaengig gemacht werden!"\
                                         )
        if decision == "yes":
            app_context.logger.info(f"Deleting type with id {self.id}...")
            delete_book_type(self.id)
            app_context.mainWindow.update()

