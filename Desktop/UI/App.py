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
from customtkinter import CTkLabel, CTk
from customtkinter import CTkTabview
from UI.Author.AuthorsTab import AuthorsTab
from UI.Book.BooksTab import BooksTab
from UI.BookType.TypesTab import TypesTab
from UI.OverviewTab import OverviewTab
from UI.Room.RoomsTab import RoomsTab
from UI.Search.SearchTab import SearchTab


class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        # Is called after app_context.logger is initialized
        app_context.logger.info("Initializing main window")
        self.title("Lerchbacher Bücherdatenbank")

        app_context.mainWindow = self

        app_context.logger.info("Creating tab control widget")
        self.tabControl = CTkTabview(self, fg_color="transparent")
        self.tabControl.pack(fill="both", expand=True)

        self.tabControl.add('Übersicht')
        self.tabControl.add('Bücher')
        self.tabControl.add('Autoren')
        self.tabControl.add('Buchtypen')
        self.tabControl.add('Räume')
        self.tabControl.add('Suche')
        
        app_context.logger.info("Populating tab control widget")
        self.overviewTab = OverviewTab(self.tabControl.tab("Übersicht"))
        self.booksTab = BooksTab(self.tabControl.tab("Bücher"))
        self.authorsTab = AuthorsTab(self.tabControl.tab("Autoren"))
        self.typesTab = TypesTab(self.tabControl.tab("Buchtypen"))
        self.roomsTab = RoomsTab(self.tabControl.tab("Räume"))
        self.searchTab = SearchTab(self.tabControl.tab("Suche"))
        
        self.overviewTab.pack(fill="both", expand=True)
        self.booksTab.pack(fill="both", expand=True)
        self.authorsTab.pack(fill="both", expand=True)
        self.typesTab.pack(fill="both", expand=True)
        self.roomsTab.pack(fill="both", expand=True)
        self.searchTab.pack(fill="both", expand=True)

        app_context.logger.info("Successfully initialized main window")
        
        self.bind("<Configure>", self.on_configure)
        self.minsize(800, 600)

        self.mainloop()
        
    def on_configure(self, event):
        self.update_idletasks()
        for child in widget.winfo_children():
            force_redraw(child)

    def refresh(self):
        self.overviewTab.refresh()
        self.booksTab.refresh()
        self.authorsTab.refresh()
        self.searchTab.refresh()
        self.typesTab.refresh()
        self.roomsTab.refresh()

