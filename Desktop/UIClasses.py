#
# Lerchbacher Buecherdatenbank Desktop Client
# Copyright 2025 Lars Lerchbacher
#
from tkinter import *
from tkinter.ttk import *
from handle_db import *
from PIL import Image, ImageTk
import requests
from pathlib import Path


IMAGE_SIZE = 175


class BookWidget(Frame):
    def __init__(self, parent, id: int, *args, **kwargs):
        super().__init__(parent, relief=SUNKEN, width = 600, height = 350, *args, **kwargs)
        self.title = Label(self, text = "", font="Arial 16 bold")
        self.author = Label(self, text = "", font = "Arial 12")

        image = Image.open("../Web/static/noCover.png")

        w, h = image.size
        if h != IMAGE_SIZE:
            ratio = IMAGE_SIZE / h
            new_size = (int(w * ratio), IMAGE_SIZE)
            image = image.resize(new_size, Image.BILINEAR)

        self.image_data = ImageTk.PhotoImage(image)

        self.image = Label(self, image = self.image_data)
        
        self.button = Button(self, text='Weiterlesen...', command=self.update)

        self.id = id

        self.title.pack(pady = 10, padx = 50)
        self.author.pack(pady = 10, padx = 50)
        self.image.pack(pady = 10, padx = 50)
        self.button.pack(pady = 10, padx = 50)

        self.pack_propagate(0)

        self.update()

    
    def update(self):
        book = fetch_book_by_id(self.id)
        self.title.config(text = book.title)
        authors = [fetch_author_by_id(id) for id in book.author_ids] 
        self.author.config(text = "")
        if len(authors) > 1:
            while len(authors) > 2:
                self.author.config(text = self.author["text"] + authors.pop().name)
                self.author.config(text = self.author["text"] + ", ")
            self.author.config(text = self.author["text"] + authors.pop().name)
            self.author.config(text = self.author["text"] + " und ")
        self.author.config(text = self.author["text"] + authors.pop().name)

        cover = fetch_covers([book])[0]
        if not cover == "/static/noCover.png":
            filename = f"./cache/images/{book.id}.jpg"
            filePath = Path(filename)
            if not filePath.is_file():
                response = requests.get(cover)
                file = open(filename, mode = "wb+")
                file.write(response.content)
                file.close()

        else:
            filename = "./static/noCover.png" 

        image = Image.open(filename)

        w, h = image.size
        if h != IMAGE_SIZE:
            ratio = IMAGE_SIZE / h
            new_size = (int(w * ratio), IMAGE_SIZE)
            image = image.resize(new_size, Image.BILINEAR)

        self.image_data = ImageTk.PhotoImage(image)
        self.image.config(image = self.image_data)


class RecentBooksWidget(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_books = fetch_books()
        self.books = all_books[-12:]

        self.header = Label(self, text = "Neueste Buecher", font = "Arial 14 bold")
        self.bookWidgets = []

        self.header.pack()
            
        self.update()

    def update(self):
        self.books = fetch_books()[-12:]
        
        for bookWidget in self.bookWidgets:
            bookWidget.destroy()

        for book in self.books:
            self.bookWidgets.append(BookWidget(self, book.id))

        for bookWidget in self.bookWidgets:
            bookWidget.pack(pady = 20)


class AllBooksWidget(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.books = fetch_books()

        self.bookWidgets = []
            
        self.update()

    def update(self):
        self.books = fetch_books()
        
        for bookWidget in self.bookWidgets:
            bookWidget.destroy()

        for book in self.books:
            self.bookWidgets.append(BookWidget(self, book.id))

        for bookWidget in self.bookWidgets:
            bookWidget.pack(pady = 20)

