#
# Lerchbacher book database desktop
# Copyright 2025 Lars Lerchbacher
#


import sys
from handle_db import *
from tkinter import *
from tkinter.ttk import *

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
header_label = Label(mainTab,text='Lerchbacher Buecherdatenbank')

tabControl.grid_columnconfigure(0, weight=1)
tabControl.grid_columnconfigure(1, weight=1)
tabControl.grid_columnconfigure(2, weight=1)
tabControl.grid_rowconfigure(0, weight=1)
tabControl.grid_rowconfigure(1, weight=1)
tabControl.grid_rowconfigure(2, weight=1)

header_label.grid(row=0, column=1, columnspan=3, sticky = 'WE', pady = 2)



root.mainloop()

