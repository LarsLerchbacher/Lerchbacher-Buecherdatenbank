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


from database import fetch_author, fetch_author_by_name, fetch_authors, search_authors 
from customtkinter import *
from CTkListbox import CTkListbox
from tkinter import StringVar 


class AuthorSelectWidget(CTkFrame):
    def __init__(self, parent, used: list):
        super().__init__(parent, fg_color="transparent")

        self.columnconfigure(index=0)
        self.columnconfigure(index=1)
        self.columnconfigure(index=2)
        self.rowconfigure(index=0)
        self.rowconfigure(index=1)

        self.searchVar = StringVar(self)
        self.searchVar.trace_add("write", self.search)

        self.searchCTkLabel = CTkLabel(self, text="Suche nach: ")
        self.searchCTkLabel.grid(row=0, column=0)
    
        self.searchBox = CTkEntry(self, textvariable=self.searchVar)
        self.searchBox.grid(row=0, column=2)

        self.available_list = CTkListbox(self, multiple_selection=True)
        self.used_list = CTkListbox(self, multiple_selection=True)

        self.available_list.grid(row=1, column=0)
        self.used_list.grid(row=1, column=3)

        self.button_frame = CTkFrame(self)
        self.button_frame.grid(row=1, column=2)

        self.select = CTkButton(self.button_frame, text='>', command=self.select)
        self.deselect = CTkButton(self.button_frame, text='<', command=self.deselect)
        self.select_all = CTkButton(self.button_frame, text='>>', command=self.select_all)
        self.deselect_all = CTkButton(self.button_frame, text='<<', command=self.deselect_all)

        self.select.pack(padx=10, pady=5)
        self.deselect.pack(padx=10, pady=5)
        self.select_all.pack(padx=10, pady=5)
        self.deselect_all.pack(padx=10, pady=5)

        self.init_used = used
        self.set(self.init_used)

    def select(self):
        selected = self.available_list.curselection()
        already_moved = 0
        for author in selected:
            author_object = fetch_author_by_name(self.available_list.get(author - already_moved))
            self.used_list.insert(author_object.id, author_object.getName())
            self.available_list.delete(author - already_moved)
            already_moved += 1

    def deselect(self):
        selected = self.used_list.curselection()
        already_moved = 0
        for author in selected:
            author_object = fetch_author_by_name(self.available_list(author - already_moved))
            self.available_list.insert(author_object.id, author_object.getName())
            self.used_list.delete(author - already_moved)
            already_moved += 1

    def select_all(self):
        selected = self.available_list.get("all")
        for author in selected:
            author_object = fetch_author_by_name(author)
            self.used_list.insert(author_object.id, author_object.getName())
        self.available_list.delete("all")

    def deselect_all(self):
        selected = self.used_list.get("all")
        for author in selected:
            author_object = fetch_author_by_name(author)
            self.available_list.insert(author_object.id, author_object.getName())
        self.used_list.delete("all")

    def get(self) -> list[int]:
        names = self.used_list.get("all")
        ids = []
        for name in names:
            author = fetch_author_by_name(name)
            if author:
                ids.append(author.id)
            else:
                ids.append(-1)

        return ids

    def set(self, used: list) -> None:
        self.authors = fetch_authors()
        self.used_list.delete("all")
        self.available_list.delete("all")

        for author in self.authors:
            if author.id in used:
                self.used_list.insert(author.id, author.getName())
            else:
                self.available_list.insert(author.id, author.getName())

    def search(self, *args):
        self.available_list.delete("end")
        self.authors = search_authors(self.searchVar.get())

        for author in self.authors:
            self.available_list.insert(END, author.getName())
