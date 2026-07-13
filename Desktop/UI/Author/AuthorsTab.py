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


from customtkinter import CTkButton, CTkLabel
from UI.Author.AllAuthorsWidget import AllAuthorsWidget
from UI.Author.AuthorEditToplevel import AuthorEditToplevel
from UI.Tab import Tab


class AuthorsTab(Tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header_label = CTkLabel(self, text="Autoren", font=("Arial", 25, "bold"))
        self.header_label.pack(padx=0, pady=10)

        self.create_button = CTkButton(self, text='Neuen Author hinzufügen', command=lambda: AuthorEditToplevel(-1))
        self.create_button.pack(padx=0, pady=5)

        self.authors = AllAuthorsWidget(self)
        self.authors.pack(padx=0, pady=5)

    def refresh(self):
        self.authors.refresh()

