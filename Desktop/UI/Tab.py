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


from tkinter import Canvas, Frame, Scrollbar


class Tab(Frame):
    def __init__(self, *args, **kwargs):
        # --------------------------------------------------------------------------------------------------------------------------- #
        # ChatGPT generated code, because I don't understand how scrollbars work in tkinter (haven't found a good explanation yet)... #
        # --------------------------------------------------------------------------------------------------------------------------- #

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
