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


from database import fetch_authors, fetch_books, fetch_book_type_id, fetch_book_types, fetch_book_type_ids, fetch_rooms, fetch_room_id, fetch_room_ids
from datetime import date
from tkinter import *
from UI.Author.AuthorWidget import AuthorWidget
from UI.Book.BookWidget import BookWidget
from UI.BookType.TypeWidget import TypeWidget
from UI.Room.RoomWidget import RoomWidget
from UI.Tab import Tab
from UI.Search.SearchFilterAll import SearchFilterAll
from UI.Search.SearchFilterAuthors import SearchFilterAuthors
from UI.Search.SearchFilterBooks import SearchFilterBooks



class SearchTab(Tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #
        # The header of the tab
        #
        self.header_label = Label(self.inner_frame, text="Suche", font="Arial 25 bold")
        self.header_label.pack(padx=0, pady=10)

        
        #
        # Selection widget to choose between search for: everything, books, authors, book types or rooms
        #
        self.selectFrame = Frame(self.inner_frame)
        self.selectFrame.pack(padx=0, pady=10)

        self.selectVar = StringVar(self.selectFrame, "1")
        self.selectVar.trace_add("write", self.update)

        self.selectLabel = Label(self.selectFrame, text="Suche nach: ")
        self.selectLabel.grid(row=0, columnspan=5, pady=10)

        self.selectAll = Radiobutton(self.selectFrame, text="Alles", value=1, variable=self.selectVar)
        self.selectAll.grid(row=1, column=0, padx=5)

        self.selectBooks = Radiobutton(self.selectFrame, text="Bücher", value=2, variable=self.selectVar)
        self.selectBooks.grid(row=1, column=1, padx=5)
        
        self.selectAuthors = Radiobutton(self.selectFrame, text="Autoren", value=3, variable=self.selectVar)
        self.selectAuthors.grid(row=1, column=2, padx=5)

        self.selectTypes = Radiobutton(self.selectFrame, text="Buchtypen", value=4, variable=self.selectVar)
        self.selectTypes.grid(row=1, column=3, padx=5)

        self.selectRooms = Radiobutton(self.selectFrame, text="Räume", value=5, variable=self.selectVar)
        self.selectRooms.grid(row=1, column=4, padx=5)


        #
        #  The frame in which the filter options for the above selected option appear
        #
        self.filterFrame = Frame(self.inner_frame)
        self.filterFrame.pack(padx=0, pady=10)


        #
        # The search button
        #
        self.searchButton = Button(self.inner_frame, text="Suchen", command=self.search)
        self.searchButton.pack(padx=0, pady=10)


        #
        # The filters for searching everything
        #
        self.filterAll = SearchFilterAll(self.filterFrame)

        #
        # The filters for searching for books
        #
        self.filterBooks = SearchFilterBooks(self.filterFrame)
        
        #
        # The filters for searching authors
        #
        self.filterAuthors = SearchFilterAuthors(self.filterFrame)


        #
        # The filters for searching for book types
        #
        self.filterTypes = Frame(self.filterFrame)

        self.type_label = Label(self.filterTypes, text="Name: ")
        self.type_entry = Entry(self.filterTypes, width=30)
        self.type_label.grid(row=0, column=0, padx=10, pady=10)
        self.type_entry.grid(row=0, column=1, padx=10)


        #
        # The filters for searching for rooms
        #
        self.filterRooms = Frame(self.filterFrame)

        self.room_label = Label(self.filterRooms, text="Name: ")
        self.room_entry = Entry(self.filterRooms, width=30)
        self.room_label.grid(row=0, column=0, padx=10, pady=10)
        self.room_entry.grid(row=0, column=1, padx=10)


        #
        # The results for each category
        #
        self.resultBooks = []
        self.resultBooksFrame = Frame(self.inner_frame)
        self.resultBooksHeader = Label(self.resultBooksFrame, text="Bücher", font="Arial 18 bold")
        self.resultBooksHeader.pack()
        self.resultBooksFrame.pack(pady=10)

        self.resultAuthors = []
        self.resultAuthorsFrame = Frame(self.inner_frame)
        self.resultAuthorsHeader = Label(self.resultAuthorsFrame, text="Autoren", font="Arial 18 bold")
        self.resultAuthorsHeader.pack()

        self.resultTypes = []
        self.resultTypesFrame = Frame(self.inner_frame)
        self.resultTypesHeader = Label(self.resultTypesFrame, text="Buchtypen", font="Arial 18 bold")
        self.resultTypesHeader.pack()

        self.resultRooms = []
        self.resultRoomsFrame = Frame(self.inner_frame)
        self.resultRoomsHeader = Label(self.resultRoomsFrame, text="Räume", font="Arial 18 bold")
        self.resultRoomsHeader.pack()

        self.update()


    def update(self, *args):
        # Remove all shown filters
        self.filterAll.pack_forget()
        self.filterBooks.pack_forget()
        self.filterAuthors.pack_forget()
        self.filterTypes.pack_forget()
        self.filterRooms.pack_forget()
        # And all shown results
        self.resultBooksFrame.pack_forget()
        self.resultAuthorsFrame.pack_forget()
        self.resultTypesFrame.pack_forget()
        self.resultRoomsFrame.pack_forget()
        

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


        for child in self.resultBooksFrame.winfo_children():
            if type(child) != Label:
                child.destroy()
        for child in self.resultAuthorsFrame.winfo_children():
            if type(child) != Label:
                child.destroy()
        for child in self.resultTypesFrame.winfo_children():
            if type(child) != Label:
                child.destroy()
        for child in self.resultRoomsFrame.winfo_children():
            if type(child) != Label:
                child.destroy()

        # Then show the ones needed for the current selection
        match self.selectVar.get():
            case "1":
                # Everything
                self.all_types = fetch_book_types()
                self.all_rooms = fetch_rooms()
                self.filterBooks.authors.update()
                self.filterAll.pack()

            case "2":
                # Books
                self.all_types = fetch_book_types()
                self.all_rooms = fetch_rooms()
                self.filterBooks.authors.update()
                self.filterBooks.pack()
                self.resultBooksFrame.pack(pady=10)

            case "3":
                # Authors
                self.filterAuthors.pack()
                self.resultAuthorsFrame.pack(pady=10)
            
            case "4":
                # Book types
                self.filterTypes.pack()
                self.resultTypesFrame.pack(pady=10)

            case "5":
                # Rooms
                self.filterRooms.pack()
                self.resultRoomsFrame.pack(pady=10)

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

                if search_value != "":
                    # Search the books
                    for book in all_books:
                        if search_value in book.title:
                            self.resultBooks.append(BookWidget(self.resultBooksFrame, book.id))

                    # Display the found books
                    for bookWidget in self.resultBooks:
                        bookWidget.pack(pady=20)


                    # Sound the authors
                    for author in all_authors:
                        if search_value in author.name:
                            self.resultAuthors.append(AuthorWidget(self.resultAuthorsFrame, author.id))

                    # Display the found authors
                    for authorWidget in self.resultAuthors:
                        authorWidget.pack(pady=20)

                    
                    # Search the book types
                    for index, book_type in enumerate(all_types):
                        if search_value in book_type:
                            id = fetch_book_type_id(book_type)
                            self.resultTypes.append(TypeWidget(self.resultTypesFrame, id))

                    # Display the found book types
                    for typeWidget in self.resultTypes:
                        typeWidget.pack(pady=20)


                    # Search the rooms
                    for index, room in enumerate(all_rooms):
                        if search_value in room:
                            id = all_room_ids[index]
                            self.resultRooms.append(RoomWidget(self.resultRoomsFrame, id))

                    # Display the found rooms
                    for roomWidget in self.resultRooms:
                        roomWidget.pack(pady=20)

                    # Show the results
                    self.resultBooksFrame.pack(pady=10)
                    self.resultAuthorsFrame.pack(pady=10)
                    self.resultTypesFrame.pack(pady=10)
                    self.resultRoomsFrame.pack(pady=10)

                # If the search bar is empty, update the display
                else:
                    self.update()

            case "2":
                # Searching for books
                for book in self.resultBooks:
                    for child in book.winfo_children():
                        if child.winfo_exists():
                            child.destroy()
                    book.destroy()
                self.resultBooks = []

                all_books = fetch_books()


                for book in all_books:
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

                    if lend_str == "Ja":
                        lend = 1
                    elif lend_str == "Nein":
                        lend = 0


                    if book_type_name:
                        book_type = fetch_book_type_id(book_type_name)

                    if room_name:
                        room = fetch_room_id(room_name)


                    criteria = []

                    if title:
                        if title in book.title:
                            criteria.append(True)
                        else:
                            continue

                    if author_ids != []:
                        containsAuthors = []
                        for author_id in author_ids:
                            if author_id in book.author_ids:
                                containsAuthors.append(True)
                            else: 
                                containsAuthors.append(False)
                            
                        if (True in containsAuthors) and (False not in containsAuthors):
                            criteria.append(True)
                        else:
                            continue

                    if publisher:
                        if publisher in book.publisher:
                            criteria.append(True)
                        else:
                            continue

                    if isbn:
                        if isbn in str(book.isbn):
                            criteria.append(True)
                        else:
                            continue

                    if edition:
                        if edition == book.edition:
                            criteria.append(True)
                        else:
                            continue

                    if year:
                        if int(year) == book.year:
                            criteria.append(True)
                        else:
                            continue

                    if book_type != None:
                        print(book_type)
                        print(book.type)
                        if book_type == book.type:
                            print("Matching")
                            criteria.append(True)

                    if tags != []:
                        for tag in tags:
                            if tag in book.tags:
                               criteria.append(True)
                            else:
                               continue

                    if room != None:
                        if room == book.room:
                            criteria.append(True)
                        else:
                            continue

                    if shelf != "":
                        if shelf in book.shelf:
                            criteria.append(True)
                        else:
                            continue

                    if lend != None:
                        if lend == book.lend:
                            criteria.append(True)
                        else:
                            continue
                    
                    if (False not in criteria) and (True in criteria):
                        self.resultBooks.append(BookWidget(self.resultBooksFrame, book.id))


                # Pack the book widgets
                for bookWidget in self.resultBooks:
                    bookWidget.pack(pady=20)

                # Display the results
                self.resultBooksFrame.pack(pady=10)

            case "3":
                for author in self.resultAuthors:
                    for child in author.winfo_children():
                        if child.winfo_exists():
                            child.destroy()
                    author.destroy()
                self.resultAuthors = []

                all_authors = fetch_authors()

                name = self.filterAuthors.name.get()
                country = self.filterAuthors.country.get()
                dob = self.filterAuthors.dob.get()
                dod = self.filterAuthors.dod.get()
                hasNobel = None
                hasNobelName = self.filterAuthors.npw.get()

                if hasNobelName == "Ja":
                    hasNobel = 1
                elif hasNobelName == "Nein":
                    hasNobel = 0

                for author in all_authors:
                    criteria = []

                    if name:
                        if name in author.name:
                            criteria.append(True)
                        else:
                            criteria.append(False)

                    if country:
                        if country in author.country:
                            criteria.append(True)
                        else:
                            criteria.append(False)

                    if dob != date(2200, 1, 1):
                        if dob == author.birthdate:
                            criteria.append(True)
                        else:
                            criteria.append(False)

                    if dod != date(2200, 1, 1):
                        if dob == author.date_of_death:
                            criteria.append(True)
                        else:
                            criteria.append(False)
                    
                    if hasNobel != None:
                        if hasNobel == author.has_nobel_prize:
                            criteria.append(True)
                        else:
                            criteria.append(False)

                    if (True in criteria) and (False not in criteria):
                        self.resultAuthors.append(AuthorWidget(self.resultAuthorsFrame, author.id))

                for authorWidget in self.resultAuthors:
                    authorWidget.pack(pady=20)

                self.resultAuthorsFrame.pack(pady=10)

            case "4":
                for book_type in self.resultTypes:
                    for child in book_type.winfo_children():
                        if child.winfo_exists():
                            child.destroy()
                    book_type.destroy()
                self.resultTypes = []

                self.all_types = fetch_book_types()
                search_value = self.type_entry.get()

                for book_type in self.all_types:
                    if search_value:
                        if search_value in book_type:
                            id = fetch_book_type_id(book_type)
                            self.resultTypes.append(TypeWidget(self.resultTypesFrame, id))

                for typeWidget in self.resultTypes:
                    typeWidget.pack(pady=20)

                self.resultTypesFrame.pack(pady=10)


            case "5":
                for room in self.resultRooms:
                    for child in room.winfo_children():
                        if child.winfo_exists():
                            child.destroy()
                    room.destroy()
                self.resultTypes = []

                self.all_rooms= fetch_rooms()
                search_value = self.room_entry.get()

                for room in self.all_rooms:
                    if search_value:
                        if search_value in room:
                            id = fetch_room_id(room)
                            self.resultRooms.append(RoomWidget(self.resultRoomsFrame, id))

                for roomWidget in self.resultRooms:
                    roomWidget.pack(pady=20)

                self.resultRoomsFrame.pack(pady=10)

