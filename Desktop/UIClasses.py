#
# Lerchbacher Buecherdatenbank Desktop Client
# Copyright 2025 Lars Lerchbacher
#


from array import array
from tkinter import *
from tkinter.ttk import *
from handle_db import *
from PIL import Image, ImageTk
import requests
from pathlib import Path
from helperfunctions import *


IMAGE_SIZE = 175


class BookWidget(Frame):
    def __init__(self, parent, id: int, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.preview = Frame(self, relief = SUNKEN)
        self.details = Frame(self.preview)
        self.preview.pack()

        self.title = Label(self.preview, text = "", font="Arial 16 bold", wraplength=500, justify='center')
        self.author = Label(self.preview, text = "", font = "Arial 12")

        image = Image.open("../Web/static/noCover.png")

        w, h = image.size
        if h != IMAGE_SIZE:
            ratio = IMAGE_SIZE / h
            new_size = (int(w * ratio), IMAGE_SIZE)
            image = image.resize(new_size, Image.BILINEAR)

        self.image_data = ImageTk.PhotoImage(image)

        self.image = Label(self.details, image = self.image_data)

        self.id = id

        self.publisher = Label(self.details, text = 'Verlag: ')
        self.publisher.pack(pady = 5, padx = 50)

        self.isbn = Label(self.details, text = 'ISBN: ')
        self.isbn.pack(pady = 5, padx = 50)

        self.edition = Label(self.details, text = 'Auflage Nr.:')
        self.edition.pack(pady = 5, padx = 50)        

        self.year = Label(self.details, text = 'Jahr: ')
        self.year.pack(pady = 5, padx = 50)

        self.type = Label(self.details, text = 'Buchtyp: ')
        self.type.pack(pady = 5, padx = 50)

        self.tags = Label(self.details, text = 'Kategorie(n): ')
        self.tags.pack(pady = 5, padx = 50)

        self.room = Label(self.details, text = 'Raum: ')
        self.room.pack(pady = 5, padx = 50)

        self.shelf = Label(self.details, text = 'Regal: ')
        self.shelf.pack(pady = 5, padx = 50)

        self.lend = Label(self.details, text = 'Verliehen?: ')
        self.lend.pack(pady = 5, padx = 50)

        self.button_frame = Frame(self.preview)
        
        self.button = Button(self.button_frame, text='Mehr anzeigen', command = self.expand)
        self.edit = Button(self.button_frame, text = 'Bearbeiten', command = lambda: open_book_edit(self.id))

        self.title.pack(pady = 10, padx = 50)
        self.author.pack(pady = 10, padx = 50)
        self.image.pack(pady = 10, padx = 50)
        self.button_frame.pack(pady = 10, padx = 250)
        self.button.grid(padx = 10, row = 0, column = 0)

        self.update()

    def update(self):
        book = fetch_book_by_id(self.id)
        self.title.config(text=book.title)
        authors = [fetch_author_by_id(id) for id in book.author_ids] 
        self.author.config(text="")
        if len(authors) > 1:
            while len(authors) > 2:
                self.author.config(text = self.author["text"] + authors.pop().name)
                self.author.config(text = self.author["text"] + ", ")
            self.author.config(text = self.author["text"] + authors.pop().name)
            self.author.config(text = self.author["text"] + " und ")
        self.author.config(text = self.author["text"] + authors.pop().name)

        image = get_cover(book)

        self.image_data = ImageTk.PhotoImage(image)
        self.image.config(image = self.image_data)

        self.publisher.config(text = f'Verlag: {book.publisher}')

        self.isbn.config(text = 'ISBN: {}')
        isbn_value = str(book.isbn)
        self.isbn.config(text = f"ISBN: {isbn_value[0:3]}-{isbn_value[3]}-{isbn_value[4:7]}-{isbn_value[7:12]}-{isbn_value[12]}")

        self.edition.config(text = f'Auflage: {book.edition}')

        self.year.config(text = f'Jahr: {book.year}')

        all_types = read_book_types()
        self.type.config(text = f'Buchtyp: {all_types[book.type] if book.type in range(0, len(all_types)) else "Unbekannt"}')

        tag_string = ""
        tag_loop = book.tags
        while len(tag_loop) > 1:
            tag_string += f" {tag_loop.pop()};"
        tag_string += f" {tag_loop.pop()}"
        self.tags.config(text = f'Kategorie(n): {tag_string}')

        all_rooms = read_rooms()
        self.room.config(text = f'Raum: {all_rooms[book.room] if book.room in range(0, len(all_rooms)) else "Unbekannt"}')

        self.shelf.config(text = f'Regal: {book.shelf}')

        self.lend.config(text = f'Verliehen?: {"Ja" if book.lend else "Nein"}')
    

    def expand(self):

        # Code to expand to details
        self.button_frame.pack_forget()
        self.details.pack()
        self.button.configure(text = 'Weniger anzeigen', command = self.shrink)
        self.edit.grid(row = 0, column = 1)
        self.button_frame.pack(pady = 10, padx = 250)


    def shrink(self):

        # Code to shrink to overview
        self.button_frame.pack_forget()
        self.details.pack_forget()
        self.button.configure(text = 'Mehr anzeigen', command = self.expand)
        self.edit.grid_forget()
        self.button_frame.pack(pady = 10, padx = 250)


class RecentBooksWidget(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_books = fetch_books()
        self.books = all_books[-12:]

        self.header = Label(self, text="Neueste Buecher", font="Arial 14 bold")
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
            bookWidget.pack(pady=20)


class ISBNWidget(Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<KeyRelease>", self.format)

    def format(self, event):
        position = self.index(INSERT)
        if position in [3, 5, 8, 15] and not event.keysym in ["BackSpace", "Left", "Right"]:
            # Insert dash
            self.insert(INSERT, '-')

            # Move cursor
            self.icursor(position + 1)

        elif position > 13 or len(self.get()) > 17:
            # Limit input length
            self.delete(17, END)

    def get(self):
        text = super().get()
        text = text.replace('-', '')
        return text


class BookEdit(Toplevel):
    def __init__(self, id):
        super().__init__()
        if id != None:
            self.id = id
        else:
            self.id = -1

        self.title_frame = Frame(self)
        self.title_frame.pack(padx=20, pady=20)

        self.title_label = Label(self.title_frame, text="Titel: ")
        self.title = Entry(self.title_frame, width=75)
        self.title_label.grid(row=0, column=0)
        self.title.grid(row=0, column=1, columnspan=4)

        self.authors_frame = Frame(self)
        self.authors_frame.pack(padx=20, pady=5)

        self.authors_label = Label(self.authors_frame, text="Autoren: ")
        self.authors = AuthorSelectWidget(self.authors_frame, [])
        self.authors_label.grid(row=0, column=0)
        self.authors.grid(row=1, column=0, pady=20)

        self.publisher_frame = Frame(self)
        self.publisher_frame.pack(padx=20, pady=5)

        self.publisher_label = Label(self.publisher_frame, text="Verlag: ")
        self.publisher = Entry(self.publisher_frame, width=50)
        self.publisher_label.grid(row=0, column=0)
        self.publisher.grid(row=0, column=1, columnspan=3)

        self.isbn_frame = Frame(self)
        self.isbn_frame.pack(padx=20, pady=5)

        self.isbn_label = Label(self.isbn_frame, text="  ISBN: ")
        self.isbn = ISBNWidget(self.isbn_frame, width=50)
        self.isbn_label.grid(row=0, column=0)
        self.isbn.grid(row=0, column=1, columnspan=3)

        self.edition_frame = Frame(self)
        self.edition_frame.pack(padx=20, pady=5)

        self.edition_label = Label(self.edition_frame, text='Auflage: ')
        self.edition = Spinbox(self.edition_frame, increment=1, from_=1, to=20, wrap=True, width=25)
        self.edition_label.grid(row=0, column=0)
        self.edition.grid(row=0, column=1)

        self.year_frame = Frame(self)
        self.year_frame.pack(padx=20, pady=5)

        self.year_label = Label(self.year_frame, text="Jahr: ")
        self.year = Spinbox(self.year_frame, increment=1, from_=1800, to=2099, wrap=True, width=25)
        self.year_label.grid(row=0, column=0)
        self.year.grid(row=0, column=1)

        self.type_frame = Frame(self)
        self.type_frame.pack(padx=20, pady=5)

        self.all_types = read_book_types()
        self.type_label = Label(self.type_frame, text="Typ: ")
        self.type = Combobox(self.type_frame, values=self.all_types, state="readonly", width=25)
        self.type_label.grid(row=0, column=0)
        self.type.grid(row=0, column=1)

        self.tags_frame = Frame(self)
        self.tags_frame.pack(padx=20, pady=5)

        self.tags_label = Label(self.tags_frame, text="Kategorien (durch ';' getrennt): ")
        self.tags = Entry(self.tags_frame, width=50)
        self.tags_label.grid(row=0, column=0)
        self.tags.grid(row=0, column=1)

        self.room_frame = Frame(self)
        self.room_frame.pack(padx=20, pady=5)

        self.all_rooms = read_rooms()
        self.room_label = Label(self.room_frame, text='Raum: ')
        self.room = Combobox(self.room_frame, values=self.all_rooms, width=25)
        self.room_label.grid(row=0, column=0)
        self.room.grid(row=0, column=1)

        self.shelf_frame = Frame(self)
        self.shelf_frame.pack(padx=20, pady=5)
        
        self.shelf_label = Label(self.shelf_frame, text='Regal: ')
        self.shelf = Entry(self.shelf_frame, width=25)
        self.shelf_label.grid(row=0, column=0)
        self.shelf.grid(row=0, column=1)

        self.lend_frame = Frame(self)
        self.lend_frame.pack(padx=20, pady=5)

        self.lend_label = Label(self.lend_frame, text='Ausgeborgt: ')
        self.lend_var = IntVar()
        self.lend = Checkbutton(self.lend_frame, variable=self.lend_var)
        self.lend_label.grid(row=0, column=0)
        self.lend.grid(row=0, column=1)

        self.button_frame = Frame(self)
        self.button_frame.pack(padx=20, pady=5)

        self.save_button = Button(self.button_frame, text='Speichern', command=self.save)
        self.cancel_button = Button(self.button_frame, text='Abbrechen', command=self.cancel)
        self.save_button.grid(row=0, column=0)
        self.cancel_button.grid(row=0, column=1, padx=10)

        if self.id != -1:
            self.update()

    def update(self):
        book = fetch_book_by_id(self.id)

        self.title.delete(0, END)
        self.title.insert(0, book.title)

        self.authors.set(book.author_ids)

        self.publisher.delete(0, END)
        self.publisher.insert(0, book.publisher)

        self.isbn.delete(0, END)
        isbn_value = str(book.isbn)
        self.isbn.insert(0, f"{isbn_value[0:3]}-{isbn_value[3]}-{isbn_value[4:7]}-{isbn_value[7:12]}-{isbn_value[12]}")

        self.edition.set(book.edition)

        self.year.set(book.year)

        self.all_types = read_book_types()
        if self.all_types == []:
            set_book_types(["Kinderbuch", "Jugendbuch", "Roman", "Sachbuch"])
        self.type['values'] = self.all_types

        if book.type in range(0, len(self.all_types)):
            self.type.set(self.all_types[book.type])
        else:
            self.type.set("Unbekannt")

        if book.room in range(0, len(self.all_rooms)):
            self.room.set(self.all_rooms[book.room])
        else:
            self.room.set("Unbekannt")

        self.tags.delete(0, END)
        self.tags.insert(0, "; ".join(book.tags))

        self.shelf.delete(0, END)
        self.shelf.insert(0, book.shelf)

        if book.lend == 0:
            self.lend_var.set(0)
        else:
            self.lend_var.set(1)

    def save(self):
        # Code to save changes / create new book
        pass

    def cancel(self):
        self.destroy()


class AuthorSelectWidget(Frame):
    def __init__(self, parent, used: list):
        super().__init__(parent)
        self.init_used = used
        self.set(self.init_used)

        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)
        self.columnconfigure(index=2, weight=1)
        self.rowconfigure(index=0, weight=1)

        self.available_var = Variable(self, value=self.available)
        self.available_list = Listbox(self, listvariable=self.available_var, selectmode=MULTIPLE)
        self.av_scrollbar = Scrollbar(self, orient="vertical", command=self.available_list.yview)

        self.used_var = Variable(self, value=self.used)
        self.used_list = Listbox(self, listvariable=self.used_var, selectmode=MULTIPLE)
        self.used_scrollbar = Scrollbar(self, orient="vertical", command=self.used_list.yview)

        self.available_list.grid(row=0, column=0)
        self.av_scrollbar.grid(row=0, column=1)
        self.used_list.grid(row=0, column=3)
        self.used_scrollbar.grid(row=0, column=4)

        self.button_frame = Frame(self)
        self.button_frame.grid(row=0, column=2)

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
            author = fetch_author_by_id(author_id)
            if author.name in self.available:
                self.available.remove(author.name)
                self.available_list.delete(self.available_list.get(0, END).index(author.name))
                self.used.append(author.name)
                self.used_list.insert(author.id, author.name)

            else:
                self.used.append("Unbekannt")


class Tab(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scrollbar = Scrollbar(self, orient="vertical")

        self.canvas = Canvas(self, yscrollcommand=self.scrollbar.set)
        self.inner_frame = Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind(
                "<Configure>",
                lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.bind(
                "<Configure>",
                lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width)
        )

        self.scrollbar.config(command=self.canvas.yview)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Scrolling code, needs to be in children of Tab
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)  # Windows and Mac
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))  # Linux scroll up
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))  # Linux scroll down

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class MainTab(Tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header_label = Label(self.inner_frame, text='Lerchbacher Bücherdatenbank', font="Arial 25 bold")
        self.header_label.pack(padx=0, pady=10)

        self.recentBooks = RecentBooksWidget(self.inner_frame)
        self.recentBooks.pack(padx=0, pady=10)


class BooksTab(Tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header_label = Label(self.inner_frame, text='Bücher', font="Arial 25 bold")
        self.header_label.pack(padx=0, pady=10)

        self.books = AllBooksWidget(self.inner_frame)
        self.books.pack()


class AuthorsTab(Tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SearchTab(Tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SettingsTab(Tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def open_book_edit(id):
    BookEdit(id)


class App(Tk):
    def __init__(self):
        super().__init__()
        log("Initializing main window")
        self.title("Lerchbacher Bücherdatenbank")

        log("Creating tab control widget")
        self.tabControl = Notebook(self)
        self.tabControl.pack(fill="both", expand=True)

        log("Populating tab control widget")
        self.mainTab = MainTab(self.tabControl)
        self.booksTab = BooksTab(self.tabControl)
        self.authorsTab = AuthorsTab(self.tabControl)
        self.searchTab = SearchTab(self.tabControl)
        self.settingsTab = SettingsTab(self.tabControl)

        self.tabControl.add(self.mainTab, text='Hauptmenü')
        self.tabControl.add(self.booksTab, text='Bücher')
        self.tabControl.add(self.authorsTab, text='Autoren')
        self.tabControl.add(self.searchTab, text='Suche')
        self.tabControl.add(self.searchTab, text='Einstellungen')

        log("Successfully initialized main window")


