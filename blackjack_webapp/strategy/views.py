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
    ev_hot_3, ev_21_plus_3, ev_any_pair, ev_bust_it = calculate_side_bets(deckdf)

    # turn dataframe into dictionary with lists per suit
    probdf_dict = deckdf.probdf.to_dict('list')

    # get order lists of cards for each suit
    hearts, diamonds, spades, clubs = order_cards()
  
    return render(request, 'infinite_blackjack.html', {
        'hearts': zip(hearts, probdf_dict['Hearts']),
        'diamonds': zip(diamonds, probdf_dict['Diamonds']),
        'spades': zip(spades, probdf_dict['Spades']),
        'clubs': zip(clubs, probdf_dict['Clubs']),
        'ev_insurance': f'{ev_insurance:.4f}',
        'ev_hot_3': f'{ev_hot_3:.4f}',
        'ev_21_plus_3': f'{ev_21_plus_3:.4f}',
        'ev_any_pair': f'{ev_any_pair:.4f}',
        'ev_bust_it': f'{ev_bust_it:.4f}',
    })


def infinite_blackjack_update(request):
    """updates the infinite blackjack page"""
    print("\n hoi"*5)

    # update the probdf
    deckdf.update_prob_df(clubs, diamonds, hearts, spades)

    # calculate decisions and ev for bets
    hand_decision = how_to_play_hand(deckdf, dealer_hand, player_hand)
    ev_insurance = calculate_insurance(deckdf)
    ev_side_bets = calculate_side_bets(deckdf)


    return render(request, 'infinite_blackjack.html', {
        'hearts': hearts,
        'diamonds': diamonds,
        'spades': spades,
        'clubs': clubs,
    })




def infinite_calculate_hand(request):
    """
    calculates the action that the player should take
    returns json object
    """
    # convert json ascii string to dictionary
    js_data = ast.literal_eval(request.body.decode('UTF-8'))
    
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
    hand_decision = how_to_play_hand(deckdf, dealer_hand, player_hand)
    
    # turn data into json
    json_data = json.dumps({
        'hand_decision': hand_decision[0],
        'true_count': hand_decision[1],
        'ev_insurance': ev_insurance,
    })
    
    return HttpResponse(json_data)


def infinite_new_round(request):
    """
    calculates ev of all side bets
    returns json object
    """
    print(ast.literal_eval(request.body.decode('UTF-8')))
    # convert json ascii string to dictionary
    js_data = ast.literal_eval(request.body.decode('UTF-8'))
    
    # calculate ev for bets
    ev_insurance = calculate_insurance(deckdf)
    ev_hot_3, ev_21_plus_3, ev_any_pair, ev_bust_it = calculate_side_bets(deckdf)


    suits = ['hearts', 'diamonds', 'spades', 'clubs']
    
    dictt = {suit:[str(card.image) for card in card_type] for suit in suits for card_type in order_cards()}
    
    return HttpResponse(json.dumps(dictt))


def infinite_new_shoe(request):
    """
    resets everything and recalculates ev of side bets
    returns json object
    """
    print(ast.literal_eval(request.body.decode('UTF-8')))
    # convert json ascii string to dictionary
    js_data = ast.literal_eval(request.body.decode('UTF-8'))
    
    # calculate ev for bets
    ev_insurance = calculate_insurance(deckdf)
    ev_hot_3, ev_21_plus_3, ev_any_pair, ev_bust_it = calculate_side_bets(deckdf)


    suits = ['hearts', 'diamonds', 'spades', 'clubs']
    
    dictt = {suit:[str(card.image) for card in card_type] for suit in suits for card_type in order_cards()}
    
    return HttpResponse(json.dumps(dictt))
















