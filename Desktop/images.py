#
# Desktop/images.py
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
import logging
import os
import requests
from PIL import Image
import threading


IMAGE_SIZE = 175


def update_image(book):
    """Function that checks for a manually added cover for a book and downloads one from openlibrary if there is none"""

    app_context.logger.info(f"Looking for a cover for the book {book.title} (ID: {book.id})")
    filename = get_image_src(book)

    # Check for a manually added cover
    if filename != "./img/noCover.png":            
        app_context.logger.info("Existing found")

    # If none was found, download one
    else:
        # Start the download in the background
        thread = threading.Thread(target=download_cover, args=(book,))
        thread.start()


def download_cover(book):
    """Function that downloads the cover of a book if available"""
    app_context.logger.info("Downloading cover...")
    try:
        response = requests.get(f"https://covers.openlibrary.org/b/isbn/{book.isbn}-L.jpg")

        # If the request got redirected (cover did exist)
        if len(response.history) > 1:
            file = open(f"./img/{book.id}.jpg", mode="wb+")
            file.write(response.content)
            file.close()
            app_context.logger.info("Successfully downloaded cover!")
            app_context.mainWindow.update()

        # Cover did not exist
        else:
            app_context.logger.info("Could not download cover (does not exist)")

    # An error occured
    except Exception as e:
        app_context.logger.info("Could not download cover")
        app_context.logger.error(e)


def get_image(book):
    """Function that gets the cover belonging to a book"""
    # Get the filename of the book cover
    filename = get_image_src(book)

    # Open it as an image
    image = Image.open(filename)

    # Rescale it to fit the maximum image heigth
    image = rescale_image(image)

    return image


def rescale_image(image: Image) -> Image:
    # Rescale the image to fit the maximum image heigth
    w, h = image.size
    if h != IMAGE_SIZE:
        ratio = IMAGE_SIZE / h
        new_size = (int(w * ratio), IMAGE_SIZE)
        image = image.resize(new_size, Image.BILINEAR)

    return image


def get_image_src(book):
    """Function that gets the path to the cover belonging to a book"""
    path = os.path.join(os.getcwd(), 'img', f'{book.id}.jpg')

    # Check if there is a cover for the book
    if os.path.exists(path):
        filename = str(path)

    # else use the noCover.png file
    else:
        filename = "./img/noCover.png"

    return filename

