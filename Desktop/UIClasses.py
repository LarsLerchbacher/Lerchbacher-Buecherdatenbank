#
# Lerchbacher Buecherdatenbank Desktop Client
# Copyright 2025 Lars Lerchbacher
#
from tkinter import *
from tkinter.ttk import *


class BookDisplay(Frame):
    def __init__(self, parent, title: str, image: str, id: int):
        super().__init__(parent, relief=SUNKEN)
        self.title = Label(self, text = title, font="Arial 16 bold")

        self.image_data = PhotoImage(file=image)
        self.image = Label(self, image=self.image_data)

        self.button = Button(self, text='Weiterlesen...')

        self.id = id

        self.title.pack(pady = 10, padx = 200)
        self.image.pack(pady = 10, padx = 200)
        self.button.pack(pady = 10, padx = 200)

    
    def update():
        book = fetch_book_by_id(self.id)
        self.title.text = book.title
        self.image_url = get_book_cover(book.isbn)


