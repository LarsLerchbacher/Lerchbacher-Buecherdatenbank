#
# Desktop/app.py
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


import app_context
from UIClasses import *
import sys


class ErrorHandler(object):
    def write(self, data):
        verbose = check_flags()[0]
        with open("log.txt", mode="a") as file:
            file.write(data)
        if verbose:
            print(data, end="")


def main() -> None:
    global mainWindow
    log_line()
    log("Lerchbacher book database desktop v0.0.1")
    log("Starting application")
    mainWindow = App()
    mainWindow.mainloop()


if __name__ == "__main__":
    # Proces the arguments
    args = sys.argv
    if len(args) > 1:
        del args[0]
        app_context.flags = args
    else:
        app_context.flags = []

    check_flags()

    errorHandler = ErrorHandler()
    sys.stderr = errorHandler
    main()

    log("Peacefully terminating application")
    log("Goodbye!")

