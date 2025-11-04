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
from tkinter import Label, Tk
from tkinter.ttk import Notebook
from UI.Author.AuthorsTab import AuthorsTab
from UI.Book.BooksTab import BooksTab
from UI.BookType.TypesTab import TypesTab
from UI.OverviewTab import OverviewTab
from UI.Room.RoomsTab import RoomsTab
from UI.Search.SearchTab import SearchTab


class App(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        # Is called after app_context.logger is initialized
        app_context.logger.info("Initializing main window")
        self.title("Lerchbacher Bücherdatenbank")

        app_context.mainWindow = self

        app_context.logger.info("Creating tab control widget")
        self.tabControl = Notebook(self)
        self.tabControl.pack(fill="both", expand=True)

        app_context.logger.info("Populating tab control widget")
        self.overviewTab = OverviewTab(self.tabControl)
        self.booksTab = BooksTab(self.tabControl)
        self.authorsTab = AuthorsTab(self.tabControl)
        self.typesTab = TypesTab(self.tabControl)
        self.roomsTab = RoomsTab(self.tabControl)
        self.searchTab = SearchTab(self.tabControl)

        self.tabControl.add(self.overviewTab, text='Übersicht')
        self.tabControl.add(self.booksTab, text='Bücher')
        self.tabControl.add(self.authorsTab, text='Autoren')
        self.tabControl.add(self.typesTab, text='Buchtypen')
        self.tabControl.add(self.roomsTab, text='Räme')
        self.tabControl.add(self.searchTab, text='Suche')

        app_context.logger.info("Successfully initialized main window")

        self.mainloop()


    def update(self):
        self.mainTab.update()
        self.booksTab.update()
        self.authorsTab.update()
        self.searchTab.update()
        self.typesTab.update()
        self.roomsTab.update()

