from .deck_df import create_simple_probdf

import math
import pandas as pd
from itertools import combinations_with_replacement


"""
# Bust It - side bet calculation
The probability of busting is the same for the dealer no matter how the player plays (I think)

With Bust It you bet that the dealer will bust
- Dealer stands on soft 17
- The Bust It side bet is pushed if player has Blackjack
- Bust with 3 cards pays 1 unit
- Bust with 4 cards pays 2 units
- Bust with 5 cards pays 9 units
- Bust with 6 cards pays 50 units
- Bust with 7 cards pays 100 units
- Bust with 8 or more cards pays 250 units
"""

# right now hand combinations are unequal length, because dealer can stop drawing cards
# it actually depends what cards are drawn first so the order matters

def probability(combi, probdf_simple, deck_length):
    """
    takes a combination of cards and calculates number of permutations
    returns probability of this specific combination of cards
    """
    unique = set(combi)
    
    total_permutations = 0
    
    for card in unique:       
        # number of permutations to get this card as many times as it occurs in combi
        n_permutations = math.perm(probdf_simple.at[card], combi.count(card))
        
        if not total_permutations:
            total_permutations += n_permutations
        else:
            total_permutations *= n_permutations
        
    return total_permutations / math.perm(deck_length, len(combi))


def all_comb(all_combos, card_values, hand1):
    """
    this finds all possible hand combinations of the dealer
    and adds them to the correct list, if the dealer busts or not
    """
    for card in card_values:
        hand = hand1.copy()
        hand.append(card)
        
        # correct for soft values
        if 11 in hand and sum(hand) > 21:
            while sum(hand) > 21 and 11 in hand:
                hand[hand.index(11)] = 1
        
        hand_sum = sum(hand)
        
        # append hand to correct list, else take extra card
        if hand_sum > 21:
            # convert all to string
            hand = [str(i) for i in hand]
            
            # change all A values to 'A'
            while '1' in hand:
                hand[hand.index('1')] = 'A'
            while '11' in hand:
                hand[hand.index('11')] = 'A'
            
            hand_length = len(hand)
            
            if hand_length < 8:
                all_combos[f'busted_{hand_length}'].append(hand)
            else:
                all_combos['busted_8'].append(hand)
                
        elif 17 <= hand_sum <= 21:
            # convert all to string
            hand = [str(i) for i in hand]
            
            # change all A values to 'A'
            while '1' in hand:
                hand[hand.index('1')] = 'A'
            while '11' in hand:
                hand[hand.index('11')] = 'A'
            
            # append combination to correct outcome
            all_combos[f'not_busted_{hand_sum}'].append(hand)

        elif hand_sum < 17:
            all_comb(all_combos, card_values, hand)


def get_all_combinations():
    """find hand combinations for each bust type and non-busts"""
    # values of each card
    card_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    # all (non-)busting hand combinations of dealer
    all_combos = {}
    all_combos['not_busted_17'] = []
    all_combos['not_busted_18'] = []
    all_combos['not_busted_19'] = []
    all_combos['not_busted_20'] = []
    all_combos['not_busted_21'] = []
    all_combos['busted_3'] = []
    all_combos['busted_4'] = []
    all_combos['busted_5'] = []
    all_combos['busted_6'] = []
    all_combos['busted_7'] = []
    all_combos['busted_8'] = []

    # get all dealer's possible hand combinations
    all_comb(all_combos, card_values, [])

    return all_combos


def calculate_ev(probdf):
    """
    calculates the probabilities of each outcome of the bust it side bet
    and then it calculates the expected value of betting on the bust it side bet
    returns expected value
    """
    # copy probdf so it doesn't interfere with other scripts
    probdf = probdf.copy()

    # simple probdf
    probdf_simple = create_simple_probdf(probdf)

    # get all combinations
    all_combos = get_all_combinations()


    # save probabilities of dealer (not) busting with a specific open card
    open_card_prob = {}
    for card in probdf_simple.index:
        open_card_prob[card] = {}
        
        # for each open card add outcomes (prob busted and prob not busted 17 - 21)
        open_card_prob[card]['prob_busted'] = 0
        open_card_prob[card]['prob_not_busted_17'] = 0
        open_card_prob[card]['prob_not_busted_18'] = 0
        open_card_prob[card]['prob_not_busted_19'] = 0
        open_card_prob[card]['prob_not_busted_20'] = 0
        open_card_prob[card]['prob_not_busted_21'] = 0
        open_card_prob[card]['prob_not_busted_BJ'] = 0  # keep this because dealer doesn't check for BJ if open card is 10
        

    # save probabilities of the following outcomes
    prob_combos = {}
    prob_combos['prob_not_busted_17'] = 0
    prob_combos['prob_not_busted_18'] = 0
    prob_combos['prob_not_busted_19'] = 0
    prob_combos['prob_not_busted_20'] = 0
    prob_combos['prob_not_busted_21'] = 0
    prob_combos['prob_not_busted_BJ'] = 0
    prob_combos['prob_busted_3'] = 0
    prob_combos['prob_busted_4'] = 0
    prob_combos['prob_busted_5'] = 0
    prob_combos['prob_busted_6'] = 0
    prob_combos['prob_busted_7'] = 0
    prob_combos['prob_busted_8'] = 0


    # total cards in deck
    deck_length = sum(probdf_simple.loc[:, 'Total_cards'])

    # total probability of dealer getting specific outcome
    for outcome in prob_combos:
        # prob_combos does not have BJ combinations seperate
        if 'BJ' in outcome:
            continue
            
        for combi in all_combos[f'{outcome[5:]}']:
            # probability of this specific combinations
            prob = probability(combi, probdf_simple.loc[:, 'Total_cards'], deck_length)
            
            # keep blackjack probabilities seperate, because dealer checks for BJ if open card is A and not if it is 10
            if combi == ['A', '10']:
                prob_combos['prob_not_busted_BJ'] += prob
                continue
            elif combi == ['10', 'A']:
                prob_combos['prob_not_busted_BJ'] += prob
                open_card_prob[combi[0]]['prob_not_busted_BJ'] += prob
                continue
            
            # add probabilities to the outcomes
            prob_combos[outcome] += prob
            
            if not 'not' in outcome:
                open_card_prob[combi[0]]['prob_busted'] += prob
            else:
                open_card_prob[combi[0]][outcome] += prob
            



    # rescale probabilities to scale of 1 (100%)
    for card in open_card_prob:
        card = open_card_prob[card]
        
        # total prob in card needed for rescaling
        total_prob = 0
        
        # calculate total_prob
        for prob in card:
            total_prob += card[prob]
        
        # rescale
        for prob in card:
            card[prob] /= total_prob
            



    # probabilities needed for either blackjack the game or the bust it side bet
    blackjack_prob = {}
    blackjack_prob['prob_busted'] = 0

    bust_it_prob = {}
    bust_it_prob['prob_not_busted'] = 0

    # split prob_combos
    for outcome in prob_combos:
        if "not_busted" in outcome:
            blackjack_prob[outcome] = prob_combos[outcome]
            bust_it_prob['prob_not_busted'] += prob_combos[outcome]
        else:
            blackjack_prob['prob_busted'] += prob_combos[outcome]
            bust_it_prob[outcome] = prob_combos[outcome]




    # correct bust it probabilities, because blackjack pushes the bust it side bet
    for prob in bust_it_prob:
        bust_it_prob[prob] -= bust_it_prob[prob] * prob_combos['prob_not_busted_BJ']




    # payouts
    busted_3_payout = 1
    busted_4_payout = 2
    busted_5_payout = 9
    busted_6_payout = 50
    busted_7_payout = 100
    busted_8_payout = 250

    # returns
    return_busted_3 = bust_it_prob['prob_busted_3'] * busted_3_payout
    return_busted_4 = bust_it_prob['prob_busted_4'] * busted_4_payout
    return_busted_5 = bust_it_prob['prob_busted_5'] * busted_5_payout
    return_busted_6 = bust_it_prob['prob_busted_6'] * busted_6_payout
    return_busted_7 = bust_it_prob['prob_busted_7'] * busted_7_payout
    return_busted_8 = bust_it_prob['prob_busted_8'] * busted_8_payout 
    return_not_busted = -bust_it_prob['prob_not_busted']

    total_ev = return_busted_3 + return_busted_4 + return_busted_5 + return_busted_6 + return_busted_7 + return_busted_8 + return_not_busted

    return total_ev
