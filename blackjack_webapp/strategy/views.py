from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Card_Image
from .one_time_setups import setup_database_images


def setup_things(request):
    """sets up things for properly working website"""
    # make sure that card images are in database
    setup_database_images()

    return HttpResponseRedirect(reverse("index"))


def index(request):
    """things for index page"""

    return render(request, 'index.html', {
        
    })


def infinite_bj(request):
    """things for infinite blackjack page"""
    # order cards this way
    card_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    # get all card image objects
    all_card_images = Card_Image.objects.all()

    # filter card images by suit
    hearts = [card for card in all_card_images if card.suit == "Hearts"]
    diamonds = [card for card in all_card_images if card.suit == "Diamonds"]
    spades = [card for card in all_card_images if card.suit == "Spades"]
    clubs = [card for card in all_card_images if card.suit == "Clubs"]
    
    # sort card images in card_order
    hearts.sort(key=lambda card: card_order.index(card.card))
    diamonds.sort(key=lambda card: card_order.index(card.card))
    spades.sort(key=lambda card: card_order.index(card.card))
    clubs.sort(key=lambda card: card_order.index(card.card))
   
    return render(request, 'infinite_bj.html', {
        'hearts': hearts,
        'diamonds': diamonds,
        'spades': spades,
        'clubs': clubs,
    })
















