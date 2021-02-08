import math
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


def get_all_combinations():
    """this part finds all card combinations that add up to 19, 20, 21"""
    # values of cards in the deck
    card_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    # get all 3 card combinations
    comb = list(combinations_with_replacement(card_values, 3))

    # save the winning combinations here
    hot_3_combos = {}
    hot_3_combos['combos_21'] = []
    hot_3_combos['combos_20'] = []
    hot_3_combos['combos_19'] = []

    # select the right combinations
    for com in comb:
        com = list(com)
            
        # correct for soft values
        if 11 in com and sum(com) > 21:
            while sum(com) > 21 and 11 in com:
                com.remove(11)
                com.append(1)
        
        if sum(com) == 19:
            hot_3_combos['combos_19'].append([str(card) if 1 != card != 11 else 'A' for card in com])
        elif sum(com) == 20:
            hot_3_combos['combos_20'].append([str(card) if 1 != card != 11 else 'A' for card in com])
        elif sum(com) == 21:
            hot_3_combos['combos_21'].append([str(card) if 1 != card != 11 else 'A' for card in com])

    # remove the triple 7 combination
    hot_3_combos['combos_21'].remove(['7', '7', '7'])

    return hot_3_combos


def calculate_ev(Deckdf):
    """
    calculates the probabilities of each outcome for the hot 3 side bet
    and then it calculates the expected value of betting on the hot 3 side bet
    returns expected value
    """
    # copy simple probdf so it doesn't interfere with other scripts
    simple_probdf = Deckdf.probdf_simple.copy()
    
    # get all combinations
    hot_3_combos = get_all_combinations()


    # number of combinations to get triple 7
    simple_probdf['Triple_7'] = 0
    simple_probdf.loc['7', 'Triple_7'] = math.comb(simple_probdf.at['7', 'Total_cards'], 3)


    # number of combinations to get 21
    simple_probdf['Total_21'] = 0
    for combi in hot_3_combos['combos_21']:
        total_ncr = 0
        
        for card in set(combi):
            if not total_ncr:
                total_ncr += math.comb(simple_probdf.at[card, 'Total_cards'], combi.count(card))
            else:
                total_ncr *= math.comb(simple_probdf.at[card, 'Total_cards'], combi.count(card))
        
        simple_probdf['Total_21'] += total_ncr / len(simple_probdf.index)

    # number of combinations to get a suited 21
    simple_probdf['Suited_21'] = 0
    for combi in hot_3_combos['combos_21']:
        for suit in Deckdf.suits:
            total_ncr = 0
            
            for card in set(combi):
                if not total_ncr:
                    total_ncr += math.comb(simple_probdf.at[card, suit], combi.count(card))
                else:
                    total_ncr *= math.comb(simple_probdf.at[card, suit], combi.count(card))
        
            simple_probdf['Suited_21'] += total_ncr / len(simple_probdf.index)

    # number of combinations to get an unsuited 21    
    simple_probdf['Unsuited_21'] = simple_probdf['Total_21'] - simple_probdf['Suited_21']


    # number of combinations to get a 20
    simple_probdf['All_20'] = 0
    for combi in hot_3_combos['combos_20']:
        total_ncr = 0
        
        for card in set(combi):
            if not total_ncr:
                total_ncr += math.comb(simple_probdf.at[card, 'Total_cards'], combi.count(card))
            else:
                total_ncr *= math.comb(simple_probdf.at[card, 'Total_cards'], combi.count(card))
        
        simple_probdf['All_20'] += total_ncr / len(simple_probdf.index)
            

    # number of combinations to get 19
    simple_probdf['All_19'] = 0
    for combi in hot_3_combos['combos_19']:
        total_ncr = 0
        
        for card in set(combi):
            if not total_ncr:
                total_ncr += math.comb(simple_probdf.at[card, 'Total_cards'], combi.count(card))
            else:
                total_ncr *= math.comb(simple_probdf.at[card, 'Total_cards'], combi.count(card))
        
        simple_probdf['All_19'] += total_ncr / len(simple_probdf.index)



    # total 3 card combinations
    total_cards = sum(simple_probdf.loc[:, 'Total_cards'])
    total_combinations = math.comb(total_cards, 3)

    # probabilities of each
    prob_triple_7 = sum(simple_probdf['Triple_7']) / total_combinations
    prob_suited_21 = sum(simple_probdf['Suited_21']) / total_combinations
    prob_unsuited_21 = sum(simple_probdf['Unsuited_21']) / total_combinations
    prob_all_20 = sum(simple_probdf['All_20']) / total_combinations
    prob_all_19 = sum(simple_probdf['All_19']) / total_combinations
    prob_losing_combos = 1 - prob_triple_7 - prob_suited_21 - prob_unsuited_21 - prob_all_20 - prob_all_19


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

    return total_ev
