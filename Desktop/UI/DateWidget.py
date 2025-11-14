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


from tkinter import Frame, Label
from tkinter.ttk import Spinbox
from datetime import date


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

        self.year.set(str(2200))
        self.month.set(str(1))
        self.day.set(str(1))

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
            self.day.set(str(1))

    def get(self):
        # Get the currently selected values
        year = int(self.year.get())
        month = int(self.month.get())
        day = int(self.day.get())
        
        # Return a date object with these values
        return date(year, month, day)
    

    def set(self, date: date):
        self.year.set(str(date.year))
        self.month.set(str(date.month))
        self.day.set(str(date.day))
        self.update()

