"""
This is meant to setup the webapp backend for the first time
- For example store the card images in the database (models.py)
"""
import os
from .models import Card_Image

def setup_database_images():
    """saves card images and data in database"""
    # only run function in no card_image objects
    if Card_Image.objects.all():
        return

    # absolute path to this file's directory
    absolute_path = os.path.dirname(os.path.abspath(__file__))

    # save images data in database
    for file in os.listdir(f"{absolute_path}/static/cards_jpgs"):
        # name part of the filename 10S.jpg -> 10S
        name = file[:-4]

        # save image data in database
        card_image = Card_Image.objects.create(
            image = file,
            card = name[:-1],
            suit = name[-1],
        )
        




