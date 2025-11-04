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
from database import fetch_room_ids
from tkinter import Frame
from UI.Room.RoomWidget import RoomWidget


class AllRoomsWidget(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        app_context.logger.info("Creating 'all rooms widget'")

        self.rooms = fetch_room_ids()

        self.room_widgets = []

        self.update()

    def update(self):

        app_context.logger.info("Updating 'all rooms widget'")

        self.rooms = fetch_room_ids()

        for widget in self.room_widgets:
            for child in widget.winfo_children():
                child.destroy()
            widget.destroy()
        
        self.room_widgets = []

        for room in self.rooms:
            self.room_widgets.append(RoomWidget(self, room))

        for widget in self.room_widgets:
            widget.pack(pady=20)

