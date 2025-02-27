#
# app.py
# ----------
# Book database project
# (c) Lars Lerchbacher 2025
#


from handle_db import *
from flask import *
import requests
from flask_bootstrap import Bootstrap5

from flask_wtf import CSRFProtect
import secrets
from forms import *

app = Flask("Lerchbacher Bücherdatenbank")
foo = secrets.token_urlsafe(16)
app.secret_key = foo
app.config["SECRET_KEY"] = foo

bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)
csrf.init_app(app)


@app.route("/")
def home():
    # Fetches the 12 last added books from the database
    books = fetch_books()[-12:]

    # Creates a new empty list to store all the covers for those books
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

    # Returns the rendered webpage with all needed data to the user's browser
    return render_template("index.html", books=books, covers=covers)


@app.route("/books")
def all_books():
    books = fetch_books()

    # Creates a new empty list to store all the covers for those books
    covers = []

    # Iterates through all books in the books list
    for book in books:

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
    
    return render_template("book.html", book=book, cover=cover, authors=authors, link=link, types=book.types, tags=book.tags, isbn=str(book.isbn))


# TODO: Restructure and improve book_edit function
# TODO: Comment book_edit function
@app.route("/books/edit", methods=['GET', 'POST'])
@csrf.exempt
def book_edit():
    form = BookForm()
    if request.method == 'GET':
        form.authors.choices = [(str(author.id), author.name) for author in fetch_authors()]
        if request.args.get('id'):
            book_id = request.args.get('id')
            book = fetch_book_by_id(book_id)
            form.title.data = book.title
            form.authors.data = book.author_ids
            form.publisher.data = book.publisher
            form.isbn.data = book.isbn
            form.edition.data = book.edition
            form.year.data = book.year
            form.types.data = str(book.types).replace('[', '').replace(']', '').replace("'", '').replace(',', ';')
            form.tags.data = str(book.tags).replace('[', '').replace(']', '').replace("'", '').replace(',', ';')
            form.room.data = book.room
            form.shelf.data = book.shelf
            form.lend.data = book.lend
            form.id.data = book.id

        return render_template("edit_book.html", form=form)
    
    elif request.method == "POST":
        book_id = form.id.data
        book_title = form.title.data
        book_authors = form.authors.data
        book_publisher = form.publisher.data
        book_isbn = form.isbn.data
        book_edition = form.edition.data
        book_year = form.year.data
        book_types = str(form.types.data.replace("; ", ";").split(";"))
        book_tags = str(form.tags.data.replace("; ", ";").split(";"))
        book_room = form.room.data
        book_shelf = form.shelf.data
        book_lend = form.lend.data

        new_book = Book(id=book_id, title=book_title, author_ids=book_authors, publisher=book_publisher, isbn=book_isbn, edition=book_edition, year=book_year,
                        types=book_types, tags=book_tags, room=book_room, shelf=book_shelf, lend=book_lend)

        if form.validate_on_submit():
            if form.id.data:
                if edit_book(book_id, new_book):
                    return redirect(f"/books/details?id={book_id}")
            else:
                if create_book(new_book):
                    created_book = fetch_book_by_title(new_book.title)
                    return redirect(f"/books/details?id={created_book.id}")

                else:
                    form.authors.choices = [(str(author.id), author.name) for author in fetch_authors()]
                    book_id = new_book.id
                    book = fetch_book_by_id(book_id)
                    form.title.data = new_book.title
                    form.authors.data = new_book.author_ids
                    form.publisher.data = new_book.publisher
                    form.isbn.data = new_book.isbn
                    form.edition.data = new_book.edition
                    form.year.data = new_book.year
                    form.types.data = str(new_book.types).replace('[', '').replace(']', '').replace("'", '').replace(',', ';')
                    form.tags.data = str(new_book.tags).replace('[', '').replace(']', '').replace("'", '').replace(',',';')
                    form.room.data = new_book.room
                    form.shelf.data = new_book.shelf
                    form.lend.data = new_book.lend
                    form.id.data = new_book.id

                    message = "Buch konnte nicht geändert/erstellt werden. Bitte prüfen Sie ob die ID korrekt ist/ein Buch mit diesem Namen bereits existiert."

                    return render_template("edit_book.html", form=form, message=message)

        else:
            form.authors.choices = [(str(author.id), author.name) for author in fetch_authors()]
            book_id = new_book.id
            form.title.data = new_book.title
            form.authors.data = new_book.author_ids
            form.publisher.data = new_book.publisher
            form.isbn.data = new_book.isbn
            form.edition.data = new_book.edition
            form.year.data = new_book.year
            form.types.data = str(new_book.types).replace('[', '').replace(']', '').replace("'", '').replace(',', ';')
            form.tags.data = str(new_book.tags).replace('[', '').replace(']', '').replace("'", '').replace(',', ';')
            form.room.data = new_book.room
            form.shelf.data = new_book.shelf
            form.lend.data = new_book.lend
            form.id.data = new_book.id

            message = "Buch konnte nicht geändert/erstellt werden. Bitte prüfen Sie ob die ID korrekt ist/ein Buch mit diesem Namen bereits existiert."

            return render_template("edit_book.html", form=form, message=message)


# TODO: Comment book_deletion function
@app.route("/books/delete", methods=["GET", "POST"])
@csrf.exempt
def book_deletion():
    book_id = request.args.get("id")
    book = fetch_book_by_id(book_id)
    form = DeleteForm()
    if request.method == "GET":
        message = ""
        return render_template("delete_book.html", book=book, form=form, message=message)

    else:
        if form.checkbox.data:
            if delete_book(book_id, form.passphrase.data):
                return redirect("/books")
            else:
                message = "Löschen fehlgeschlagen! Bitte überprüfen Sie den Sicherheitscode!"
                return render_template("delete_book.html", book=book, form=form, message=message)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=2025, debug=True)


# Book table columns:
"""
Book ID INTEGER PRIMARY KEY
Book title STRING NOT NULL
Author ID INTEGER
book publisher STRING NOT NULL
book isbn STRING
book edition INTEGER DEFAULT 1
book year INTEGER
book types BLOB
book tags BLOB
book room STRING
book shelf STRING
book lend BOOLEAN
"""
