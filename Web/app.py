#
# app.py
# ----------
# The Lerchbacher book database project
# © Lars Lerchbacher 2024-2025
#      This file is part of the Lerchbacher book database
#
#    the Lerchbacher book database is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#    The Lerchbacher book database is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along with the Lerchabcher book database. If not, see <https://www.gnu.org/licenses/>. 
#

from handle_db import *
from flask import *
import requests
from flask_bootstrap import Bootstrap5

from flask_wtf import CSRFProtect
import secrets
from forms import *

from datetime import date

app = Flask("Lerchbacher Bücherdatenbank")
foo = secrets.token_urlsafe(16)
app.secret_key = foo
app.config["SECRET_KEY"] = foo

bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)
csrf.init_app(app)

BOOK_TYPES = ["Kinderbuch", "Jugendbuch", "Roman", "Sachbuch"]


def fetch_covers(books:list) -> list:
    covers = []
    # Iterates through all books in the books list
    for book in books:

        # Tries to get a cover for the book using the Google books request API
        try:

            # Querries the API
            req = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:"+str(book.isbn))

            # Reads all available images for the book
            imageEntries = req.json()["items"][0]["volumeInfo"]["imageLinks"]

            # Creates a new empty list to store all the book cover links
            imageLinks = []

            # Iterates through all entries in the imageEntries dict
            for key, value in imageEntries.items():
                # Adds the link of the current entry to the imageLinks list
                imageLinks.append(value)

            # Tries to get the smallest cover
            cover = imageLinks[0]

        # If there is an error with the api or no book cover available
        except Exception:
            # Sets the cover to the noCover file
            cover = "/static/noCover.png"

        # Adds the current cover to the covers list
        covers.append(cover)

    return covers


@app.route("/")
def home():
    # Fetches the 12 last added books from the database
    books = fetch_books()[-4:]

    # Creates a new empty list to store all the covers for those books
    covers = fetch_covers(books)

    authors = fetch_authors()[-4:]

    # Returns the rendered webpage with all needed data to the user's browser
    return render_template("index.html", books=books, covers=covers, authors=authors)


@app.route("/books")
def all_books():
    books = fetch_books()

    # Creates a new empty list to store all the covers for those books
    covers = fetch_covers(books)

    return render_template("books.html", books=books, covers=covers)


# TODO: Comment book_detail function
@app.route("/books/details")
def book_detail():
    book_id = request.args.get('id')
    book = fetch_book_by_id(book_id)
    authors=[]
    for id in book.author_ids:
        authors.append(fetch_author_by_id(id))
    link = ""
    try:
        req = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:"+str(book.isbn))
        if req.status_code == 200:
            imageLinks = []
            for key, value in req.json()["items"][0]["volumeInfo"]["imageLinks"].items():
                imageLinks.append(value)
            cover = imageLinks[-1]
            
            if req.json()["items"][0]["volumeInfo"]["infoLink"]:
                link = req.json()["items"][0]["volumeInfo"]["infoLink"]
            else:
                link = ""
    except KeyError:
        cover = "/static/noCover.png"
    
    return render_template("book.html", book=book, cover=cover, authors=authors, link=link, type=book.type, tags=book.tags, isbn=str(book.isbn), types=BOOK_TYPES)


# TODO: Restructure and improve book_edit function
# TODO: Comment book_edit function
@app.route("/books/edit", methods=['GET', 'POST'])
@csrf.exempt
def book_edit():
    form = BookForm()

    if request.method == 'GET':
        form.authors.choices = [(str(author.id), author.name) for author in fetch_authors()]
        form.type.choices = [(index -2, type) for index, type in enumerate(BOOK_TYPES)]
        if request.args.get('id'):
            book_id = request.args.get('id')
            book = fetch_book_by_id(book_id)
            form.title.data = book.title
            form.authors.data = book.author_ids
            form.publisher.data = book.publisher
            form.isbn.data = book.isbn
            form.edition.data = book.edition
            form.year.data = book.year
            form.type.data = book.type
            form.tags.data = str(book.tags).replace('[', '').replace(']', '').replace("'", '').replace(',', ';')
            form.room.data = book.room
            form.shelf.data = book.shelf
            form.lend.data = book.lend
            form.id.data = book.id

        return render_template("edit_book.html", form=form)
    
    else:
        book_id = form.id.data
        book_title = form.title.data
        book_authors = form.authors.data
        book_publisher = form.publisher.data
        book_isbn = form.isbn.data
        book_edition = form.edition.data
        book_year = form.year.data
        book_type = form.type.data
        book_tags = str(form.tags.data.replace("; ", ";").split(";"))
        book_room = form.room.data
        book_shelf = form.shelf.data
        book_lend = form.lend.data

        new_book = Book(id=book_id, title=book_title, author_ids=book_authors, publisher=book_publisher, isbn=book_isbn, edition=book_edition, year=book_year,
                        type=book_type, tags=book_tags, room=book_room, shelf=book_shelf, lend=book_lend)

        if form.validate_on_submit():
            if form.id.data:
                if edit_book(book_id, new_book):
                    return redirect(f"/books/details?id={book_id}")
                else:
                    message = "Buch konnte nicht geändert/erstellt werden. Bitte prüfen Sie ob die ID korrekt ist/ein Buch mit diesem Namen bereits existiert."

                    return render_template("edit_book.html", form=form, message=message)
            else:
                if create_book(new_book):
                    created_book = fetch_book_by_title(new_book.title)
                    return redirect(f"/books/details?id={created_book.id}")

                else:
                    message = "Buch konnte nicht geändert/erstellt werden. Bitte prüfen Sie ob die ID korrekt ist/ein Buch mit diesem Namen bereits existiert."

                    return render_template("edit_book.html", form=form, message=message)

        else:

            message = "Buch konnte nicht geändert/erstellt werden. Bitte prüfen Sie ihre Eingabe!"

            return render_template("edit_book.html", form=form, message=message)


@app.route("/books/delete", methods=["GET", "POST"])
@csrf.exempt
def book_deletion():
    # Gets the book in question
    book_id = request.args.get("id")
    book = fetch_book_by_id(book_id)

    # Creates a WTF Form
    form = DeleteForm()

    # If the page is requested
    if request.method == "GET":
        # Shows the deletion protection prompt
        message = ""
        return render_template("delete_book.html", book=book, form=form, message=message)

    # If the page sends data
    else:
        # If the user wants to delete the book
        if form.checkbox.data:
            # If the passphrase is correct
            if delete_book(book_id, form.passphrase.data):
                # Deletes the book and redirects the user to the books overview page
                return redirect("/books")
            else:
                # If the deletion was not successful it sends the user a message
                message = "Löschen fehlgeschlagen! Bitte überprüfen Sie den Sicherheitscode!"
                return render_template("delete_book.html", book=book, form=form, message=message)


@app.route("/authors")
def authors_overview():
    authors = fetch_authors()
    return render_template("authors.html", authors=authors)


@app.route("/authors/details")
def author_details():
    # Fetches the author from the database
    author = fetch_author_by_id(request.args.get("id"))

    # Gets all the books, that the author contributed to
    books = fetch_books()
    author_books = [book for book in books if author.id in book.author_ids]

    # Creates a new empty list to store all the covers for those books
    covers = []

    # Iterates through all books in the books list
    for book in author_books:

        # Tries to get a cover for the book using the Google books request API
        try:

            # Querries the API
            req = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:" + str(book.isbn))

            # Reads all available images for the book
            imageEntries = req.json()["items"][0]["volumeInfo"]["imageLinks"]

            # Creates a new empty list to store all the book cover links
            imageLinks = []

            # Iterates through all entries in the imageEntries dict
            for key, value in imageEntries.items():
                # Adds the link of the current entry to the imageLinks list
                imageLinks.append(value)

            # Tries to get the smallest cover
            cover = imageLinks[0]

        # If there is an error with the api or no book cover available
        except Exception:
            # Sets the cover to the noCover file
            cover = "/static/noCover.png"

        # Adds the current cover to the covers list
        covers.append(cover)

    # Returns the rendered page
    return render_template("author.html", author=author, books=author_books, covers=covers, default_death=date(2200, 1, 1))


@app.route("/authors/edit", methods=["GET", "POST"])
@csrf.exempt
def author_editing():
    form = AuthorForm()

    if request.method == "GET":
        # If a certain author was requested in the url
        if request.args.get("id"):
            # Fetches the authors data and fills it in the form
            author = fetch_author_by_id(request.args.get("id"))
            form.name.data = author.name
            form.country.data = author.country
            form.birthdate.process_data(author.birthdate)
            form.date_of_death.process_data(author.date_of_death)
            form.has_nobel_prize.data = author.has_nobel_prize
            form.id.data = int(author.id)

            # Returns the user the rendered page
            return render_template("edit_author.html", form=form, message="")

        # If a new author should be created
        else:
            # Returns the rendered page with an empty form
            return render_template("edit_author.html", form=form, message="")

    # If the form is submitted
    else:
        # If all validators are fulfilled
        if form.validate_on_submit():

            # Creates a new author object with the received data
            if form.date_of_death.data:
                new_author = Author(form.id.data, name=form.name.data, has_nobel_prize=form.has_nobel_prize.data,
                                    country=form.country.data, birthdate=str(form.birthdate.data), date_of_death=str(form.date_of_death.data))
            else:
                new_author = Author(form.id.data, name=form.name.data, has_nobel_prize=form.has_nobel_prize.data,
                                    country=form.country.data, birthdate=str(form.birthdate.data))

            # If an existing author should be edited
            if form.id.data:
                # Tries to edit the author
                if edit_author(form.id.data, new_author):
                    return redirect(f"/authors/details?id={form.id.data}")

                # Messages the user, that the editing failed
                else:
                    message = ("Autor konnte nicht geändert werden. "
                               "Bitte prüfen Sie ob die ID korrekt ist/ein Autor mit diesem Namen bereits existiert.")
                    return render_template("edit_author.html", form=form, message=message, default_death=date(2200, 1, 1))

            # If a new author should be created
            else:
                # Tries to create a new author
                if create_author(new_author):
                    return redirect(f"/authors/details?id={fetch_author_by_name(form.name.data).id}")

                # Messages the user, that the editing failed
                else:
                    message = ("Autor konnte nicht erstellt werden. "
                               "Bitte prüfen Sie ob die ID korrekt ist/ein Autor mit diesem Namen bereits existiert.")
                    return render_template("edit_author.html", form=form, message=message, default_death=date(2200, 1, 1))

        # If the form is not valid
        else:
            # Asks the user to check their input
            message = "Buch konnte nicht geändert/erstellt werden. Bitte prüfen Sie ihre Eingabe!"
            return render_template("edit_author.html", form=form, message=message, default_death=date(2200, 1, 1))


@app.route("/authors/delete", methods=["GET", "POST"])
@csrf.exempt
def author_deletion():
    # Gets the author in question
    author_id = request.args.get("id")
    author = fetch_author_by_id(author_id)

    # Creates a WTF Form
    form = DeleteForm()

    # If the page is requested
    if request.method == "GET":
        # Shows the deletion protection prompt
        message = ""
        return render_template("delete_author.html", author=author, form=form, message=message)

    # If the page sends data
    else:
        # If the user wants to delete the author
        if form.checkbox.data:
            # If the passphrase is correct
            if delete_author(author.name, form.passphrase.data):
                # Deletes the author and redirects the user to the author overview page
                return redirect("/authors")
            else:
                # If the deletion was not successful it sends the user a message
                message = "Löschen fehlgeschlagen! Bitte überprüfen Sie den Sicherheitscode!"
                return render_template("delete_author.html", author=author, form=form, message=message)


@app.route("/search", methods=["GET", "POST"])
@csrf.exempt
def search():
    searchForm = SearchForm()
    bookForm = BookSearchForm()
    authorForm = AuthorSearchForm()

    if request.args.get("type"):
        type = request.args.get("type")
    else:
        type = "Alles"

    bookForm.authors.choices = [(index, author) for index, author in enumerate(["Bitte auswählen", "Niemand"] + fetch_author_names())]
    bookForm.type.choices = [(index, type) for index, type in enumerate(["Bitte auswählen"] + BOOK_TYPES)]
    bookForm.lend.choices = [(index, user) for index, user in enumerate(["Bitte auswählen", "Niemandem"] + fetch_user_names())]

    books = fetch_books()
    authors = fetch_authors()
    users = fetch_users()

    if request.method == "GET":
        return render_template("search.html", authorForm=authorForm, bookForm=bookForm, searchForm=searchForm, books=[], authors=[], type=type)

    else:
        if type == "Alles":
            results_books = [book for book in books if searchForm.searchBar.data.lower() in str(book).lower() if searchForm.searchBar.data]
            results_authors = [author for author in authors if searchForm.searchBar.data.lower() in str(author).lower() if searchForm.searchBar.data]
            result_users = [user for user in users if searchForm.searchBar.data.lower() in str(user).lower() if searchForm.searchBar.data]
            covers = fetch_covers(results_books)
            return render_template("search.html", authorForm=authorForm, bookForm=bookForm, searchForm=searchForm, books=results_books, authors=results_authors, users=result_users, type=type, covers=covers)
        elif type == "Buch":
            results_books = []
            for book in books:
                if bookForm.title.data and bookForm.title.data.lower() in book.title.lower():
                    results_books.append(book)
                    continue
                elif bookForm.id.data != None and bookForm.id.data == book.id:
                    results_books.append(book)
                    continue
                elif bookForm.isbn.data and str(bookForm.isbn.data) in str(book.isbn):
                    results_books.append(book)
                    continue
                elif bookForm.year.data and bookForm.year.data == book.year:
                    results_books.append(book)
                    continue
                elif bookForm.lend.data != -2:
                    if bookForm.lend.data == book.lend:
                        results_books.append(book)
                        continue
                elif bookForm.type.data != 0 and int(bookForm.type.data) == int(book.type)+1:
                    results_books.append(book)
                    continue
                elif bookForm.edition.data and int(bookForm.edition.data) == int(book.edition):
                    results_books.append(book)
                    continue
                elif bookForm.publisher.data and bookForm.publisher.data.lower() in book.publisher.lower():
                    results_books.append(book)
                    continue
                elif bookForm.room.data != "Bitte auswählen" and bookForm.room.data in book.room:
                    results_books.append(book)
                    continue
                elif bookForm.shelf.data and bookForm.shelf.data.lower() in book.shelf.lower():
                    results_books.append(book)
                    continue
                if bookForm.tags.data:
                    for searchTag in bookForm.tags.data.lower().split(";"):
                        if searchTag.lower() in str(book.tags):
                            results_books.append(book)
                if bookForm.authors.data and bookForm.authors.data != -2:
                    for author in bookForm.authors.data:
                        if author - 1 in book.author_ids:
                            results_books.append(book)

            covers = fetch_covers(results_books)
            return render_template("search.html", authorForm=authorForm, bookForm=bookForm, searchForm=searchForm, books=results_books, authors=[], type=type, covers=covers)
        elif type == "Autor":
            results_authors = []

            for author in authors:
                if authorForm.name.data and authorForm.name.data.lower() in author.name.lower():
                    results_authors.append(author)
                    continue
                elif authorForm.id.data == author.id and authorForm.id.data:
                    results_authors.append(author)
                    continue
                elif  authorForm.country.data and authorForm.country.data.lower() in author.country.lower():
                    results_authors.append(author)
                    continue
                elif authorForm.birthdate.data and authorForm.birthdate.data == author.birthdate:
                    results_authors.append(author)
                    continue
                elif authorForm.date_of_death.data and authorForm.date_of_death.data == author.date_of_death:
                    results_authors.append(author)
                    continue
                elif authorForm.has_nobel_prize.data != "Bitte auswählen":
                    if authorForm.has_nobel_prize.data == "Ja" and author.has_nobel_prize:
                        results_authors.append(author)
                        continue
                    elif authorForm.has_nobel_prize.data == "Nein" and not author.has_nobel_prize:
                        results_authors.append(author)
                        continue

            return render_template("search.html", authorForm=authorForm, bookForm=bookForm, searchForm=searchForm,
                                   books=[], authors=results_authors, type=type, covers=[])


@app.route("/users/")
def user_list():

    users = fetch_users()

    return render_template("users.html", users=users)


@app.route("/users/details")
def user_details():
    user_id = request.args.get("id")
    user = fetch_user_by_id(int(user_id))
    print(user)

    if user:
        books = fetch_books()

        user_books = []

        for book in user_books: 
            if book.lend == user.id:
                user_books.append(book)

        return render_template("user_details.html", user=user, books=user_books)

    else:

        return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2025, debug=True)
