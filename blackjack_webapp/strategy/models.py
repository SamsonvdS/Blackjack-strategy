from django.db import models


class Card_Image(models.Model):
    """This keeps data about card images"""
    image = models.ImageField(upload_to="static/cards_jpg")
    card = models.CharField(max_length=3)
    suit = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.card} of {self.suit}"

