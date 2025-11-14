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
from database import delete_room, fetch_room
from tkinter import *
from tkinter import messagebox
from UI.Room.RoomEditToplevel import RoomEditToplevel


class RoomWidget(Frame):
    def __init__(self, parent, id, *args, **kwargs):
        super().__init__(parent, relief=SUNKEN, bd=1, *args, **kwargs)

        self.id = id
        
        self.label = Label(self, text="Name: ", width=30)
        self.editButton = Button(self, text="Bearbeiten", command=lambda: RoomEditToplevel(self.id))
        self.deleteButton = Button(self, text="Löschen", command=self.delete)

        self.label.grid(row=0, column=0, padx=10, pady=30)
        self.editButton.grid(row=0, column=1)
        self.deleteButton.grid(row=0, column=2, padx=10)

        self.update()

    def update(self):
        room = fetch_room(self.id)

        self.label.configure(text="Name: "+room)

    def delete(self):
        room = fetch_room(self.id)
        decision = messagebox.askquestion("Bestaetigen", f"Möchten Sie den Raum {room} wirklich löschen?\n\n" +
                                          "Alle Bücher die diesen Raum in ihren Daten enthalten werden statdessen unbekannt anzeigen.\n\n" + 
                                          "Diese Aktion kann NICHT rückgaengig gemacht werde!"\
                                         )
        if decision == "yes":
            app_context.logger.info(f"Deleting room with id {self.id}...")
            delete_room(self.id)
            app_context.mainWindow.update()


