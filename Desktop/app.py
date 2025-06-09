#
# Lerchbacher book database desktop
# Copyright 2025 Lars Lerchbacher
#


import sys
from handle_db import *
from tkinter import *
from tkinter.ttk import *
from UIClasses import *

root = Tk()
root.title("Lerchbacher Buecherdatenbank")

tabControl = Notebook(root)
tabControl.pack(expand=1, fill='both')

mainTab = Frame(tabControl) 
booksTab = Frame(tabControl) 
authorsTab = Frame(tabControl)
searchTab = Frame(tabControl)

tabControl.add(mainTab, text = 'Hauptmenue') 
tabControl.add(booksTab, text = 'Buecher')
tabControl.add(authorsTab, text = 'Autoren')
tabControl.add(searchTab, text = 'Suche')



#
# Menu Tab
#
header_label = Label(mainTab,text='Lerchbacher Buecherdatenbank', font="Arial 25 bold")
header_label.pack(padx = 0, pady = 10)

recentBooks = RecentBooksWidget(mainTab)
recentBooks.pack(padx = 0, pady = 10)


#
# Books Tab
#
booksHeaderLabel = Label(booksTab, text = "Buecher", font = "Arial 25 bold")
booksHeaderLabel.pack(pady = 10)

allBooks = AllBooksWidget(booksTab)
allBooks.pack(pady = 10)


root.mainloop()


