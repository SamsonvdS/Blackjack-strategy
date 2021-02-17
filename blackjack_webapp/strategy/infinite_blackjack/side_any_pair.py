import math
import pandas as pd
import numpy as np


"""
# Any Pair - side bet calculation

The goal is to receive a pair in the first two cards that you are dealt
- Shoe consists of eight decks
- A suited (perfect) pair pays 25 units
- An unsuited pair pays 8 units
"""


def kelly(bet_percentage, prob_dict, payout_dict):
    """maximizes function for kelly criterion"""
    return prob_dict['prob_losing_pair'] * math.log(1 - bet_percentage) + \
            prob_dict['prob_unsuited_pair'] * math.log(1 + payout_dict['unsuited_pair_payout'] * bet_percentage) + \
            prob_dict['prob_suited_pair'] * math.log(1 + payout_dict['suited_pair_payout'] * bet_percentage) 


def optimize_kelly(prob_dict, payout_dict, lower=0, upper=1):
        """
        finds optimal kelly
        basically acts like quicksort sorting algorithm
        with 9 decimals it is accurate enough for a €100.000.000 bankroll
        returns lower boundary of the range of the optimization
        """
        # precision of optimization
        decimals = 9
        increments = float(f'1e-0{decimals - 1}')
        
        # maximize
        while (upper - lower) > increments:
            # get two values in middle of range
            start = round((upper - lower) / 2 + lower, decimals)
            start_plus_one = start + increments
            
            if kelly(start, prob_dict, payout_dict) >= kelly(start_plus_one, prob_dict, payout_dict):
                upper = round(start, decimals)
            else:
                lower = round(start_plus_one, decimals)
            
        return lower


def calculate_ev(Deckdf):
    """
    calculates the probabilities of each outcome for the any pair side bet
    and then it calculates the expected value of betting on the any pair side bet
    returns expected value
    """
    # copy probdf so it doesn't interfere with other scripts
    probdf = Deckdf.probdf.copy()

    # make sure function can do vectorized operations
    nCr = np.vectorize(math.comb)


    # number of possible winning pair combinations
    probdf.loc[:, 'All_winning_pairs'] = nCr(probdf['Total_cards'], 2)

    # calculate number of suited pair combinations
    probdf['Suited_pairs'] = 0
    for suit in Deckdf.suits:
        probdf.loc[:, 'Suited_pairs'] += nCr(probdf.loc[:, suit], 2)

    # calculate unsuited pairs
    probdf['Unsuited_pairs'] = probdf.All_winning_pairs - probdf.Suited_pairs



    # total cards in deck and total 2 card combinations
    total_cards = sum(probdf.Total_cards)
    total_combinations = math.comb(total_cards, 2)

    prob_suited_pair = sum(probdf.Suited_pairs) / total_combinations
    prob_unsuited_pair = sum(probdf.Unsuited_pairs) / total_combinations
    prob_losing_pair = 1 - prob_suited_pair - prob_unsuited_pair


    unsuited_pair_payout = 8
    suited_pair_payout = 25

    return_suited_pair = prob_suited_pair * suited_pair_payout
    return_unsuited_pair = prob_unsuited_pair * unsuited_pair_payout
    return_losing_pair = -prob_losing_pair

    total_ev = return_suited_pair + return_unsuited_pair + return_losing_pair


    # save probabilities and payouts
    prob_dict = {
        'prob_losing_pair': prob_losing_pair,
        'prob_unsuited_pair': prob_unsuited_pair,
        'prob_suited_pair': prob_suited_pair,
    }
    payout_dict = {
        'unsuited_pair_payout': unsuited_pair_payout,
        'suited_pair_payout': suited_pair_payout,
    }

    # find optimal bet percentage
    optimal_bet_percentage = optimize_kelly(prob_dict, payout_dict)

    return total_ev, optimal_bet_percentage
