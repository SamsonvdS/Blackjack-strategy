import copy
import random
import math
import numpy as np
import pandas as pd
from itertools import combinations_with_replacement

"""
# Hot 3 - side bet calculation

You win with this side bet if your first two cards and the dealer's open card are a specific combination (so the first three cards).

<b>Payouts of three card combinations:</b>
- Three 7's pays 100 units
- Three same suited cards totalling 21 pays 20 units
- Three unsuited cards totaling 21 pays 4 units
- Three cards totalling 20 pays 2 units
- Three cards totalling 19 pays 1 unit
"""

def nCr(n, r):
    """calculates number of combinations (without replacement)"""
    if r > n:
        return 0
    
    f = math.factorial
    return int(f(n) / (f(r) * f(n-r)))
    
# make sure function can do vectorized operations
nCr = np.vectorize(nCr)



"""this part finds all card combinations that add up to 19, 20, 21"""

# values of cards in the deck
card_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# get all 3 card combinations
comb = list(combinations_with_replacement(card_values, 3))

# save the winning combinations here
combos_21 = []
combos_20 = []
combos_19 = []

# select the right combinations
for com in comb:
    com = list(com)
        
    # correct for soft values
    if 11 in com and sum(com) > 21:
        while sum(com) > 21 and 11 in com:
            com.remove(11)
            com.append(1)
    
    if sum(com) == 19:
        combos_19.append([str(card) if 1 != card != 11 else 'A' for card in com])
    elif sum(com) == 20:
        combos_20.append([str(card) if 1 != card != 11 else 'A' for card in com])
    elif sum(com) == 21:
        combos_21.append([str(card) if 1 != card != 11 else 'A' for card in com])

# remove the triple 7 combination
combos_21.remove(['7', '7', '7'])




# cards in deck
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']
suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']

number_of_decks = 8

# total number of cards of a specific face value of a specific suit at the start of a deck
total_start_cards = number_of_decks


# number of cards in this column for each card
start_cards_column = [total_start_cards for i in range(len(cards))]

# create starting dataframe
probdf = pd.DataFrame({
    'Clubs': start_cards_column,
    'Diamonds': start_cards_column,
    'Hearts': start_cards_column,
    'Spades': start_cards_column,
}, index=cards)

# see 10, J, Q, K as the same
probdf.loc['10', :] *= 4


# sum total cards of a face value
probdf['Total_cards'] = probdf.loc[:, suits].sum(axis=1)




# number of combinations to get triple 7
probdf['Triple_7'] = 0
probdf.loc['7', 'Triple_7'] = nCr(probdf.loc['7', 'Total_cards'], 3)


# number of combinations to get 21
probdf['Total_21'] = 0
for combi in combos_21:
    total_ncr = 0
    
    for card in set(combi):
        if not total_ncr:
            total_ncr += nCr(probdf.loc[card, 'Total_cards'], combi.count(card))
        else:
            total_ncr *= nCr(probdf.loc[card, 'Total_cards'], combi.count(card))
    
    probdf['Total_21'] += total_ncr / len(cards)

# number of combinations to get a suited 21
probdf['Suited_21'] = 0
for combi in combos_21:
    for suit in suits:
        total_ncr = 0
        
        for card in set(combi):
            if not total_ncr:
                total_ncr += nCr(probdf.loc[card, suit], combi.count(card))
            else:
                total_ncr *= nCr(probdf.loc[card, suit], combi.count(card))
    
        probdf['Suited_21'] += total_ncr / len(cards)

# number of combinations to get an unsuited 21    
probdf['Unsuited_21'] = probdf['Total_21'] - probdf['Suited_21']


# number of combinations to get a 20
probdf['All_20'] = 0
for combi in combos_20:
    total_ncr = 0
    
    for card in set(combi):
        if not total_ncr:
            total_ncr += nCr(probdf.loc[card, 'Total_cards'], combi.count(card))
        else:
            total_ncr *= nCr(probdf.loc[card, 'Total_cards'], combi.count(card))
    
    probdf['All_20'] += total_ncr / len(cards)
        

# number of combinations to get 19
probdf['All_19'] = 0
for combi in combos_19:
    total_ncr = 0
    
    for card in set(combi):
        if not total_ncr:
            total_ncr += nCr(probdf.loc[card, 'Total_cards'], combi.count(card))
        else:
            total_ncr *= nCr(probdf.loc[card, 'Total_cards'], combi.count(card))
    
    probdf['All_19'] += total_ncr / len(cards)




# total 3 card combinations
total_cards = sum(probdf.Total_cards)
total_combinations = nCr(total_cards, 3)

# probabilities of each
prob_triple_7 = sum(probdf['Triple_7']) / total_combinations
prob_suited_21 = sum(probdf['Suited_21']) / total_combinations
prob_unsuited_21 = sum(probdf['Unsuited_21']) / total_combinations
prob_all_20 = sum(probdf['All_20']) / total_combinations
prob_all_19 = sum(probdf['All_19']) / total_combinations
prob_losing_combos = 1 - prob_triple_7 - prob_suited_21 - prob_unsuited_21 - prob_all_20 - prob_all_19

print("prob_triple_7", prob_triple_7)
print("prob_suited_21", prob_suited_21)
print("prob_unsuited_21", prob_unsuited_21)
print("prob_all_20", prob_all_20)
print("prob_all_19", prob_all_19)
print("prob_losing_combos", prob_losing_combos)
print("---------------------------")

# payouts
triple_7_payout = 100
suited_21_payout = 20
unsuited_21_payout = 4
all_20_payout = 2
all_19_payout = 1

# expected returns
return_triple_7 = prob_triple_7 * triple_7_payout
return_suited_21 = prob_suited_21 * suited_21_payout
return_unsuited_21 = prob_unsuited_21 * unsuited_21_payout
return_all_20 = prob_all_20 * all_20_payout
return_all_19 = prob_all_19 * all_19_payout
return_losing_combos = -prob_losing_combos

total_ev = return_triple_7 + return_suited_21 + return_unsuited_21 + return_all_20 + return_all_19 + return_losing_combos

print("total_ev", total_ev)


