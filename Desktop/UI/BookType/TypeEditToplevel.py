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
from database import create_book_type, edit_book_type, fetch_book_type
from tkinter import *


class TypeEditToplevel(Toplevel):
    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = id

        self.label = Label(self, text="Name: ")
        self.entry = Entry(self, width=30)

        self.buttonFrame = Frame(self)

        self.saveButton = Button(self.buttonFrame, text="Speichern", command=self.save)
        self.cancelButton = Button(self.buttonFrame, text="Abbrechen", command=self.cancel)

        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.entry.grid(row=0, column=1, padx=10)
        self.buttonFrame.grid(row=1, columnspan=2, padx=10, pady=10)

        self.saveButton.grid(row=0, column=0, padx=10)
        self.cancelButton.grid(row=0, column=1)

        if id != -1:
            self.update()

    def update(self):
        book_type = fetch_book_type(self.id)

        self.entry.delete(0, END)
        self.entry.insert(0, book_type)

    def save(self):
        book_type = self.entry.get()
        if self.id != -1:
            response = edit_book_type(self.id, book_type)
            if response != "OK":
                app_context.logger.error(f"Speichern nicht möglich!\n{response}")
                showerror(title="Speichern nicht möglich!", message=response)
            else:
                app_context.logger.info("Erfolgreich gespeichert")
                app_context.mainWindow.update()
                self.destroy()

        else:
            response = create_book_type(book_type)
            if response != "OK":
                app_context.logger.error(f"Speichern nicht möglich!\n{response}")
                showerror(title="Speichern nicht möglich!", message=response)
            else:
                app_context.logger.info(f"Created (book) type with name {book_type}")
                app_context.mainWindow.update()
                self.destroy()


    def cancel(self):
        if self.id == -1:
            app_context.logger.info("Closed empty book_type editing dialog wihtout saving")
        else:
            app_context.logger.info(f"Closed book_type editing dialog for book_type with id {self.id} wihtout saving")

        self.destroy()

