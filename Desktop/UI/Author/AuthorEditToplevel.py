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
from database import Author, create_author, edit_author, fetch_author
from customtkinter import *
from CTkMessagebox import CTkMessagebox


class AuthorEditToplevel(CTkToplevel):
    def __init__(self, id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Autor bearbeiten")

        self.id = id
        if self.id != -1:
            app_context.logger.info(f"Opening author editing dialog for author with id {self.id}")
        else:
            app_context.logger.info("Opening empty author editing dialog")
        
        self.fnCTkLabel = CTkLabel(self, text="Vorname: ")
        self.lnCTkLabel = CTkLabel(self, text="Nachname: ")
        self.firstName = CTkEntry(self)
        self.lastName = CTkEntry(self)

        self.fnCTkLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.firstName.grid(row=0, column=1, padx=10, sticky="ew")
        self.lnCTkLabel.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.lastName.grid(row=1, column=1, padx=10, sticky="ew")
        
        # Configure grid weights
        self.grid_columnconfigure(1, weight=1)

        self.buttonCTkFrame = CTkFrame(self, fg_color="transparent")
        self.buttonCTkFrame.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

        self.saveCTkButton = CTkButton(self.buttonCTkFrame, text='Speichern', command=self.save)
        self.cancelCTkButton = CTkButton(self.buttonCTkFrame, text='Abbrechen', command=self.cancel)
        self.saveCTkButton.grid(row=0, column=0)
        self.cancelCTkButton.grid(row=0, column=1, padx=10)

        self.firstName.focus_set()
        self.bind("<Return>", lambda e: self.save())

        if self.id != -1:
            self.refresh()

    def refresh(self):
        author = fetch_author(self.id)
        if not type(author) == Author:
            CTkMessagebox(title="ERROR", message="Autor nicht gefunden!", icon="error")
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
                CTkMessagebox(title="Speichern nicht möglich!", message=response, icon="error")
            else:
                app_context.logger.info("Erfolgreich gespeichert!")
                app_context.mainWindow.refresh()
                self.destroy()
        else:
            new_author = Author(-1, firstName, lastName)
            response = create_author(new_author)
            if response != "OK":
                app_context.logger.info(f"Speicher nicht möglich\n{response}")
                CTkMessagebox(title="Speichern nicht möglich!", message=response, icon="error")
            else:
                app_context.logger.info("Erfolgreich gespeichert!")
                app_context.mainWindow.refresh()
                self.destroy()


    def cancel(self):
        if self.id == -1:
            app_context.logger.info("Closed empty author editing dialog wihtout saving")
        else:
            app_context.logger.info(f"Closed author editing dialog for author with id {self.id} wihtout saving")

        self.destroy()

