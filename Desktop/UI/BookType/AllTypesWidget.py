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
from database import fetch_book_type_ids
from tkinter import Frame
from UI.BookType.TypeWidget import TypeWidget

class AllTypesWidget(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        app_context.logger.info("Creating 'all book_types widget'")

        self.types = fetch_book_type_ids()

        self.type_widgets = []

        self.update()

    def update(self):

        app_context.logger.info("Updating 'all book_types widget'")

        self.types = fetch_book_type_ids()

        for widget in self.type_widgets:
            for child in widget.winfo_children():
                child.destroy()
            widget.destroy()
        
        self.type_widgets = []

        for book_type in self.types:
            self.type_widgets.append(TypeWidget(self, book_type))

        for widget in self.type_widgets:
            widget.pack(pady=20)

