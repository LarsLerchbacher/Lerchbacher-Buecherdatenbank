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


from tkinter import Frame, Label
from ttkwidgets.autocomplete import AutocompleteCombobox
from UI.Book.BookEditWidget import BookEditWidget


class SearchFilterBooks(BookEditWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.lend = AutocompleteCombobox(self.lend_frame, completevalues=["Ja", "Nein"], width=25)
        self.lend.grid(row=0, column=1)

