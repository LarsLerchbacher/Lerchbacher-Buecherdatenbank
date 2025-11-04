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


from tkinter import Checkbutton, Entry, Frame, IntVar, Label
from UI.DateWidget import DateWidget


class AuthorEditWidget(Frame):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.nameFrame = Frame(self)
        self.nameFrame.pack(padx=20, pady=20)

        self.name = Entry(self.nameFrame, width=75)
        self.nameLabel = Label(self.nameFrame, text='Name: ')
        self.nameLabel.grid(row=0, column=0)
        self.name.grid(row=0, column=1)

        self.countryFrame = Frame(self)
        self.countryFrame.pack(padx=20, pady=20)

        self.country = Entry(self.countryFrame, width=75)
        self.countryLabel = Label(self.countryFrame, text='Land: ')
        self.countryLabel.grid(row=0, column=0)
        self.country.grid(row=0, column=1)

        # DOB = date of birth
        self.dobFrame = Frame(self)
        self.dobFrame.pack(padx=20, pady=20)

        self.dob = DateWidget(self.dobFrame)
        self.dobLabel = Label(self.dobFrame, text='Geburtsdatum (Unbekannt = 12.12.2200): ')
        self.dobLabel.grid(row=0, column=0)
        self.dob.grid(row=1, column=0)

        # DOD = date of death
        self.dodFrame = Frame(self)
        self.dodFrame.pack(padx=20, pady=20)

        self.dod = DateWidget(self.dodFrame)
        self.dodLabel = Label(self.dodFrame, text='Sterbedatum (Noch am Leben = 5.5.2200, Unbekannt = 12.12.2200): ')
        self.dodLabel.grid(row=0, column=0)
        self.dod.grid(row=1, column=0)

        # NPW = Nobel prize winner
        self.npwFrame = Frame(self)
        self.npwFrame.pack(padx=20, pady=20)

        self.npwVar = IntVar(self.npwFrame)
        self.npw = Checkbutton(self.npwFrame, var=self.npwVar)
        self.npwLabel = Label(self.npwFrame, text='Ist ein Nobelpreistraeger?: ')
        self.npwLabel.grid(row=0, column=0)
        self.npw.grid(row=0, column=1)

