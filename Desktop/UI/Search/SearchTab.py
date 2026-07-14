#
#   The Lerchbacher book database project
#   © Lars Lerchbacher 2025-2026
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
import csv
from database import fetch_author, fetch_author_ids, fetch_authors, \
    fetch_book, fetch_book_ids, fetch_books, \
    fetch_book_type, fetch_book_type_id, fetch_book_types, fetch_book_type_ids, \
    fetch_room, fetch_rooms, fetch_room_id, fetch_room_ids, \
    prepare_db
from datetime import date
from customtkinter import *
from tkinter.filedialog import asksaveasfilename
from UI.Author.AuthorWidget import AuthorWidget
from UI.Book.BookWidget import BookWidget
from UI.BookType.TypeWidget import TypeWidget
from UI.Room.RoomWidget import RoomWidget
from UI.Tab import Tab
from UI.Search.SearchFilterAll import SearchFilterAll
from UI.Search.SearchFilterBooks import SearchFilterBooks
from tkinter.filedialog import asksaveasfilename 


class SearchTab(Tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #
        # The header of the tab
        #
        self.header_label = CTkLabel(self, text="Suche", font=("Arial", 25, "bold"))
        self.header_label.pack(padx=0, pady=10)

        
        #
        # Selection widget to choose between search for: everything, books, authors, book types or rooms
        #
        self.selectCTkFrame = CTkFrame(self, fg_color="transparent")
        self.selectCTkFrame.pack(padx=0, pady=10)

        self.selectVar = StringVar(self.selectCTkFrame, "1")
        self.selectVar.trace_add("write", self.refresh)

        self.selectCTkLabel = CTkLabel(self.selectCTkFrame, text="Suche nach: ")
        self.selectCTkLabel.grid(row=0, columnspan=5, pady=10)

        self.selectAll = CTkRadioButton(self.selectCTkFrame, text="Alles", value=1, variable=self.selectVar)
        self.selectAll.grid(row=1, column=0, padx=5)

        self.selectBooks = CTkRadioButton(self.selectCTkFrame, text="Bücher", value=2, variable=self.selectVar)
        self.selectBooks.grid(row=1, column=1, padx=5)
        
        self.selectAuthors = CTkRadioButton(self.selectCTkFrame, text="Autoren", value=3, variable=self.selectVar)
        self.selectAuthors.grid(row=1, column=2, padx=5)

        self.selectTypes = CTkRadioButton(self.selectCTkFrame, text="Buchtypen", value=4, variable=self.selectVar)
        self.selectTypes.grid(row=1, column=3, padx=5)

        self.selectRooms = CTkRadioButton(self.selectCTkFrame, text="Räume", value=5, variable=self.selectVar)
        self.selectRooms.grid(row=1, column=4, padx=5)


        #
        #  The frame in which the filter options for the above selected option appear
        #
        self.filterCTkFrame = CTkFrame(self, fg_color="transparent")
        self.filterCTkFrame.pack(padx=10, pady=10, expand=True, fill="both")


        #
        # The search button
        #
        self.buttonCTkFrame = CTkFrame(self, fg_color="transparent")
        self.buttonCTkFrame.pack(padx=10, pady=10)
        self.searchCTkButton = CTkButton(self.buttonCTkFrame, text="Suchen", command=self.search)
        self.searchCTkButton.grid(row=10, column=0)
        self.exportCTkButton = CTkButton(self.buttonCTkFrame, text="Ergebnisse exportieren (CSV)", command=self.export, state=DISABLED)
        self.exportCTkButton.grid(row=10, column=1, padx=10)


        #
        # The filters for searching everything
        #
        self.filterAll = SearchFilterAll(self.filterCTkFrame)

        #
        # The filters for searching for books
        #
        self.filterBooks = SearchFilterBooks(self.filterCTkFrame)
        
        #
        # The filters for searching authors
        #
        self.filterAuthors = CTkFrame(self.filterCTkFrame)
        self.fn_label = CTkLabel(self.filterAuthors, text="Vorname: ")
        self.fn_entry = CTkEntry(self.filterAuthors)
        self.fn_label.grid(row=0, column=0, padx=10, pady=10)
        self.fn_entry.grid(row=0, column=1, padx=10)        
        self.ln_label = CTkLabel(self.filterAuthors, text="Nachname: ")
        self.ln_entry = CTkEntry(self.filterAuthors)
        self.ln_label.grid(row=1, column=0, padx=10, pady=10)
        self.ln_entry.grid(row=1, column=1, padx=10)

        #
        # The filters for searching for book types
        #
        self.filterTypes = CTkFrame(self.filterCTkFrame)

        self.type_label = CTkLabel(self.filterTypes, text="Name: ")
        self.type_entry = CTkEntry(self.filterTypes)
        self.type_label.grid(row=0, column=0, padx=10, pady=10)
        self.type_entry.grid(row=0, column=1, padx=10)


        #
        # The filters for searching for rooms
        #
        self.filterRooms = CTkFrame(self.filterCTkFrame)

        self.room_label = CTkLabel(self.filterRooms, text="Name: ")
        self.room_entry = CTkEntry(self.filterRooms)
        self.room_label.grid(row=0, column=0, padx=10, pady=10)
        self.room_entry.grid(row=0, column=1, padx=10)


        #
        # The results for each category
        #
        self.resultBooks = []
        self.resultBooksCTkFrame = CTkFrame(self, fg_color="transparent")
        self.resultBooksHeader = CTkLabel(self.resultBooksCTkFrame, text="Bücher", font=("Arial", 18, "bold"))
        self.resultBooksHeader.pack()
        self.resultBooksCTkFrame.pack(pady=10)

        self.resultAuthors = []
        self.resultAuthorsCTkFrame = CTkFrame(self, fg_color="transparent")
        self.resultAuthorsHeader = CTkLabel(self.resultAuthorsCTkFrame, text="Autoren", font=("Arial", 18, "bold"))
        self.resultAuthorsHeader.pack()

        self.resultTypes = []
        self.resultTypesCTkFrame = CTkFrame(self, fg_color="transparent")
        self.resultTypesHeader = CTkLabel(self.resultTypesCTkFrame, text="Buchtypen", font=("Arial", 18, "bold"))
        self.resultTypesHeader.pack()

        self.resultRooms = []
        self.resultRoomsCTkFrame = CTkFrame(self, fg_color="transparent")
        self.resultRoomsHeader = CTkLabel(self.resultRoomsCTkFrame, text="Räume", font=("Arial", 18, "bold"))
        self.resultRoomsHeader.pack()

        self.refresh()


    def refresh(self, *args):
        # Remove all shown filters
        self.filterAll.pack_forget()
        self.filterBooks.pack_forget()
        self.filterAuthors.pack_forget()
        self.filterTypes.pack_forget()
        self.filterRooms.pack_forget()
        # And all shown results
        self.resultBooksCTkFrame.pack_forget()
        self.resultAuthorsCTkFrame.pack_forget()
        self.resultTypesCTkFrame.pack_forget()
        self.resultRoomsCTkFrame.pack_forget()
        

        for book in self.resultBooks:
            if book.winfo_exists() == 1:
                for child in book.winfo_children():
                    child.destroy()
            book.destroy()
        self.resultBooks = []

        for author in self.resultAuthors:
            if author.winfo_exists():
                for child in author.winfo_children():
                    child.destroy()
            author.destroy()
        self.resultAuthors = []

        for book_type in self.resultTypes:
            for child in book_type.winfo_children():
                if child.winfo_exists():
                    child.destroy()
            book_type.destroy()
        self.resultTypes = []

        for room in self.resultRooms:
            for child in room.winfo_children():
                if child.winfo_exists():
                    child.destroy()
            room.destroy()
        self.resultRooms = []


        for child in self.resultBooksCTkFrame.winfo_children():
            if type(child) != CTkLabel:
                child.destroy()
        for child in self.resultAuthorsCTkFrame.winfo_children():
            if type(child) != CTkLabel:
                child.destroy()
        for child in self.resultTypesCTkFrame.winfo_children():
            if type(child) != CTkLabel:
                child.destroy()
        for child in self.resultRoomsCTkFrame.winfo_children():
            if type(child) != CTkLabel:
                child.destroy()

        self.filterBooks.refresh()

        self.exportCTkButton.configure(state=DISABLED)

        # Then show the ones needed for the current selection
        match self.selectVar.get():
            case "1":
                # Everything
                self.all_types = fetch_book_types()
                self.all_rooms = fetch_rooms()
                self.filterAll.pack()

            case "2":
                # Books
                self.all_types = fetch_book_types()
                self.all_rooms = fetch_rooms()
                self.filterBooks.pack(expand=True, fill="both")
                self.resultBooksCTkFrame.pack(pady=10)

            case "3":
                # Authors
                self.filterAuthors.pack()
                self.resultAuthorsCTkFrame.pack(pady=10)
            
            case "4":
                # Book types
                self.filterTypes.pack()
                self.resultTypesCTkFrame.pack(pady=10)

            case "5":
                # Rooms
                self.filterRooms.pack()
                self.resultRoomsCTkFrame.pack(pady=10)

    def search(self):
        for book in self.resultBooks:
            if book.winfo_exists() == 1:
                for child in book.winfo_children():
                    child.destroy()
            book.destroy()
        self.resultBooks = []

        for author in self.resultAuthors:
            if author.winfo_exists():
                for child in author.winfo_children():
                    child.destroy()
                author.destroy()
        self.resultAuthors = []

        for book_type in self.resultTypes:
            for child in book_type.winfo_children():
                if child.winfo_exists():
                    child.destroy()
                book_type.destroy()
        self.resultTypes = []

        for room in self.resultRooms:
            for child in room.winfo_children():
                if child.winfo_exists():
                    child.destroy()
                room.destroy()
        self.resultRooms = []

        if self.selectVar.get() != "1":
            self.exportCTkButton.configure(state=ACTIVE)

        match self.selectVar.get():
            case "1":
                # Get the search value
                search_value = self.filterAll.entry.get()


                # Remove all old search results 
                for book in self.resultBooks:
                    if book.winfo_exists() == 1:
                        for child in book.winfo_children():
                            child.destroy()
                    book.destroy()
                self.resultBooks = []

                for author in self.resultAuthors:
                    if author.winfo_exists():
                        for child in author.winfo_children():
                            child.destroy()
                    author.destroy()
                self.resultAuthors = []

                for book_type in self.resultTypes:
                    for child in book_type.winfo_children():
                        if child.winfo_exists():
                            child.destroy()
                    book_type.destroy()
                self.resultTypes = []

                for room in self.resultRooms:
                    for child in room.winfo_children():
                        if child.winfo_exists():
                            child.destroy()
                    room.destroy()

                self.resultRooms = []


                # Get a list of all items in the db
                all_books = fetch_books()
                all_authors = fetch_authors()
                all_types = fetch_book_types()
                all_type_ids = fetch_book_type_ids()
                all_rooms = fetch_rooms()
                all_room_ids = fetch_room_ids()

                # Search the books
                for book in all_books:
                    if search_value in book.title:
                        self.resultBooks.append(BookWidget(self.resultBooksCTkFrame, book.id))

                # Display the found books
                for bookWidget in self.resultBooks:
                    bookWidget.pack(pady=20)


                # Sound the authors
                for author in all_authors:
                    if search_value in author.getName():
                        self.resultAuthors.append(AuthorWidget(self.resultAuthorsCTkFrame, author.id))

                # Display the found authors
                for authorWidget in self.resultAuthors:
                    authorWidget.pack(pady=20)

                
                # Search the book types
                for index, book_type in enumerate(all_types):
                    if search_value in book_type:
                        id = fetch_book_type_id(book_type)
                        self.resultTypes.append(TypeWidget(self.resultTypesCTkFrame, id))

                # Display the found book types
                for typeWidget in self.resultTypes:
                    typeWidget.pack(pady=20)


                # Search the rooms
                for index, room in enumerate(all_rooms):
                    if search_value in room:
                        id = all_room_ids[index]
                        self.resultRooms.append(RoomWidget(self.resultRoomsCTkFrame, id))

                # Display the found rooms
                for roomWidget in self.resultRooms:
                    roomWidget.pack(pady=20)

                # Show the results
                self.resultBooksCTkFrame.pack(pady=10)
                self.resultAuthorsCTkFrame.pack(pady=10)
                self.resultTypesCTkFrame.pack(pady=10)
                self.resultRoomsCTkFrame.pack(pady=10)

            case "2":
                # Searching for books
                for book in self.resultBooks:
                    for child in book.winfo_children():
                        if child.winfo_exists():
                            child.destroy()
                    book.destroy()
                self.resultBooks = []

                all_books = fetch_books()

                conditions = []
                params = []

                title = self.filterBooks.title.get()
                author_ids = self.filterBooks.authors.get()
                publisher = self.filterBooks.publisher.get()
                isbn = self.filterBooks.isbn.get()
                edition = self.filterBooks.edition.get()
                year = self.filterBooks.year.get()
                book_type = None
                book_type_name = self.filterBooks.type_select.get()
                tags = self.filterBooks.tags.get().replace("; ", ";").split(";")
                room = None
                room_name = self.filterBooks.room.get()
                shelf = self.filterBooks.shelf.get()
                lend = None
                lend_str = self.filterBooks.lend.get()
                lend_to = self.filterBooks.lend_to.get()
                language = self.filterBooks.language.get()

                if lend_str == "Ja":
                    lend = 1
                elif lend_str == "Nein":
                    lend = 0

                if title:
                    conditions.append("book_title LIKE ?")
                    params.append("%" + title + "%")

                if author_ids != []:
                    for author_id in author_ids:
                        conditions.append("book_id IN (SELECT abBookID FROM author_books WHERE abAuthorID = ?)")
                        params.append(author_id)

                if publisher:
                    conditions.append("book_publisher LIKE ?")
                    params.append("%" + publisher + "%")

                if isbn:
                    conditions.append("book_isbn LIKE ?")
                    params.append("%" + isbn + "%")

                if edition:
                    conditions.append("book_edition = ?")
                    params.append(edition)

                if year:
                    conditions.append("book_year = ?")
                    params.append(year)

                if book_type:
                    cirteria.append("book_type = ?")
                    params.append(book_type)

                if tags != ['']:
                    for tag in tags:
                        conditions.append("book_tags LIKE ?")
                        params.append("%" + tag + "%")

                if room:
                    conditions.append("book_room LIKE ?")
                    params.append("%" + room + "%")

                if shelf:
                    conditions.append("book_shelf LIKE ?")
                    params.append("%" + shelf + "%")

                if lend:
                    conditions.append("book_lend = ?")
                    params.append(lend)

                if lend_to:
                    conditions.append("lendTo LIKE ?")
                    params.append(lend_to)

                if language:
                    conditions.append("book_language LIKE ?")
                    params.append("%" + language + "%")

                db, cur = prepare_db()

                if len(conditions) > 0:
                    book_ids = [ row[0] for row in cur.execute("SELECT book_id FROM books WHERE " + " AND ".join(conditions) + ";", tuple(params)).fetchall() ]
                else:
                    book_ids = fetch_book_ids()

                cur.close()
                db.close()

                for book_id in book_ids:
                    self.resultBooks.append(BookWidget(self.resultBooksCTkFrame, book_id))
                

                # Pack the book widgets
                for bookWidget in self.resultBooks:
                    bookWidget.pack(pady=20)

                # Display the results
                self.resultBooksCTkFrame.pack(pady=10)

            # Searching for authors
            case "3":
                for author in self.resultAuthors:
                    for child in author.winfo_children():
                        if child.winfo_exists():
                            child.destroy()
                    author.destroy()
                self.resultAuthors = []

                conditions = []
                params = []

                if self.fn_entry.get():
                    conditions.append("firstName LIKE ?")
                    params.append("%" + self.fn_entry.get() + "%")

                if self.ln_entry.get():
                    conditions.append("lastName LIKE ?")
                    params.append("%" + self.ln_entry.get() + "%")

                db, cur = prepare_db()

                if len(conditions)> 0:
                    authorIDs = [ row[0] for row in cur.execute("SELECT author_id FROM authors WHERE " + "AND".join(conditions) + ";", tuple(params)).fetchall() ]
                else:
                    authorIDs = fetch_author_ids()

                for id in authorIDs:
                    self.resultAuthors.append(AuthorWidget(self.resultAuthorsCTkFrame, id))

                for authorWidget in self.resultAuthors:
                    authorWidget.pack(pady=20)

                self.resultAuthorsCTkFrame.pack(pady=10)

            # Searching for book types
            case "4":
                for book_type in self.resultTypes:
                    for child in book_type.winfo_children():
                        if child.winfo_exists():
                            child.destroy()
                    book_type.destroy()
                self.resultTypes = []

                db, cur = prepare_db()

                ids = [ row[0] for row in cur.execute("SELECT type_id FROM types WHERE type_name LIKE ?;", ("%" + self.type_entry.get() + "%",)).fetchall() ]

                for id in ids:
                    self.resultTypes.append(TypeWidget(self.resultTypesCTkFrame, id))

                for typeWidget in self.resultTypes:
                    typeWidget.pack(pady=20)

                self.resultTypesCTkFrame.pack(pady=10)

            # Searching for rooms
            case "5":
                for room in self.resultRooms:
                    for child in room.winfo_children():
                        if child.winfo_exists():
                            child.destroy()
                    room.destroy()
                self.resultTypes = []

                db, cur = prepare_db()

                ids = [ row[0] for row in cur.execute("SELECT room_id FROM rooms WHERE room_name LIKE ?;", ("%" + self.room_entry.get() + "%",)).fetchall() ]

                for id in ids:
                        self.resultRooms.append(RoomWidget(self.resultRoomsCTkFrame, id))

                for roomWidget in self.resultRooms:
                    roomWidget.pack(pady=20)

                self.resultRoomsCTkFrame.pack(pady=10)


    # Exports search results of detail searches (not general search) to a CSV file
    def export(self):
        app_context.logger.info("Preparing data for CSV export")
        match self.selectVar.get():
            case "2":
                data = [
                        ["ID", "Titel", "Autoren", "Verlag", "ISBN", "Auflage", "Jahr", "Typ", "Stichwörter",
                         "Raum", "Regal", "Verliehen", "Verliehen an","Sprache"]
                ]

                for bookWidget in self.resultBooks:
                    book = fetch_book(bookWidget.id)
                    book_data = str(book).split(",, ")
                    book_data[2] = ", ".join(eval(book_data[2]))
                    book_data[8] = ", ".join(eval(book_data[8]))
                    book_data[9] = fetch_room(book_data[9])
                    book_data[7] = fetch_book_type(book_data[7])
                    book_data[11] = "Ja" if book_data[11] == "1" else "Nein"
                    data.append(book_data)

            case "3":
                data = [["ID", "Vorname", "Nachname"]]

                for authorWidget in self.resultAuthors:
                    author = fetch_author(authorWidget.id)
                    author_data = str(author).split(",, ")
                    data.append(author_data)

            case "4":
                data = [["ID", "Name"]]

                db, cur = prepare_db()

                for typeWidget in self.resultTypes:
                    type_data = cur.execute("SELECT * FROM types WHERE type_id = ?;", (typeWidget.id,)).fetchall()[0]
                    data.append(type_data)

                cur.close()
                db.close()

            case "5":
                data = [["ID", "Name"]]

                db, cur = prepare_db()

                for roomWidget in self.resultRooms:
                    room_data = cur.execute("SELECT * FROM rooms WHERE room_id = ?;", (roomWidget.id,)).fetchall()[0]
                    data.append(room_data)

                cur.close()
                db.close()

        if self.selectVar.get() != "1":
            filename = asksaveasfilename(title="Datei für den CSV Exportauswählen", filetypes=[("CSV Liste", "*.csv"), ("Alle Dateien", "*.*")])
            if filename:
                with open(filename, mode="w", newline="") as file:
                    app_context.logger.info("Exporting search results to '" + filename + "'")
                    writer = csv.writer(file)
                    writer.writerows(data)
