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
test_book = BookDisplay(mainTab, "Hello World", "../Web/static/noCover.png", 1)
test_book.pack(pady = 10, padx = 20)


root.mainloop()


