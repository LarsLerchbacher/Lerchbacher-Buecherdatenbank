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
MODULE_VERSION = "0.0.2"


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

    # Stores the new connection to the database in the db variable
    db = connect(DATABASE)

    # Stores the new cursor in the cur variable
    cur = db.cursor()

    # Returns the db and cur variables
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

    # Initializes a connection to the database
    db, cur = prepare_db()

    # Fetches all the users from the database
    users = cur.execute("SELECT * FROM users;").fetchall()

    # Closes the cursor
    cur.close()

    # Closes the db connection
    db.close()

    # Returns the fetched users
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

    # Fetches all users from the db
    users = fetch_users()

    # Creates a variable to store the check result
    is_existent = False

    # Loops through all users in the db
    for user in users:

        # Checks if the user's name matches the name parameter
        if user[1] == name:

            # Sets the is_existent variable to True
            is_existent = True

            # Breaks out of the loop
            break

    # Returns the check result stored in the is_existent variable
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

    # If there isn't already a user with the provided name
    if not does_user_exist(name):

        # Initializes the db connection
        db, cur = prepare_db()

        # Creates the new user
        cur.execute(f"INSERT INTO USERS (user_name, user_email, pw_hash) VALUES ('{name}', '{email}', '{pw_hash}');")

        # Commits the changes to the db
        db.commit()

        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()

        # Returns True because the user was created
        return True

    # If there is already a user with the provided name
    else:

        # False is returned because the operation was not executed
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

    # If the user is existent
    if does_user_exist(name):

        # Initializes the db connection
        db, cur = prepare_db()

        # Fetches a user with the provided name
        user = cur.execute(f"SELECT * FROM users WHERE user_name == '{name}';").fetchone()

        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()

        # If the pw hashes match
        if pw_hash == user[3]:

            # Returns True because the user was authenticated
            return True

        # If they don't match
        else:

            # Returns False because the wrong pw was entered
            return False

    # If the user doesn't exist
    else:

        # Returns False, because you can't log in as a not existent user
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

    # If the provided security key matches the predefined one
    if security_key == SECURITY_KEY:

        # Initializes the db connection
        db, cur = prepare_db()

        # Deletes the user
        cur.execute(f"DELETE * FROM users WHERE user_name == '{name}';")

        # Commits the changes to the db
        db.commit()

        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()

        # Returns True, because the user was successfully deleted
        return True

    # If the security keys don't match
    else:

        # Returns False, because the action wasn't authenticated
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

    # If the new pw hash and the new pw confirmation hash are matching
    if confirm_new_pw_hash == new_pw_hash:

        # If the user to edit exists
        if does_user_exist(name):

            # Initializes the db connection
            db, cur = prepare_db()

            # Checks if the provided pw hash is correct
            if check_user_credentials(name, pw_hash):

                # Updates the users details
                cur.execute(f"""
                UPDATE users
                SET user_name = '{new_name}', user_email = '{new_email}', pw_hash = '{new_pw_hash}'
                WHERE user_name == '{name}';
                """)

                # Commits the changes to the db
                db.commit()

                # Closes the cursor
                cur.close()

                # Closes the db connection
                db.close()

                # Returns True because the edit was successful
                return True

            # If the pw hashes don't match
            else:

                # Returns False because the action wasn't authenticated
                return False

        # If the user doesn't exist
        else:

            # Returns False because you can't edit an entry that doesn't exist
            return False

    # If the two new pw hashes don't match
    else:

        # Returns False because one new pw probably has a typo in it
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

    # The db connections is initialized
    db, cur = prepare_db()

    # Fetches all the author from the db
    authors = cur.execute("SELECT * FROM authors;").fetchall()

    # Closes the cursor
    cur.close()

    # Closes the db connection
    db.close()

    # Returns the fetched authors
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

    # Fetches all authors from the db
    authors = fetch_users()

    # Creates the is_existent variable to store the checks result
    is_existent = False

    # Iterates over all authors in the db
    for author in authors:

        # If the authors name and the name parameter match
        if author[1] == name:

            # The is_existent variable is set to True
            is_existent = True

            # Breaks out of the loop
            break

    # Returns if the authors is existent
    return is_existent


#
# Function delete_author
#
# Use: deletes the author with the given name if the security key is correct
#
# Returns: True if it deleted the user, else False
#
# Parameters:
#   name - The name of the author to be deleted
#   security_key - the key which is checked with the saved one to authorize the action
#
def delete_author(name, security_key):

    # If the security key parameter and the predefined one match
    if security_key == SECURITY_KEY:

        # Initializes the db connection
        db, cur = prepare_db()

        # Deletes the author from the db
        cur.execute(f"DELETE * FROM authors WHERE author_name == '{name}';")

        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()

        # Returns True because the author was deleted
        return True

    # If the security keys don't match
    else:

        # Returns False, because the action wasn't authenticated
        return False


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

    # If the author doesn't exist
    if not does_author_exist(name):

        # Initializes the db connection
        db, cur = prepare_db()

        # The author is added to the db
        cur.execute(f"""INSERT INTO authors (author_name, has_nobel_prize, author_country, date_of_birth, date_of_death) 
        VALUES ('{name}', '{has_nobel_prize}', '{country}', {date_of_birth}, {date_of_death});""")

        # Commits the changes to the db
        db.commit()

        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()

        # Returns True because the author was created successfully
        return True

    # If the author already exists
    else:

        # Returns False because you mustn't override an existing author to create a new one
        return False


#
# Function edit_author
#
# Use: Edits the details of the author with the provided name
#
# Returns: True if the author was updated or Else if he/she wasn't updated
#
# Parameters:
#   name - the name of the author to edit
#   new_name -  the new name the author should have
#   has_nobel_prize - has the author won any Nobel Prizes
#   country - the country where the author lives
#   date_of_birth - the date when the author was born
#   date_of_death - the date when the author died or None if he/she is still alive
#
def edit_author(name, new_name, has_nobel_prize, country, date_of_birth, date_of_death=None):

    # If the author exists
    if does_author_exist(name):

        # Initializes the db connection
        db, cur = prepare_db()

        # Updates the author's details
        cur.execute(f"""
                    UPDATE authors
                    SET author_name = '{new_name}', has_nobel_prize = {has_nobel_prize}, author_country = '{country}', date_of_birth = {date_of_birth}, date_of_death = {date_of_death}
                    WHERE author_name == '{name}';
                    """)

        # Commits the changes to the db
        db.commit()

        # Closes the cursor
        cur.close()

        # Closes the db connection
        db.close()

        # Returns True because the author was successfully edited
        return True

    # If the author doesn't exist
    else:

        # Returns False, because you can't alter the details of a not existing author
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
