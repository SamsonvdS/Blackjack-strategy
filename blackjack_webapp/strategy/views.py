from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Card_Image
from .helpers import order_cards
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
    # get order lists of cards for each suit
    hearts, diamonds, spades, clubs = order_cards()
   
    return render(request, 'infinite_bj.html', {
        'hearts': hearts,
        'diamonds': diamonds,
        'spades': spades,
        'clubs': clubs,
    })















