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
from database import Author, create_author, edit_author, fetch_author
from tkinter import *
from tkinter.messagebox import showerror


class AuthorEditToplevel(Toplevel):
    def __init__(self, id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        if self.id != -1:
            app_context.logger.info(f"Opening author editing dialog for author with id {self.id}")
        else:
            app_context.logger.info("Opening empty author editing dialog")
        
        self.fnLabel = Label(self, text="First name: ")
        self.lnLabel = Label(self, text="Last name: ")
        self.firstName = Entry(self, width=50)
        self.lastName = Entry(self, width=50)

        self.fnLabel.grid(row=0, column=0, padx=10, pady=10)
        self.firstName.grid(row=0, column=1, padx=10)
        self.lnLabel.grid(row=1, column=0, padx=10, pady=10)
        self.lastName.grid(row=1, column=1, padx=10)

        self.buttonFrame = Frame(self)
        self.buttonFrame.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

        self.saveButton = Button(self.buttonFrame, text='Speichern', command=self.save)
        self.cancelButton = Button(self.buttonFrame, text='Abbrechen', command=self.cancel)
        self.saveButton.grid(row=0, column=0)
        self.cancelButton.grid(row=0, column=1, padx=10)

        self.firstName.focus_set()
        self.bind("<Return>", lambda e: self.save())

        if self.id != -1:
            self.update()

    def update(self):
        author = fetch_author(self.id)
        if not type(author) == Author:
            showerror("ERROR", "Autor nicht gefunden!")
        else:
            self.firstName.delete(0, END)
            self.lastName.delete(0, END)

            self.firstName.insert(0, author.firstName)
            self.lastName.insert(0, author.lastName)


    def save(self):
        firstName = self.firstName.get()
        lastName = self.lastName.get()

        if self.id != -1:
            new_author = Author(id, firstName, lastName)
            response = edit_author(self.id, new_author)
            if response != "OK":
                app_context.logger.error(f"Speichern nicht möglich!\n{response}")
                showerror(title="Speichern nicht möglich!", message=response)
            else:
                app_context.logger.info("Erfolgreich gespeichert!")
                app_context.mainWindow.update()
                self.destroy()
        else:
            new_author = Author(-1, firstName, lastName)
            response = create_author(new_author)
            if response != "OK":
                app_context.logger.info(f"Speicher nicht möglich\n{response}")
                showerror(title="Speichern nicht möglich!", message=response)
            else:
                app_context.logger.info("Erfolgreich gespeichert!")
                app_context.mainWindow.update()
                self.destroy()


    def cancel(self):
        if self.id == -1:
            app_context.logger.info("Closed empty author editing dialog wihtout saving")
        else:
            app_context.logger.info(f"Closed author editing dialog for author with id {self.id} wihtout saving")

        self.destroy()

