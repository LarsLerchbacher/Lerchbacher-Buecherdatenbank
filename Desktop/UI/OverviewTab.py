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
from database import get_author_count, get_book_count
from customtkinter import CTkLabel, CTkButton, CTkFrame
from UI.Tab import Tab
from UI.Book.RecentBooksWidget import RecentBooksWidget
from UI.Author.RecentAuthorsWidget import RecentAuthorsWidget
import webbrowser


class OverviewTab(Tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header_label = CTkLabel(self, text='Lerchbacher Bücherdatenbank', font=("Arial", 25, "bold"))
        self.header_label.pack(padx=0, pady=10)

        self.stats_frame = CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(padx=0, pady=10)

        self.statsHeader = CTkLabel(self.stats_frame, text="Statistiken", font=("Arial", 16, "bold"))
        self.statsHeader.pack()

        self.statsBooks = CTkLabel(self.stats_frame, text="Anzahl an Büchern: ")
        self.statsBooks.pack()

        self.statsAuthors = CTkLabel(self.stats_frame, text="Anzahl an Autoren: ")
        self.statsAuthors.pack()

        self.recentBooks = RecentBooksWidget(self)
        self.recentBooks.pack(padx=0, pady=10)

        self.recentAuthors = RecentAuthorsWidget(self)
        self.recentAuthors.pack(padx=0, pady=10)

        self.versionCTkLabel = CTkLabel(self, text="Version " + app_context.version)
        self.versionCTkLabel.pack()

        self.label = CTkLabel(self, text="Brauchen Sie Hilfe? Hier können Sie das ")
        self.helpButton = CTkButton(self, text="Benutzerhandbuch öffnen", command=self.open_user_manual)
        self.sourceButton = CTkButton(self, text="Hier kommen Sie zum Quellcode dieser Applikation", command=self.open_source)
        self.label.pack()
        self.helpButton.pack(pady=10)
        self.sourceButton.pack()

        self.refresh()

    def refresh(self):
        self.recentBooks.refresh()
        self.recentAuthors.refresh()

        numBooks = get_book_count()
        numAuthors = get_author_count()
        self.statsBooks.configure(text=f"Anzahl an Büchern: {numBooks}")
        self.statsAuthors.configure(text=f"Anzahl an Autoren: {numAuthors}")

        numBooks = get_book_count()
        numAuthors = get_author_count()
        self.statsBooks.config(text=f"Anzahl an Büchern: {numBooks}")
        self.statsAuthors.config(text=f"Anzahl an Autoren: {numAuthors}")


    def open_user_manual(self):
        webbrowser.open(f"https://LarsLerchbacher.github.io/Lerchbacher-Buecherdatenbank/{app_context.version}.html")

    def open_source(self):
        webbrowser.open("https://github.com/LarsLerchbacher/Lerchbacher-Buecherdatenbank")
