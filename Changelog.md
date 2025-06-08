# Lerchbacher Bücherdatenbank Project Änderungsliste
Lerchbacher book database project changelog

## Commit 003-27-02-2025
### General
- Removed everything concerning users
- Added this Changelog.md file
- Removed the old LCARS Style formating and started the html part from scratch
- Changed the way I comment git commits (now they are COMMITNR-DD-MM-YYYY)
- Added some TODOs in the files for commenting or reorganizing functions
- Removed all print statements that were used for debugging
- I think the initial development of the website is 40% done (remaining: 20% ==> authors functions, 20% ==> search function, 20% ==> Styling)
- The project now includes a README.md file with a overview of the project

### app.py
- The project now includes a app.py file, which contains the main flask application
- In this file, there are the following methods:
    - home, the flask method for the homepage of the site
    - all_books, the flask method for the book list page
    - book_detail, the flask method for the book details page
    - book_edit, the flask method for the book editing page
    - book_deletion, the flask method for the book deletion page
- Currently containing a block comment showing the structure of a book entry in the database

### forms.py
- This is a python file containing form classes, based on the WTF FlaskForm class
- Contains the BookForm and the DeletionForm

### handle_db.py
- Module version 0.0.3
- Updated the copyright statement to the new year number
- Added the import of the date class from the datetime module (used for timestamps)
- Added the Book class for easier access of each books individual fields
- Added the Author class for easier access of each authors individual fields
- Changed some functions to use and return Book objects
- Added the fetch_author_names and fetch_author_ids functions for the authors selection field on the book editing page
- Removed every function concerning users
- Fixed a bug in the delete_author function
- Changed the create_author function, so you can now create authors that have a date of death and authors that don't have one
- Added the following functions
  - fetch_author_by_id
  - fetch_author_by_name
  - fetch_books
  - create_book
  - delete_book
  - edit_book
  - fetch_book_by_id
  - fetch_book_by_title
  - change_lend_state

### database.sqlite
- Removed the users table
- Added some columns to the books table
- Changed the author_id column of the books table to be the author_ids column, which has the BLOB data type
- The books table now has the following fields:
    > Book ID INTEGER PRIMARY KEY\
    Book title STRING NOT NULL\
    Author ID INTEGER\
    book publisher STRING NOT NULL\
    book isbn STRING\
    book edition INTEGER DEFAULT 1\
    book year INTEGER\
    book types BLOB\
    book tags BLOB\
    book room STRING\
    book shelf STRING\
    book lend BOOLEAN\
  
### HTML Files (/templates)
- This folder now contains the following html files:
  - base.html, the layout template
  - index.html, for the homepage page
  - books.html, for the books list page
  - book.html, for the book details page
  - edit_book, for the book editing page
  - delete_book.html, for the book deletion page

### CSS and Image Files (/static)
- This folder now contains the noCover.png file, which is used, when Google Books has no cover for a book

## Commit 004-19-03-2025
### General
- Version 0.0.4 Alpha
- Added support for all author operations
- Added search functions (only tag search does not work yet)
- The project is now 70% complete(remaining: 20% ==> User functions, 10% ==> Styling)
- I chose to add users and logins, etc. to the project, but I haven't started that yet
- The main functions are now usable, the database is ready to be filled
- Changed the book types to be selected from a predefined list (It was very complex to change that, dad!)
- I'm too lazy to document the rest of the changes. Future me(or someone else), go look at the change history of git!

## Commit 005-27-04-2025
### General
- The repo is now hosted on GitHub (private at the moment)
- I will discontinue this file and use git commit messages instead, because that's what they were made for
- Project status: 70 - 75 % complete (remaining: 20-15% ==> User functions, 10% ==> Styling)
- Added a users list page
- Added a user details page (incomplete, only name is displayed)
