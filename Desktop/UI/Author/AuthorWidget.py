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
from database import delete_author, fetch_author
from tkinter import *
from tkinter import messagebox
from UI.Author.AuthorEditToplevel import AuthorEditToplevel


class AuthorWidget(Frame):
    def __init__(self, parent, id, *args, **kwargs):
        super().__init__(parent, relief=SUNKEN, bd=1, *args, **kwargs)

        self.id = id

        self.firstName = Label(self)
        self.lastName = Label(self)

        self.buttonFrame = Frame(self)

        self.editButton = Button(self.buttonFrame, text='Bearbeiten', command=lambda:AuthorEditToplevel(self.id))
        self.deleteButton = Button(self.buttonFrame, text='Löschen', command=self.delete)

        self.firstName.grid(row=0, column=0, padx=100, pady=5)
        self.lastName.grid(row=1, column=0, padx=100, pady=5)
        self.buttonFrame.grid(row=2, column=0)
        self.editButton.grid(row=0, column=1, pady=10)
        self.deleteButton.grid(row=0, column=2, padx=10, pady=10)


        if self.id != -1:
            self.update()

    
    def update(self):

        author = fetch_author(self.id)

        self.firstName.config(text=f"First Name: {author.firstName}")
        self.lastName.config(text=f"Last Name: {author.lastName}")


    def delete(self):
        author = fetch_author(self.id)
        decision = messagebox.askquestion("Bestaetigen", f"Möchten Sie den Autor {author.getName()} wirklich löschen?\n Diese Aktion kann NICHT rueckgaengig gemacht werden!")
        if decision == "yes":
            app_context.logger.info(f"Deleting author with id {self.id}...")
            delete_author(self.id)
            app_context.mainWindow.update()

