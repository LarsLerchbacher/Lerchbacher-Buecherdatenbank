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
from database import fetch_room_ids
from customtkinter import CTkFrame
from UI.Room.RoomWidget import RoomWidget


class AllRoomsWidget(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(parent, *args, **kwargs)

        app_context.logger.info("Creating 'all rooms widget'")

        self.rooms = fetch_room_ids()

        self.room_widgets = []

        self.refresh()

    def refresh(self):

        app_context.logger.info("Updating 'all rooms widget'")

        self.rooms = fetch_room_ids()

        for widget in self.room_widgets:
            widget.destroy()
        
        self.room_widgets = []

        for room in self.rooms:
            self.room_widgets.append(RoomWidget(self, room))

        for widget in self.room_widgets:
            widget.pack(pady=20)

