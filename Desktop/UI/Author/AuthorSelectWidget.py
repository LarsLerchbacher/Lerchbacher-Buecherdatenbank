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


from database import fetch_author, fetch_author_by_name, fetch_authors
from tkinter import *


class AuthorSelectWidget(Frame):
    def __init__(self, parent, used: list):
        super().__init__(parent)
        self.init_used = used
        self.set(self.init_used)

        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)
        self.columnconfigure(index=2, weight=1)
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)

        self.searchVar = StringVar(self)
        self.searchVar.trace_add("write", self.search)

        self.searchLabel = Label(self, text="Suche nach: ")
        self.searchLabel.grid(row=0, column=0)
    
        self.searchBox = Entry(self, textvariable=self.searchVar)
        self.searchBox.grid(row=0, column=2)

        self.available_var = Variable(self, value=self.available)
        self.available_list = Listbox(self, listvariable=self.available_var, selectmode=MULTIPLE)
        self.av_scrollbar = Scrollbar(self, orient="vertical", command=self.available_list.yview)

        self.used_var = Variable(self, value=self.used)
        self.used_list = Listbox(self, listvariable=self.used_var, selectmode=MULTIPLE)
        self.used_scrollbar = Scrollbar(self, orient="vertical", command=self.used_list.yview)

        self.available_list.grid(row=1, column=0)
        self.av_scrollbar.grid(row=1, column=1)
        self.used_list.grid(row=1, column=3)
        self.used_scrollbar.grid(row=1, column=4)

        self.button_frame = Frame(self)
        self.button_frame.grid(row=1, column=2)

        self.select = Button(self.button_frame, text='>', command=self.select)
        self.deselect = Button(self.button_frame, text='<', command=self.deselect)
        self.select_all = Button(self.button_frame, text='>>', command=self.select_all)
        self.deselect_all = Button(self.button_frame, text='<<', command=self.deselect_all)

        self.select.pack(padx=10, pady=5)
        self.deselect.pack(padx=10, pady=5)
        self.select_all.pack(padx=10, pady=5)
        self.deselect_all.pack(padx=10, pady=5)

    def select(self):
        selected = self.available_list.curselection()
        already_moved = 0
        for author in selected:
            author_object = fetch_author_by_name(self.available_list.get(author - already_moved))
            self.used_list.insert(author_object.id, author_object.name)
            self.available_list.delete(author - already_moved)
            already_moved += 1

    def deselect(self):
        selected = self.used_list.curselection()
        already_moved = 0
        for author in selected:
            author_object = fetch_author_by_name(self.used_list.get(author - already_moved))
            self.available_list.insert(author_object.id, author_object.name)
            self.used_list.delete(author - already_moved)
            already_moved += 1

    def select_all(self):
        selected = self.available_list.get(0, END)
        for author in selected:
            author_object = fetch_author_by_name(author)
            self.used_list.insert(author_object.id, author_object.name)
        self.available_list.delete(0, END)

    def deselect_all(self):
        selected = self.used_list.get(0, END)
        for author in selected:
            author_object = fetch_author_by_name(author)
            self.available_list.insert(author_object.id, author_object.name)
        self.used_list.delete(0, END)

    def get(self) -> list[int]:
        names = self.used_list.get(0, END)
        ids = []
        for name in names:
            author = fetch_author_by_name(name)
            if author:
                ids.append(author.id)
            else:
                ids.append(-1)

        return ids

    def set(self, init_used: list) -> None:
        self.used = []
        self.authors = fetch_authors()
        self.available = []

        for author in self.authors:
            self.available.append(author.name)

        for author_id in init_used:
            author = fetch_author(author_id)
            if author.name in self.available:
                self.available.remove(author.name)
                self.available_list.delete(self.available_list.get(0, END).index(author.name))
                self.used.append(author.name)
                self.used_list.insert(author.id, author.name)

            else:
                self.used.append("Unbekannt")

    def search(self, *args):
        self.available_list.delete(0, END)
        self.authors = fetch_authors()

        for author in self.authors:
            if self.searchVar.get() in author.name:
                self.available_list.insert(END, author.name)

