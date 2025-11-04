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
from database import delete_author, fetch_author
from datetime import date
from tkinter import *
from tkinter import messagebox
from UI.Author.AuthorEditToplevel import AuthorEditToplevel


class AuthorWidget(Frame):
    def __init__(self, parent, id, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.id = id

        self.preview = Frame(self, relief=SUNKEN, bd=1)
        self.details = Frame(self.preview)
        self.preview.pack()

        self.name = Label(self.preview, font='Arial 16 bold', wraplength=500, justify='center')
        self.name.pack(padx=50, pady=10)

        self.country = Label(self.details, text='Aus: ')
        self.country.pack(pady=5, padx=50)

        self.nobel = Label(self.details)
        self.nobel.pack(pady=5, padx=50)

        self.dob = Label(self.details, text='Geburtsdatum: ')
        self.dob.pack(pady=5, padx=50)

        self.dod = Label(self.details, text='Sterbedatum: ')
        self.dod.pack(pady=5, padx=50)

        self.button_frame = Frame(self.preview)
        self.button_frame.pack(pady=10, padx=250)

        self.toggle = Button(self.button_frame, text='Mehr anzeigen', command=self.expand)
        self.toggle.grid(row=0, column=0, padx=10)

        self.edit = Button(self.button_frame, text='Bearbeiten', command=lambda:AuthorEditToplevel(self.id))

        self.delete = Button(self.button_frame, text='Löschen', command=self.delete)


        if self.id != -1:
            self.update()

    
    def update(self):

        author = fetch_author(self.id)

        self.name.config(text=author.name)

        self.country.config(text=author.country)

        if author.has_nobel_prize == 1:
            nobel_text = "Ist ein Nobelpreistraeger"
        else:
            nobel_text = "Ist kein Nobelpreistraeger"

        self.nobel.config(text=nobel_text)

        if author.birthdate != date(2200, 12, 12):
            birthdate_str = str(author.birthdate)[8:11] + "." + str(author.birthdate)[5:7] + "." + str(author.birthdate)[0:4]

            self.dob.config(text=f'Geboren am {birthdate_str}')

        else:
            self.dob.config(text=f"Geburtsdatum unbekannt")

        if author.date_of_death not in [date(2200, 5, 5), date(2200, 12, 12)]:
            date_of_death_str = str(author.date_of_death)[8:11] + "." + str(author.date_of_death)[5:7] + "." + str(author.date_of_death)[0:4] 
            self.dod.config(text=f'Gestorben am {date_of_death_str}')
        elif author.date_of_death == date(2200, 5, 5):
            self.dod.config(text='Ist noch am Leben')
        else:
            self.dod.config(text="Sterbedatum unbekannt")



    def expand(self):
        self.button_frame.pack_forget()
        self.details.pack()
        self.toggle.config(text='Weniger anzeigen', command=self.shrink)
        self.edit.grid(row=0, column=1)
        self.delete.grid(row=0, column=2, padx=10)
        self.button_frame.pack(pady=10, padx=250)


    def shrink(self):
        self.button_frame.pack_forget()
        self.details.pack_forget()
        self.toggle.config(text='Mehr anzeigen', command=self.expand)
        self.edit.grid_forget()
        self.delete.grid_forget()
        self.button_frame.pack(pady=10, padx=250)


    def delete(self):
        author = fetch_author(self.id)
        decision = messagebox.askquestion("Bestaetigen", f"Möchten Sie den Autor {author.name} wirklich löschen?\n Diese Aktion kann NICHT rueckgaengig gemacht werden!")
        if decision == "yes":
            app_context.logger.info(f"Deleting author with id {self.id}...")
            delete_author(self.id)
            app_context.mainWindow.update()

