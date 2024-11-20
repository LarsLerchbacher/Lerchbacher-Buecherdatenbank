#
# handle_db.py
# ----------
# Book database Project
# (c)2024 Lars Lerchbacher
#

#
# Importing all needed modules, packages and libraries
#
# Imports:
# sqlite3 for the database handling and operations
#
from sqlite3 import *


#
# Defines all constants for the project
#
# Constants:
#   DATABASE - is used to store the filename for the database file
#   SECURITY_KEY - stores the security key that is used to authenticate an admin when deleting something
#   MODULE_VERSION - indicates the current version of the file
#
DATABASE = "database.sqlite"
SECURITY_KEY = "Alpha Delta Omikron 37 45 Blau"
MODULE_VERSION = "0.0.1"


#
# Function prepare_db
#
# Use: Establishes a connection with the Database and creates a Cursor
#
# Returns: The db Object which is the Database Connection and the cur Object which is the Cursor
#
# Parameters: None
#
def prepare_db():
    db = connect(DATABASE)
    cur = db.cursor()
    return db, cur


#
# Function fetch_users
#
# Use: Gets all users stored in the database
#
# Returns: A list of all users stored in the database file
#
# Parameters: None
#
def fetch_users():
    db, cur = prepare_db()
    users = cur.execute("SELECT * FROM users;").fetchall()
    cur.close()
    db.close()
    return users


#
# Function does_user_exist
#
# Use: Checks if there is already an existing user with the provided name
#
# Returns: A boolean that indicates if there is already a user with the provided name
#
# Parameters: name - The name that should be checked
#
def does_user_exist(name):
    users = fetch_users()
    is_existent = False
    for user in users:
        if user[1] == name:
            is_existent = True
            break
    return is_existent


#
# Function create_user
#
# Use: Creates a new user if there isn´t already one with the provided name
#
# Returns: a boolean that indicates if a new user with the given credentials was created
#
# Parameters:
#   name - The username that the new use should have
#   email - The email that the new user should have registered
#   pw_hash - The hash of the inputted password to check if the user enters the correct pw upon login.
#
def create_user(name, email, pw_hash):
    if not does_user_exist(name):
        db, cur = prepare_db()
        cur.execute(f"INSERT INTO USERS (user_name, user_email, pw_hash) VALUES ('{name}', '{email}', '{pw_hash}');")
        db.commit()
        cur.close()
        db.close()
        return True
    else:
        return False


#
# Function check_user_credentials
#
# Use: Checks if the hash of the inputted password and the stored password hash of the user with the provided
# name match. This is used for login
#
# Returns: True if the user is existent and the stored hash and the provided hash match, otherwise it will return False
#
# Parameters:
#   name - The name of the user trying to authenticate
#   pw_hash - the hash of the inputted password which is compared to the stored hash of the user with the given name.
#
def check_user_credentials(name, pw_hash):
    if does_user_exist(name):
        db, cur = prepare_db()
        user = cur.execute(f"SELECT * FROM users WHERE user_name == '{name}';").fetchone()
        cur.close()
        db.close()
        if pw_hash == user[3]:
            return True
        else:
            return False
    else:
        return False


#
# Function delete_user
#
# Use: Deletes the user with the provided name if the provided security key matches the predefined one
#
# Returns:
#   True, if the security key if correct
#   False, if the key is incorrect
#
# Parameters:
#   name - the name of the user to be deleted
#   security_key -  the security key that was entered. It is compared to the predefined one
#
def delete_user(name, security_key):
    if security_key == SECURITY_KEY:
        db, cur = prepare_db()
        cur.execute(f"DELETE * FROM users WHERE user_name == '{name}';")
        cur.close()
        db.close()
        return True
    else:
        return False


#
# Function change_user_details
#
# Use: Changes the name and/or the password of the user with the provided name
#
# Returns:
#   True if the operation was successful
#   False if the operation was unsuccessful due to wrong pw or the user to edit doesn't exist or the new pws don´t match
#
# Parameters:
#   name - the name of the user to edit
#   new_name -  the new name the user should have set as the username
#   new_email -  the new email to set for the user
#   pw_hash -  the hash of the inputted password, used to authorize the action
#   new_pw_hash - the hash of the new password to be set
#
def change_user_details(name, new_name, new_email, pw_hash, new_pw_hash, confirm_new_pw_hash):
    if confirm_new_pw_hash == new_pw_hash:
        if does_user_exist(name):
            db, cur = prepare_db()
            user = cur.execute(f"SELECT * FROM users WHERE user_name == '{name}';").fetchone()
            if pw_hash == user[3]:
                cur.execute(f"""
                UPDATE users
                SET user_name = '{new_name}', user_email = '{new_email}', pw_hash = '{new_pw_hash}'
                WHERE user_name == '{name}';
                """)
                db.commit()
                cur.close()
                db.close()
                return True
            else:
                return False
        else:
            return False
    else:
        return False


#
# Function fetch_authors
#
# Use: Gets all authors stored in the database
#
# Returns: A list of all authors stored in the database file
#
# Parameters: None
#
def fetch_authors():
    db, cur = prepare_db()
    authors = cur.execute("SELECT * FROM authors;").fetchall()
    cur.close()
    db.close()
    return authors


#
# Function does_author_exist
#
# Use: Checks if there is already an existing author with the provided name
#
# Returns: A boolean that indicates if there is already an author with the provided name
#
# Parameters: name - The name that should be checked
#
def does_author_exist(name):
    authors = fetch_users()
    is_existent = False
    for author in authors:
        if author[1] == name:
            is_existent = True
            break
    return is_existent


#
# Function create_author
#
# Use: Creates a new author with the give parameters
#
# Returns: True if the author was created, otherwise False
#
# Parameters:
#   name - the name the new author should have
#   has_nobel_price - a boolean that indicates if the author has a Nobel Prize
#   country - the country that the author is from
#   date_of_birth - the date of birth of the new author
#   date_of_death - the date when the author passed away or none if he/she is still alive
#
def create_author(name, has_nobel_prize, country, date_of_birth, date_of_death=None):
    if not does_author_exist(name):
        db, cur = prepare_db()
        cur.execute(f"""INSERT INTO authors (author_name, has_nobel_prize, author_country, date_of_birth, date_of_death) 
        VALUES ('{name}', '{has_nobel_prize}', '{country}', {date_of_birth}, {date_of_death});""")
        db.commit()
        cur.close()
        db.close()
        return True
    else:
        return False


#
# Main programm loop
# Is executed when the module is run as a standalone python script
# Contains some information to be printed and is used for testing functions
#
if __name__ == "__main__":
    print("-------------------------------------------")
    print("Executing file 'handle_db.py'")
    print("This file is executed as the main process")
    print(f"Module version {MODULE_VERSION}")
    print("-------------------------------------------")
