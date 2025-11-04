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
from database import fetch_books
from tkinter import Frame, Label
from UI.Book.BookWidget import BookWidget

class RecentBooksWidget(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app_context.logger.info("Creating 'recent books widget'")
        all_books = fetch_books()
        self.books = all_books[-12:]

        self.header = Label(self, text="Neueste Bücher", font="Arial 14 bold")
        self.bookWidgets = []

        self.header.pack()

        self.update()

    def update(self):
        app_context.logger.info("Updating 'recent books widget'")
        all_books = fetch_books()
        self.books = all_books[-12:]
        
        for bookWidget in self.bookWidgets:
            for child in bookWidget.winfo_children():
                child.destroy()
            bookWidget.destroy()

        self.bookWidgets = []

        for book in self.books:
            self.bookWidgets.append(BookWidget(self, book.id))

        for bookWidget in self.bookWidgets:
            bookWidget.pack(pady=20)

