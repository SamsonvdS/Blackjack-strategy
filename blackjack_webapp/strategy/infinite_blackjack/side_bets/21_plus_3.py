import copy
import random
import math
import numpy as np
import pandas as pd


def nCr(n, r):
    """calculates number of combinations (without replacement)"""
    if r > n:
        return 0
    
    f = math.factorial
    return int(f(n) / (f(r) * f(n-r)))

# make sure function can do vectorized operations
nCr = np.vectorize(nCr)

"""
# 21+3 - side bet calculation

You win with this side bet if your first two cards and the dealer's open card are a specific combination (so the first three cards).

<b>Payouts of three card combinations:</b>
- Suited Trips pays 100 units (three identical cards (same type and same suit))
- Straight Flush pays 40 units (three cards in sequence (2-10, J, Q, K, A) all in the same suit)
- Three of a Kind pays 30 units (three cards of the same value but different suits)
- Straight pays 10 units (three cards in sequence (2-10, J, Q, K, A) with different suits)
- Flush pays 5 units (three non-sequential cards in the same suit)
"""



# total number of combinations of three the same cards
probdf['Total_three_of_a_kind'] = nCr(probdf.loc[:, suits].sum(axis=1), 3)
        
# number of possible suited trips combinations
probdf['Suited_trips'] = 0
for suit in suits:
    probdf['Suited_trips'] += nCr(probdf.loc[:, suit], 3)
    
# number of possible three of a kinds (non-suited trips) combinations
probdf['Three_of_a_kind'] = probdf['Total_three_of_a_kind'] - probdf['Suited_trips']


# number of possible sequential card combinations
probdf['Total_sequences'] = 0
for sequence in cards_sequences:
    probdf.loc[sequence[0], 'Total_sequences'] += probdf.loc[sequence, 'Total_cards'].product()

# number of possible straight flush combinations
probdf['Straight_flush'] = 0
for sequence in cards_sequences:
    for suit in suits:
        probdf.loc[sequence[0], 'Straight_flush'] += probdf.loc[sequence, suit].product()
          
# number of possible straight combinations
probdf['Straight'] = probdf['Total_sequences'] - probdf['Straight_flush']


# number of possible same suit card combinations
probdf['Total_same_suit'] = 0
for suit in suits:
    probdf['Total_same_suit'] += nCr(probdf.loc[:, suit].sum(), 3) / len(cards) # len(card) to correct combinations for a per card value instead of total

# number of possible flush combinations
probdf['Flush'] = probdf['Total_same_suit'] - probdf['Straight_flush'] - probdf['Suited_trips']




for i in probdf.iloc[:, 4:]:
    print(i, sum(probdf[i]))



# total 3 card combinations
total_cards = sum(probdf.Total_cards)
total_combinations = nCr(total_cards, 3)

# probabilities
prob_suited_trips = sum(probdf.Suited_trips) / total_combinations
prob_straight_flush = sum(probdf.Straight_flush) / total_combinations
prob_three_of_a_kind = sum(probdf.Three_of_a_kind) / total_combinations
prob_straight = sum(probdf.Straight) / total_combinations
prob_flush = sum(probdf.Flush) / total_combinations
prob_losing_combi = 1 - prob_flush - prob_straight - prob_three_of_a_kind - prob_straight_flush - prob_suited_trips
print("prob_suited_trips", prob_suited_trips)
print("prob_straight_flush", prob_straight_flush)
print("prob_three_of_a_kind", prob_three_of_a_kind)
print("prob_straight", prob_straight)
print("prob_flush", prob_flush)
print("prob_losing_combi", prob_losing_combi)
print("-----------------------")

# payouts
suited_trips_payout = 100
straight_flush_payout = 40
three_of_a_kind_payout = 30
straight_payout = 10
flush_payout = 5

# returns
return_suited_trips = prob_suited_trips * suited_trips_payout
return_straight_flush = prob_straight_flush * straight_flush_payout
return_three_of_a_kind = prob_three_of_a_kind * three_of_a_kind_payout
return_straight = prob_straight * straight_payout
return_flush = prob_flush * flush_payout
return_losing_combi = -prob_losing_combi

total_ev = return_suited_trips + return_straight_flush + return_three_of_a_kind + return_straight + return_flush + return_losing_combi
print("total_ev", total_ev)

