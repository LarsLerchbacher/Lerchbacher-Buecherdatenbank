#
#   The Lerchbacher book database project
#   © Lars Lerchbacher 2025-2026
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
from database import Author, Book, create_book, edit_book, fetch_author, fetch_authors, fetch_authors_for_book, fetch_book, fetch_book_type, fetch_book_type_id, fetch_book_types, fetch_room, fetch_room_id, fetch_rooms, prepare_db, create_author, fetch_book_by_isbn
from images import update_image
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from UI.Author.AuthorEditToplevel import AuthorEditToplevel
from UI.Book.BookEditWidget import BookEditWidget
from UI.ISBNWidget import ISBNWidget
from requests import get
import re
import threading


class BookAddToplevel(CTkToplevel):
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.title("Buch hinzufügen")

                self.label = CTkLabel(self, text="ISBN eingeben: ")
                self.isbn = ISBNWidget(self)
                self.isbn.pack(padx=20, pady=5)
                
                self.button_frame = CTkFrame(self, fg_color="transparent")
                self.button_frame.pack(padx=20, pady=5) 

                self.save_button = CTkButton(self.button_frame, text='Speichern', command=self.save)
                self.cancel_button = CTkButton(self.button_frame, text='Abbrechen', command=self.cancel)
                self.save_button.grid(row=0, column=0)
                self.cancel_button.grid(row=0, column=1, padx=10)

                self.bind("<Return>", lambda e: self.save())
        
        def save(self):
                self.save_button.configure(state="disabled")
                if not self.isbn.get() or len(self.isbn.get()) < 13:
                        app_context.logger.warning("Trying to add book via ISBN, but an invalid ISBN has been supplied.")
                        CTkMessagebox(icon="Warning", title="ISBN Fehlerhaft", message="Bitte geben Sie eine gültige ISBN ein!")
                        self.save_button.configure(state="normal")
                        return

                elif fetch_book_by_isbn(self.isbn.get()) != None:
                        CTkMessagebox(title="Buch existier bereits", message="Es existiert bereits ein Buch mit dieser ISBN.")
                        self.destroy()
                        return
                    
                try:
                    url_target = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{self.isbn.get()}" 
                    response = get(url_target, headers={"x-goog-api-key": "AIzaSyDuEts1XTeWZ0r-882BfQPM9pnUaS27xVs"}).json()
                    response = get(response["items"][0]["selfLink"], headers={"x-goog-api-key": "AIzaSyDuEts1XTeWZ0r-882BfQPM9pnUaS27xVs"}).json()
                except Exception as e:
                        app_context.logger.warning(f"Error while fetching book data: {type(e)}: {e}")
                        CTkMessagebox(icon="Error", title="Fehler bei der Abfrage", message="Beim Abfragen der Daten von Google Server ist ein Fehler aufgetreten.\nBitte überprüfen Sie die ISBN und versuchen Sie es erneut!")
                        self.destroy()
                        return

                title = response["volumeInfo"]["title"]
                authors = []
                db, cur = prepare_db()

                try:
                    for author_name in response["volumeInfo"]["authors"]:
                            nameParts = author_name.split(" ")
                            lastName = nameParts[-1]
                            firstName = " ".join(nameParts[:-1]) 
                            
                            
                            result = cur.execute("SELECT author_id FROM authors WHERE firstName == ? AND lastName == ?;", (firstName, lastName)).fetchone() 
                            if not result or len(result) != 1:
                                    create_author(Author(-1, firstName, lastName))
                                    id = int(cur.execute("SELECT seq FROM sqlite_sequence WHERE name == 'authors';").fetchone()[0])
                            else:
                                    id = int(result[0])

                            authors.append(id)

                except Exception as e:
                    app_context.logger.error(e)

                finally: 
                        cur.close()
                        db.commit()
                        db.close()
                
                publisher = response["volumeInfo"]["publisher"] if "publisher" in response["volumeInfo"].keys() else "" 
                year = int(response["volumeInfo"]["publishedDate"]) if "publishedDate" in response["volumeInfo"].keys() else 0
                tags = response["volumeInfo"]["categories"] if "catetories" in response["volumeInfo"].keys() else []
                language = response["volumeInfo"]["language"] if "language" in response["volumeInfo"].keys() else "Unbekannt"

                db, cur = prepare_db()
                try:
                        result = cur.execute("SELECT type_id from types WHERE type_name == 'Unbekannt';").fetchone()
                        if not result or len(result) != 1:
                                cur.execute("INSERT INTO types (type_name) VALUES ('Unbekannt');")
                                id = int(cur.execute("SELECT seq FROM sqlite_sequence WHERE name == 'types';").fetchone()[0])
                        else:
                                id = int(result[0])
                        
                        book_type = id
                
                except Exception as e:
                    app_context.logger.error(e)

                finally:
                        cur.close()
                        db.commit()
                        db.close()

                book = Book(title, authors, language, publisher, self.isbn.get(), 1, year, book_type, tags, "", "", "", -1)
                app_context.logger.debug(book)
                app_context.logger.info(f"Successfully added book for ISBN {self.isbn.get()}")

                creation_result = create_book(book)
                if type(creation_result) != int:
                        app_context.logger.error(f"Error while adding book via ISBN: {creation_result}")
                        CTkMessagebox(icon="Error", title="Fehler beim hinzufügen", message=f"Beim hinzufügen des Buches ist ein Fehler aufgetreten.")
                        self.save_button.configure(state="normal")
                else:
                        book.id = int(creation_result)
                        thread = threading.Thread(target=update_image, args=(book,))
                        thread.start()
                        app_context.mainWindow.refresh()
                        self.destroy()
                
        def cancel(self):
                self.destroy()
