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


from tkinter import Label, Button
from UI.Tab import Tab
from UI.Book.RecentBooksWidget import RecentBooksWidget
from UI.Author.RecentAuthorsWidget import RecentAuthorsWidget
import webbrowser


class OverviewTab(Tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header_label = Label(self.inner_frame, text='Lerchbacher Bücherdatenbank', font="Arial 25 bold")
        self.header_label.pack(padx=0, pady=10)

        self.recentBooks = RecentBooksWidget(self.inner_frame)
        self.recentBooks.pack(padx=0, pady=10)

        self.recentAuthors = RecentAuthorsWidget(self.inner_frame)
        self.recentAuthors.pack(padx=0, pady=10)

        self.label = Label(self.inner_frame, text="Brauchen Sie Hilfe? Hier koennen Sie das ")
        self.button = Button(self.inner_frame, text="Benutzerhandbuch oeffnen", command=self.open_user_manual)
        self.label.pack()
        self.button.pack()

    def update(self):
        self.recentBooks.update()
        self.recentAuthors.update()


    def open_user_manual(self):
        webbrowser.open("https://LarsLerchbacher.github.io/Lerchbacher-Buecherdatenbank")

