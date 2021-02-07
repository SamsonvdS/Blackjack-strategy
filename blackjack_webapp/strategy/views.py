# general imports
import pandas as pd

# django imports
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# main workframe imports
from .models import Card_Image
from .helpers import order_cards
from .one_time_setups import setup_database_images
from .infinite_blackjack.deck_df import create_prob_df, create_simple_probdf, update_prob_df

# calculation imports
from .infinite_blackjack.blackjack_hands import make_decision
from .infinite_blackjack.insurance import calculate_ev as calculate_ev_insurance
from .infinite_blackjack.side_hot_3 import calculate_ev as calculate_ev_hot_3
from .infinite_blackjack.side_21_plus_3 import calculate_ev as calculate_ev_21_plus_3
from .infinite_blackjack.side_any_pair import calculate_ev as calculate_ev_any_pair
from .infinite_blackjack.side_bust_it import calculate_ev as calculate_ev_bust_it



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
    """for first load of infinite blackjack page"""
    # create first probdf
    probdf = create_prob_df(number_of_decks=8)

    # calculate ev for bets
    ev_insurance = calculate_ev_insurance(probdf)
    ev_hot_3 = calculate_ev_hot_3(probdf)
    ev_21_plus_3 = calculate_ev_21_plus_3(probdf)
    ev_any_pair = calculate_ev_any_pair(probdf)
    ev_bust_it = calculate_ev_bust_it(probdf)
    
    # turn dataframe into dictionary with lists per suit
    prob_dict = probdf.to_dict('list')

    # get order lists of cards for each suit
    hearts, diamonds, spades, clubs = order_cards()

    return render(request, 'infinite_bj.html', {
        'hearts': zip(hearts, prob_dict['Hearts']),
        'diamonds': zip(diamonds, prob_dict['Diamonds']),
        'spades': zip(spades, prob_dict['Spades']),
        'clubs': zip(clubs, prob_dict['Clubs']),
    })


def infinite_bj_update(request):
    """updates the infinite blackjack page"""
    print("\n hoi"*5)
    # calculate decisions and ev
    decision = make_decision(probdf)
    ev_insurance = calculate_ev_insurance(probdf)
    ev_hot_3 = calculate_ev_hot_3(probdf)
    ev_21_plus_3 = calculate_ev_21_plus_3(probdf)
    ev_any_pair = calculate_ev_any_pair(probdf)
    ev_bust_it = calculate_ev_bust_it(probdf)


    return render(request, 'infinite_bj.html', {
        'hearts': hearts,
        'diamonds': diamonds,
        'spades': spades,
        'clubs': clubs,
    })









