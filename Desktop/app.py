#
# Lerchbacher book database desktop
# Copyright 2025 Lars Lerchbacher
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

