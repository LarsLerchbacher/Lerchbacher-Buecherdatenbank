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


from tkinter import *


class ISBNWidget(Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<KeyRelease>", self.format)

    def format(self, event):
        position = self.index(INSERT)
        if position in [3, 5, 8, 15] and not event.keysym in ["BackSpace", "Left", "Right"]:
            # Insert dash
            self.insert(INSERT, '-')

            # Move cursor
            self.icursor(position + 1)

        elif position > 13 or len(self.get()) > 17:
            # Limit input length
            self.delete(17, END)

    def get(self):
        text = super().get()
        text = text.replace('-', '')
        return text
