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
from database import delete_book_type, fetch_book_type
import sys
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from UI.BookType.TypeEditToplevel import TypeEditToplevel


class TypeWidget(CTkFrame):
    def __init__(self, parent, id, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.id = id
        
        self.label = CTkLabel(self, text="Name: ", width=30)
        self.editCTkButton = CTkButton(self, text="Bearbeiten", command=lambda: TypeEditToplevel(self.id))
        self.deleteCTkButton = CTkButton(self, text="Löschen", command=self.delete)

        self.label.grid(row=0, column=0, padx=10, pady=30)
        self.editCTkButton.grid(row=0, column=1, padx=10)
        self.deleteCTkButton.grid(row=0, column=2, padx=10)

        self.refresh()

    def refresh(self):
        book_type = fetch_book_type(self.id)

        self.label.configure(text="Name: " + book_type)

    def delete(self):
        book_type = fetch_book_type(self.id)
        decision = CTkMessagebox(
                                    title="Bestätigen",
                                    message=f"Möchten Sie den Buchtypen {book_type} wirklich löschen?\n\n" +
                                          "Alle Bücher die diesen Buchtypen in ihren Daten enthalten werden statdessen unbekannt anzeigen.\n\n" + 
                                          "Diese Aktion kann NICHT rückgängig gemacht werden!",
                                    icon="question", option_1="Nein", option_2="Ja").get()
        if decision == "Ja":
            app_context.logger.info(f"Deleting type with id {self.id}...")
            delete_book_type(self.id)
            app_context.mainWindow.refresh()

