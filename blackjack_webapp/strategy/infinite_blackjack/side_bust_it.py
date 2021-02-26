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


def kelly(bet_percentage, prob_dict, payout_dict):
    """maximizes function for kelly criterion"""
    return prob_dict['prob_not_busted'] * math.log(1 - bet_percentage) + \
            prob_dict['prob_busted_3'] * math.log(1 + payout_dict['busted_3_payout'] * bet_percentage) + \
            prob_dict['prob_busted_4'] * math.log(1 + payout_dict['busted_4_payout'] * bet_percentage) + \
            prob_dict['prob_busted_5'] * math.log(1 + payout_dict['busted_5_payout'] * bet_percentage) + \
            prob_dict['prob_busted_6'] * math.log(1 + payout_dict['busted_6_payout'] * bet_percentage) + \
            prob_dict['prob_busted_7'] * math.log(1 + payout_dict['busted_7_payout'] * bet_percentage) + \
            prob_dict['prob_busted_8'] * math.log(1 + payout_dict['busted_8_payout'] * bet_percentage) 


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


def calculate_ev(DealerCombinations):
    """
    calculates and returns expected value of bust it side bet and optimal bet 
    """
    # get probabilities for bust it side bet
    bust_it_prob = DealerCombinations.bust_it_prob
    
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


    # save payouts
    payout_dict = {
        'busted_3_payout': busted_3_payout,
        'busted_4_payout': busted_4_payout,
        'busted_5_payout': busted_5_payout,
        'busted_6_payout': busted_6_payout,
        'busted_7_payout': busted_7_payout,
        'busted_8_payout': busted_8_payout,
    }

    # find optimal bet percentage
    optimal_bet_percentage = optimize_kelly(bust_it_prob, payout_dict)

    return total_ev, optimal_bet_percentage
