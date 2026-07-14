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
from database import fetch_books
from customtkinter import CTkFrame
from UI.Book.BookWidget import BookWidget


class AllBooksWidget(CTkFrame):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(*args, **kwargs)
        app_context.logger.info("Creating 'all books widget'")
        self.books = fetch_books()

        self.bookWidgets = []

        
        self.refresh()

    def refresh(self):
        app_context.logger.info("Updating 'all books widget'")
        self.books = fetch_books()
        
        for bookWidget in self.bookWidgets:
            for child in bookWidget.winfo_children():
                child.destroy()
            bookWidget.destroy()
        
        self.bookWidgets = []

        for book in self.books:
            self.bookWidgets.append(BookWidget(self, book.id))

        for bookWidget in self.bookWidgets:
            bookWidget.pack(pady=20)

