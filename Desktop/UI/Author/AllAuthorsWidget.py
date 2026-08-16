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
from database import fetch_authors
from UI.Author.AuthorWidget import AuthorWidget
from customtkinter import CTkFrame


class AllAuthorsWidget(CTkFrame):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(*args, **kwargs)
        app_context.logger.info("Creating 'all authors widget'")
        self.authors = fetch_authors()

        self.authorWidgets = []

        self.refresh()


    def refresh(self):
        app_context.logger.info("Updating 'all authors widget'")
        self.authors = fetch_authors()

        # Deleting all old Author widgets
        for authorWidget in self.authorWidgets:
            authorWidget.destroy()

        self.authorWidgets = []

        # Creating a new AuthorWidget for every author in the list
        for author in self.authors:
            self.authorWidgets.append(AuthorWidget(self, author.id))

        # Displaying the AuthorWidgets
        for authorWidget in self.authorWidgets:
            authorWidget.pack(pady=20)

