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
from database import get_author_count, get_book_count
from tkinter import Label, Button, Frame
from UI.Tab import Tab
from UI.Book.RecentBooksWidget import RecentBooksWidget
from UI.Author.RecentAuthorsWidget import RecentAuthorsWidget
import webbrowser


class OverviewTab(Tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header_label = Label(self.inner_frame, text='Lerchbacher Bücherdatenbank', font="Arial 25 bold")
        self.header_label.pack(padx=0, pady=10)

        self.statsFrame = Frame(self.inner_frame)
        self.statsFrame.pack(padx=0, pady=10)

        self.statsHeader = Label(self.statsFrame, text="Statistiken", font="Arial 16 bold")
        self.statsHeader.pack()

        self.statsBooks = Label(self.statsFrame, text="Anzahl an Büchern: ")
        self.statsBooks.pack()

        self.statsAuthors = Label(self.statsFrame, text="Anzahl an Autoren: ")
        self.statsAuthors.pack()

        self.recentBooks = RecentBooksWidget(self.inner_frame)
        self.recentBooks.pack(padx=0, pady=10)

        self.recentAuthors = RecentAuthorsWidget(self.inner_frame)
        self.recentAuthors.pack(padx=0, pady=10)

        self.versionLabel = Label(self.inner_frame, text="Version " + app_context.version)
        self.versionLabel.pack()

        self.label = Label(self.inner_frame, text="Brauchen Sie Hilfe? Hier können Sie das ")
        self.button = Button(self.inner_frame, text="Benutzerhandbuch öffnen", command=self.open_user_manual)
        self.label.pack()
        self.button.pack()

        self.update()

    def update(self):
        self.recentBooks.update()
        self.recentAuthors.update()

        numBooks = get_book_count()
        numAuthors = get_author_count()
        self.statsBooks.config(text=f"Number of books: {numBooks}")
        self.statsAuthors.config(text=f"Number of authors: {numAuthors}")


    def open_user_manual(self):
        webbrowser.open(f"https://LarsLerchbacher.github.io/Lerchbacher-Buecherdatenbank/{app_context.version}.html")

