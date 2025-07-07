#
# Lerchbacher book database desktop
# Copyright 2025 Lars Lerchbacher
#


from UIClasses import *
import sys



def write_args(args: list) -> None:
    with open("flags.txt", mode="w") as file:
        file.writelines(args)


def main() -> None:
    log_line()
    log("Lerchbacher book database desktop v0.0.1")
    log("Starting application")
    mainWindow = App()
    mainWindow.mainloop()


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        del args[0]
        write_args(args)
    else:
        write_args([])
    main()

    log("Peacefully terminating application")
    log("Goodbye!")

