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


from ttkwidgets.autocomplete import AutocompleteCombobox
from UI.Author.AuthorEditWidget import AuthorEditWidget


class SearchFilterAuthors(AuthorEditWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dobLabel.config(text='Geburtsdatum (Unbekannt = 12.12.2200, Ignorieren = 1.1.2200): ')
        self.dodLabel.config(text='Sterbedatum (Noch am Leben = 5.5.2200, Unbekannt = 12.12.2200, Ignorieren = 1.1.2200): ')

        self.npw = AutocompleteCombobox(self.npwFrame, completevalues=["Ja", "Nein"])
        self.npw.grid(row=0, column=1)

