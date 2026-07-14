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
from database import create_room, edit_room, fetch_room
from customtkinter import *


class RoomEditToplevel(CTkToplevel):
    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = id

        self.label = CTkLabel(self, text="Name: ")
        self.entry = CTkEntry(self)

        self.buttonCTkFrame = CTkFrame(self, fg_color="transparent")

        self.saveCTkButton = CTkButton(self.buttonCTkFrame, text="Speichern", command=self.save)
        self.cancelCTkButton = CTkButton(self.buttonCTkFrame, text="Abbrechen", command=self.cancel)

        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.entry.grid(row=0, column=1, padx=10)
        self.buttonCTkFrame.grid(row=1, columnspan=2, padx=10, pady=10)

        self.saveCTkButton.grid(row=0, column=0, padx=10)
        self.cancelCTkButton.grid(row=0, column=1)

        self.entry.focus_set()
        self.bind("<Return>", lambda e: self.save())

        if id != -1:
            self.refresh()

    def refresh(self):
        room = fetch_room(self.id)

        self.entry.delete(0, END)
        self.entry.insert(0, room)

    def save(self):
        room = self.entry.get()
        if self.id != -1:
            response = edit_room(self.id, room)
            if response != "OK":
                app_context.logger.error(f"Speichern nicht möglich!\n{response}")
                CTkMessageBox(title="Speichern nicht möglich!", message=response, icon="error")
            else:
                app_context.logger.info("Erfolgreich gespeichert")
                app_context.mainWindow.refresh()
                self.destroy()

        else:
            response = create_room(room)
            if response != "OK":
                app_context.logger.error(f"Speichern nicht möglich!\n{response}")
                CTkMessageBox(title="Speichern nicht möglich!", message=response, icon="error")
            else:
                app_context.logger.info(f"Created room with name {room}")
                app_context.mainWindow.refresh()
                self.destroy()


    def cancel(self):
        if self.id == -1:
            app_context.logger.info("Closed empty room editing dialog wihtout saving")
        else:
            app_context.logger.info(f"Closed room editing dialog for room with id {self.id} wihtout saving")

        self.destroy()

