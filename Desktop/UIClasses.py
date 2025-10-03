#
# Desktop/UIClasses.py
# ----------
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


from array import array
from app import get_image, get_image_src, update_image
import app_context
from database import *
from datetime import date
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter.messagebox import *
from PIL import Image, ImageTk
import requests


IMAGE_SIZE = 175

global logger, formatter


class BookWidget(Frame):
    def __init__(self, parent, id: int, *args, **kwargs):
        global logger
        super().__init__(parent, *args, **kwargs)

        self.id = id

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

        self.lend = Label(self.details, text = 'Verliehen: ')
        self.lend.pack(pady = 5, padx = 50)

        self.button_frame = Frame(self.preview)
        
        self.button = Button(self.button_frame, text='Mehr anzeigen', command = self.expand)
        self.edit = Button(self.button_frame, text = 'Bearbeiten', command = self.open_edit)
        self.delete = Button(self.button_frame, text = 'Loeschen', command = self.delete_book)

        self.title.pack(pady = 10, padx = 50)
        self.author.pack(pady = 10, padx = 50)
        self.image.pack(pady = 10, padx = 50)
        self.button_frame.pack(pady = 10, padx = 250)
        self.button.grid(padx = 10, row = 0, column = 0)


        self.update()


    def open_edit(self):
        edit = BookEdit(self.id)


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

        image = get_image(book)

        self.image_data = ImageTk.PhotoImage(image)
        self.image.config(image = self.image_data)

        self.publisher.config(text = f'Verlag: {book.publisher}')

        self.isbn.config(text = 'ISBN: {}')
        isbn_value = str(book.isbn)
        self.isbn.config(text = f"ISBN: {isbn_value[0:3]}-{isbn_value[3]}-{isbn_value[4:7]}-{isbn_value[7:12]}-{isbn_value[12]}")

        self.edition.config(text = f'Auflage: {book.edition}')

        self.year.config(text = f'Jahr: {book.year}')

        all_types = get_book_types()
        self.type.config(text = f'Buchtyp: {all_types[book.type] if book.type in range(0, len(all_types)) else "Unbekannt"}')

        tag_string = ""
        tag_loop = book.tags
        while len(tag_loop) > 1:
            tag_string += f" {tag_loop.pop()};"
        tag_string += f" {tag_loop.pop()}"
        self.tags.config(text = f'Kategorie(n): {tag_string}')

        all_rooms = get_rooms()
        self.room.config(text = f'Raum: {all_rooms[book.room] if book.room in range(0, len(all_rooms)) else "Unbekannt"}')

        self.shelf.config(text = f'Regal: {book.shelf}')

        self.lend.config(text = f'Verliehen: {"Ja" if book.lend else "Nein"}')

    

    def expand(self):
        self.button_frame.pack_forget()
        self.details.pack()
        self.button.configure(text = 'Weniger anzeigen', command = self.shrink)
        self.edit.grid(row = 0, column = 1)
        self.delete.grid(row = 0, column = 2, padx = 10)
        self.button_frame.pack(pady = 10, padx = 250)


    def shrink(self):
        self.button_frame.pack_forget()
        self.details.pack_forget()
        self.button.configure(text = 'Mehr anzeigen', command = self.expand)
        self.edit.grid_forget()
        self.delete.grid_forget()
        self.button_frame.pack(pady = 10, padx = 250)


    def delete_book(self):
        book = fetch_book_by_id(self.id)
        decision = messagebox.askquestion("Bestaetigen", f"Moechten Sie das Buch {book.title} wirklich loeschen?\n Diese Aktion kann NICHT rueckgaengig gemacht werde!")
        if decision == "yes":
            logger.info(f"Deleting book with id {self.id}...")
            delete_book(self.id, SECURITY_KEY)
            app_context.mainWindow.update()
        
        


class RecentBooksWidget(Frame):
    def __init__(self, *args, **kwargs):
        global logger, formatter
        super().__init__(*args, **kwargs)
        logger.info("Creating 'recent books widget'")
        all_books = fetch_books()
        self.books = all_books[-12:]

        self.header = Label(self, text="Neueste Buecher", font="Arial 14 bold")
        self.bookWidgets = []

        self.header.pack()

        self.update()

    def update(self):
        logger.info("Updating 'recent books widget'")
        all_books = fetch_books()
        self.books = all_books[-12:]
        
        for bookWidget in self.bookWidgets:
            for child in bookWidget.winfo_children():
                child.destroy()
            bookWidget.destroy()

        self.bookWidgets = []

        for book in self.books:
            self.bookWidgets.append(BookWidget(self, book.id))

        for bookWidget in self.bookWidgets:
            bookWidget.pack(pady = 20)



class AllBooksWidget(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("Creating 'all books widget'")
        self.books = fetch_books()

        self.bookWidgets = []

        
        self.update()

    def update(self):
        logger.info("Updating 'all books widget'")
        self.books = fetch_books()
        
        for bookWidget in self.bookWidgets:
            for child in bookWidget.winfo_children():
                child.destroy()
            bookWidget.destroy()
        
        self.bookWidgets = []

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
        self.id = id
        if self.id != -1:
            logger.info(f"Opening book editing dialog for book with id {self.id}")
        else:
            logger.info("Opening empty book editing dialog")

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

        self.lend_label = Label(self.lend_frame, text='Verliehen : ')
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
        logger.info("Saving book: ")

        title = self.title.get()
        logger.info(f"\tTitle: {title}")

        author_ids = self.authors.get()
        authors = []
        all_authors = fetch_authors()
        for author in fetch_authors():
            if author.id in author_ids:
                authors.append(author.name)
        logger.info(f"\tAutoren: {authors} (Ids: {author_ids})")

        publisher = self.publisher.get()
        logger.info(f"\tVerlag: {publisher}")

        isbn = self.isbn.get()
        isbn_value = str(isbn)
        logger.info(f"\tISBN: {isbn_value[0:3]}-{isbn_value[3]}-{isbn_value[4:7]}-{isbn_value[7:12]}-{isbn_value[12]}")

        edition = self.edition.get()
        logger.info(f"\tAuflage: {edition}")

        year = self.year.get()
        logger.info(f"\tJahr: {year}")

        book_type = self.type.get()
        type_nr = self.all_types.index(book_type)
        logger.info(f"\tBuchtyp: {book_type} (Typ Nr. {type_nr})")

        tags = self.tags.get().replace("; ", ";").split(";")
        logger.info(f"\tKategorien: {tags}")

        book_room = self.room.get()
        room_nr = self.all_rooms.index(book_room)
        logger.info(f"\tRaum: {book_room} (Raum Nr. {room_nr})")

        shelf = self.shelf.get()
        logger.info(f"\tRegal: {shelf}")

        lend = self.lend_var.get()
        logger.info(f"\tVerliehen: {"ja" if lend else "nein"} (lend_var: {lend})")

        book = Book(id=self.id, title=title, author_ids=author_ids, publisher=publisher, isbn=isbn, edition=edition, year=year, type=type_nr, tags=tags, room=room_nr, shelf=shelf, lend=lend)

        if self.id != -1:
            response = edit_book(self.id, book)
            if response != "OK":
                logger.info(f"Speichern nicht moeglich!\n{response}", "ERROR")
                showerror(title="Speichern nicht moeglich!", message=response)
            else:
                logger.info("Erfolgreich gespeichert!")

                update_image(book)

                app_context.mainWindow.update()
                self.destroy()
        else:
            response = create_book(book)
            if type(response) == str:
                logger.info(f"Speichern nicht moeglich!\n{response}", "ERROR")
                showerror(title="Speichern nicht moeglich!", message=response)
            else:
                self.id = response
                book.id = response
                logger.info("Erfolgreich gespeichert!")

                update_image(book)

                app_context.mainWindow.update()
                self.destroy()


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


class AuthorWidget(Frame):
    def __init__(self, parent, id, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.id = id

        self.preview = Frame(self, relief=SUNKEN)
        self.details = Frame(self.preview)
        self.preview.pack()

        self.name = Label(self.preview, font='Arial 16 bold', wraplength=500, justify='center')
        self.name.pack(padx=50, pady=10)

        self.country = Label(self.details, text='From: ')
        self.country.pack(pady=5, padx=50)

        self.nobel = Label(self.details)
        self.nobel.pack(pady=5, padx=50)

        self.dob = Label(self.details, text='Born on: ')
        self.dob.pack(pady=5, padx=50)

        self.dod = Label(self.details, text='Died on: ')
        self.dod.pack(pady=5, padx=50)

        self.button_frame = Frame(self.preview)
        self.button_frame.pack(pady=10, padx=250)

        self.toggle = Button(self.button_frame, text='Mehr anzeigen', command=self.expand)
        self.toggle.grid(row=0, column=0, padx=10)

        self.edit = Button(self.button_frame, text='Bearbeiten', command=lambda:AuthorEdit(self.id))

        self.delete = Button(self.button_frame, text='Loeschen', command=self.delete_author)


        if self.id != -1:
            self.update()

    
    def update(self):

        author = fetch_author_by_id(self.id)

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

        if author.date_of_death not in [date(2200, 1, 1), date(2200, 12, 12)]:
            date_of_death_str = str(author.date_of_death)[8:11] + "." + str(author.date_of_death)[5:7] + "." + str(author.date_of_death)[0:4] 
            self.dod.config(text=f'Gestorben am {date_of_death_str}')
        elif author.date_of_death == date(2200, 1, 1):
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


    def delete_author(self):
        author = fetch_author_by_id(self.id)
        decision = messagebox.askquestion("Bestaetigen", f"Moechten Sie den Autor {author.name} wirklich loeschen?\n Diese Aktion kann NICHT rueckgaengig gemacht werde!")
        if decision == "yes":
            logger.info(f"Deleting author with id {self.id}...")
            delete_author(self.id, SECURITY_KEY)
            app_context.mainWindow.update()


class DateWidget(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.day = Spinbox(self, from_=1, to=31, width=10, wrap=True, command=self.update)
        self.month = Spinbox(self, from_=1, to=12, width=10, wrap=True, command=self.update)
        self.year = Spinbox(self, from_=0, to=2200, command=self.update)
        self.firstDot = Label(self, text='.')
        self.secondDot = Label(self, text='.')

        self.day.grid(row=0, column=0)
        self.firstDot.grid(row=0, column=1)
        self.month.grid(row=0, column=2)
        self.secondDot.grid(row=0, column=3)
        self.year.grid(row=0, column=4)

        self.day.set(1)
        self.month.set(1)
        self.year.set(2200)

        self.update()

    def update(self):
        # Get the currently selected values
        year = int(self.year.get())
        month = int(self.month.get())
        day = int(self.day.get())

        # Check if the currently selected year is a leap year
        isLeapYear = False
        if year % 4 == 0:
            isLeapYear = True
        else:
            isLeapYear = False

        
        # Stores the days each month has.
        daysPerMonthList = [31, 'x', 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        # Set the number of days that february has based on the currently selected year
        if isLeapYear:
            daysPerMonthList[1] = 29
        else:
            daysPerMonthList[1] = 28

        # Gets the number of days in the currently selected month (lists are 0-based, months 1-based)
        daysPerMonth = daysPerMonthList[month - 1]

        # If the currently selected day is higher than the number of days in the currently selected month, set it back to 1
        self.day.config(to=daysPerMonth)
        if day > daysPerMonth:
            self.day.set(1)

    def get(self):
        # Get the currently selected values
        year = int(self.year.get())
        month = int(self.month.get())
        day = int(self.day.get())
        
        # Return a date object with these values
        return Date(year, month, day)
    

    def set(self, date: Date):
        self.year.set(date.year)
        self.month.set(date.month)
        self.day.set(date.day)
        self.update()

        
class AuthorEdit(Toplevel):
    def __init__(self, id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        if self.id != -1:
            logger.info(f"Opening author editing dialog for author with id {self.id}")
        else:
            logger.info("Opening empty author editing dialog")

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
        self.dodLabel = Label(self.dodFrame, text='Sterbedatum (Noch am Leben = 1.1.2200, Unbekannt = 12.12.2200): ')
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

        self.buttonFrame = Frame(self)
        self.buttonFrame.pack(padx=20, pady=20)

        self.saveButton = Button(self.buttonFrame, text='Speichern', command=self.save)
        self.cancelButton = Button(self.buttonFrame, text='Abbrechen', command=self.cancel)
        self.saveButton.grid(row=0, column=0)
        self.cancelButton.grid(row=0, column=1, padx=10)



        if self.id != -1:
            self.update()


    def update(self):
        author = fetch_author_by_id(self.id)

        self.name.delete(0, END)
        self.name.insert(0, author.name)

        self.country.delete(0, END)
        self.country.insert(0, author.country)

        self.dob.set(author.birthdate)

        self.dod.set(author.date_of_death)

        self.npwVar.set(author.has_nobel_prize)



    def save(self):
        name = self.name.get()
        country = self.country.get()
        dob = str(self.dob.get())
        dod = str(self.dod.get())
        npw = self.npwVar.get()

        if self.id != -1:
            new_author = Author(id, name, npw, country, dob, dod)
            response = edit_author(self.id, new_author)
            if response != "OK":
                logger.info(f"Speichern nicht moeglich!\n{response}", "ERROR")
                showerror(title="Speichern nicht moeglich!", message=response)
            else:
                logger.info("Erfolgreich gespeichert!")
                app_context.mainWindow.update()
                self.destroy()
        else:
            new_author = Author(-1, name, npw, country, dob, dod)
            response = create_author(new_author)
            if response != "OK":
                logger.info(f"Speichern nicht moeglich!\n{response}", "ERROR")
                showerror(title="Speichern nicht moeglich!", message=response)
            else:
                logger.info("Erfolgreich gespeichert!")
                app_context.mainWindow.update()
                self.destroy()


    def cancel(self):
        if self.id == -1:
            logger.info("Closed empty author editing dialog wihtout saving")
        else:
            logger.info(f"Closed author editing dialog for author with id {self.id} wihtout saving")

        self.destroy()



class AllAuthorsWidget(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("Creating 'all authors widget'")
        self.authors = fetch_authors()

        self.authorWidgets = []

        self.update()


    def update(self):
        logger.info("Updating 'all authors widget'")
        self.authors = fetch_authors()

        for authorWidget in self.authorWidgets:
            for child in authorWidget.winfo_children():
                child.destroy()
            authorWidget.destroy()

        self.authorWidgets = []

        for author in self.authors:
            self.authorWidgets.append(AuthorWidget(self, author.id))

        for authorWidget in self.authorWidgets:
            authorWidget.pack(pady=20)


class RecentAuthorsWidget(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("Creating 'recent authors widget'")
        all_authors = fetch_authors()
        self.authors = all_authors[-12:]

        self.header = Label(self, text="Neueste Autoren", font="Arial 14 bold")
        self.authorWidgets = []

        self.header.pack()

        self.update()

    def update(self):
        logger.info("Updating 'recent authors widget'")
        all_authors = fetch_authors()
        self.authors = all_authors[-12:]
        
        for authorWidget in self.authorWidgets:
            for child in authorWidget.winfo_children():
                child.destroy()
            authorWidget.destroy()

        self.authorWidgets = []

        for author in self.authors:
            self.authorWidgets.append(AuthorWidget(self, author.id))

        for authorWidget in self.authorWidgets:
            authorWidget.pack(pady = 20)


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

        self.recentAuthors = RecentAuthorsWidget(self.inner_frame)
        self.recentAuthors.pack(padx=0, pady=10)

    def update(self):
        self.recentBooks.update()
        self.recentAuthors.update()


class BooksTab(Tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header_label = Label(self.inner_frame, text='Bücher', font="Arial 25 bold")
        self.header_label.pack(padx=0, pady=10)

        self.create_button = Button(self.inner_frame, text='Neues Buch hinzufuegen', command=lambda: BookEdit(-1))
        self.create_button.pack(padx=0, pady=5)

        self.books = AllBooksWidget(self.inner_frame)
        self.books.pack()

    def update(self):
        self.books.update()


class AuthorsTab(Tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header_label = Label(self.inner_frame, text="Autoren", font="Arial 25 bold")
        self.header_label.pack(padx=0, pady=10)

        self.create_button = Button(self.inner_frame, text='Neuen Author hinzufuegen', command=lambda: AuthorEdit(-1))
        self.create_button.pack(padx=0, pady=5)

        self.authors = AllAuthorsWidget(self.inner_frame)
        self.authors.pack(padx=0, pady=5)

    def update(self):
        self.authors.update()


class SearchTab(Tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def update(self):
        pass


class RoomsTab(Tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        pass


class TypesTab(Tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        pass


class App(Tk):
    def __init__(self):
        global logger, formatter

        super().__init__()

        logger = app_context.logger
        formatter = app_context.formatter

        logger.info("Initializing main window")
        self.title("Lerchbacher Bücherdatenbank")

        app_context.mainWindow = self

        logger.info("Creating tab control widget")
        self.tabControl = Notebook(self)
        self.tabControl.pack(fill="both", expand=True)

        logger.info("Populating tab control widget")
        self.mainTab = MainTab(self.tabControl)
        self.booksTab = BooksTab(self.tabControl)
        self.authorsTab = AuthorsTab(self.tabControl)
        self.typesTab = TypesTab(self.tabControl)
        self.roomsTab = RoomsTab(self.tabControl)
        self.searchTab = SearchTab(self.tabControl)

        self.tabControl.add(self.mainTab, text='Hauptmenü')
        self.tabControl.add(self.booksTab, text='Bücher')
        self.tabControl.add(self.authorsTab, text='Autoren')
        self.tabControl.add(self.typesTab, text='Buchtypen')
        self.tabControl.add(self.roomsTab, text='Raeume')
        self.tabControl.add(self.searchTab, text='Suche')

        logger.info("Successfully initialized main window")

    def update(self):

        self.mainTab.update()
        self.booksTab.update()
        self.authorsTab.update()
        self.searchTab.update()
        self.typesTab.update()
        self.roomsTab.update()


