# general imports
import pandas as pd
import numpy as np
import json
import ast  

# django imports
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# main workframe imports
from .models import Card_Image
from .helpers import order_cards, how_to_play_hand, calculate_insurance, calculate_side_bets
from .one_time_setups import setup_database_images
from .infinite_blackjack.deck_df import Deckdf



"""
things that only need to be done once at server start
"""
# create first probdf
deckdf = Deckdf(number_of_decks=8)

# make sure that card images are in database
setup_database_images()




def index(request):
    """things for index page"""

    return render(request, 'index.html', {
        
    })


def infinite_blackjack(request):
    """for first load of infinite blackjack page"""
    # calculate ev for bets
    ev_insurance = calculate_insurance(deckdf)
    side_bets = calculate_side_bets(deckdf)

    ev_hot_3, ev_21_plus_3, ev_any_pair, ev_bust_it = side_bets[0]
    kelly_pct_hot_3, kelly_pct_21_plus_3, kelly_pct_any_pair, kelly_pct_bust_it = side_bets[1]

    # turn dataframe into dictionary with lists per suit
    probdf_dict = deckdf.probdf.to_dict('list')

    # get order lists of cards for each suit
    hearts, diamonds, spades, clubs = order_cards()
  
    return render(request, 'infinite_blackjack.html', {
        'number_of_decks': deckdf.number_of_decks,
        'hearts': zip(hearts, probdf_dict['Hearts']),
        'diamonds': zip(diamonds, probdf_dict['Diamonds']),
        'spades': zip(spades, probdf_dict['Spades']),
        'clubs': zip(clubs, probdf_dict['Clubs']),
        'ev_insurance': f'{ev_insurance:.4f}',
        'ev_hot_3': f'{ev_hot_3:.4f}',
        'ev_21_plus_3': f'{ev_21_plus_3:.4f}',
        'ev_any_pair': f'{ev_any_pair:.4f}',
        'ev_bust_it': f'{ev_bust_it:.4f}',
        'kelly_pct_hot_3': kelly_pct_hot_3,
        'kelly_pct_21_plus_3': kelly_pct_21_plus_3,
        'kelly_pct_any_pair': kelly_pct_any_pair,
        'kelly_pct_bust_it': kelly_pct_bust_it,
    })




"""
--------------------------------------------------------------
views for API
--------------------------------------------------------------
"""


def infinite_calculate_hand(request):
    """
    calculates the action that the player should take
    returns json object
    """
    # convert json ascii string to dictionary
    js_data = ast.literal_eval(request.body.decode('UTF-8'))
    
    # get bankroll value
    bankroll = int(js_data['bankroll'])

    # change numbers from string to int
    Clubs = np.array(js_data['Clubs'], dtype=np.int64)
    Diamonds = np.array(js_data['Diamonds'], dtype=np.int64)
    Hearts = np.array(js_data['Hearts'], dtype=np.int64)
    Spades = np.array(js_data['Spades'], dtype=np.int64)

    # update deckdf
    deckdf.update_prob_df(Clubs, Diamonds, Hearts, Spades)
    
    # cards worth 10
    tens = ['J', 'Q', 'K']

    # clean cards in hands and conver J, Q, K to 10 
    dealer_hand = [card[:-1] if card[:-1] not in tens else '10' for card in js_data['dealer_hand']]
    player_hand = [card[:-1] if card[:-1] not in tens else '10' for card in js_data['player_hand']]

    # calculate player's decision and ev of insurance
    ev_insurance = calculate_insurance(deckdf)
    hand_decision, true_count, kelly_pct = how_to_play_hand(deckdf, dealer_hand, player_hand)
    
    # fractional kelly
    fraction_kelly = 0.8

    # turn data into json
    json_data = json.dumps({
        'hand_decision': hand_decision,
        'true_count': f'{true_count:.1f}',
        'insurance': f'{ev_insurance:.4f}',
        'kelly_pct_hand_decision': kelly_pct,
        'optimal_bet_hand_decision':round(bankroll * kelly_pct * fraction_kelly, 2),
    })
    return HttpResponse(json_data)


def infinite_new_round(request):
    """
    calculates ev of all side bets
    returns json object
    """
    # convert json ascii string to dictionary
    js_data = ast.literal_eval(request.body.decode('UTF-8'))
    
    # get bankroll value
    bankroll = int(js_data['bankroll'])

    # change numbers from string to int
    Clubs = np.array(js_data['Clubs'], dtype=np.int64)
    Diamonds = np.array(js_data['Diamonds'], dtype=np.int64)
    Hearts = np.array(js_data['Hearts'], dtype=np.int64)
    Spades = np.array(js_data['Spades'], dtype=np.int64)

    # update deckdf
    deckdf.update_prob_df(Clubs, Diamonds, Hearts, Spades)

    # calculate ev for bets
    ev_insurance = calculate_insurance(deckdf)
    side_bets = calculate_side_bets(deckdf)

    # get expected values and optimal bet percentages (kelly criterion)
    ev_hot_3, ev_21_plus_3, ev_any_pair, ev_bust_it = side_bets[0]
    kelly_pct_hot_3, kelly_pct_21_plus_3, kelly_pct_any_pair, kelly_pct_bust_it = side_bets[1]

    # fractional kelly
    fraction_kelly = 0.8

    # turn data into json
    json_data = json.dumps({
        'hot_3': f'{ev_hot_3:.4f}',
        '21_plus_3': f'{ev_21_plus_3:.4f}',
        'any_pair': f'{ev_any_pair:.4f}',
        'bust_it': f'{ev_bust_it:.4f}',
        'insurance': f'{ev_insurance:.4f}',
        'kelly_pct_hot_3': kelly_pct_hot_3,
        'kelly_pct_21_plus_3': kelly_pct_21_plus_3,
        'kelly_pct_any_pair': kelly_pct_any_pair,
        'kelly_pct_bust_it': kelly_pct_bust_it,
        'optimal_bet_hot_3':round(bankroll * kelly_pct_hot_3 * fraction_kelly, 2),
        'optimal_bet_21_plus_3':round(bankroll * kelly_pct_21_plus_3 * fraction_kelly, 2),
        'optimal_bet_any_pair':round(bankroll * kelly_pct_any_pair * fraction_kelly, 2),
        'optimal_bet_bust_it':round(bankroll * kelly_pct_bust_it * fraction_kelly, 2),
    })
    return HttpResponse(json_data)


def infinite_new_shoe(request):
    """
    resets everything and recalculates ev of side bets
    returns json object
    """
    # convert json ascii string to dictionary
    js_data = ast.literal_eval(request.body.decode('UTF-8'))

    # get bankroll value
    bankroll = int(js_data['bankroll'])

    # reset deckdf
    deckdf.reset_probdf()

    # calculate ev for bets
    ev_insurance = calculate_insurance(deckdf)
    side_bets = calculate_side_bets(deckdf)

    # get expected values and optimal bet percentages (kelly criterion)
    ev_hot_3, ev_21_plus_3, ev_any_pair, ev_bust_it = side_bets[0]
    kelly_pct_hot_3, kelly_pct_21_plus_3, kelly_pct_any_pair, kelly_pct_bust_it = side_bets[1]

    # fractional kelly
    fraction_kelly = 0.8

    # turn data into json
    json_data = json.dumps({
        'hot_3': f'{ev_hot_3:.4f}',
        '21_plus_3': f'{ev_21_plus_3:.4f}',
        'any_pair': f'{ev_any_pair:.4f}',
        'bust_it': f'{ev_bust_it:.4f}',
        'insurance': f'{ev_insurance:.4f}',
        'kelly_pct_hot_3': kelly_pct_hot_3,
        'kelly_pct_21_plus_3': kelly_pct_21_plus_3,
        'kelly_pct_any_pair': kelly_pct_any_pair,
        'kelly_pct_bust_it': kelly_pct_bust_it,
        'optimal_bet_hot_3':round(bankroll * kelly_pct_hot_3 * fraction_kelly, 2),
        'optimal_bet_21_plus_3':round(bankroll * kelly_pct_21_plus_3 * fraction_kelly, 2),
        'optimal_bet_any_pair':round(bankroll * kelly_pct_any_pair * fraction_kelly, 2),
        'optimal_bet_bust_it':round(bankroll * kelly_pct_bust_it * fraction_kelly, 2),
    })
    return HttpResponse(json_data)
















