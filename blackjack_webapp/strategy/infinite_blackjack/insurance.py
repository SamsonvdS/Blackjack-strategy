import random
import pandas as pd
import scipy.stats as st


"""
# Insurance - calculation

- The option of insurance is only given if the dealer has an A
- Insurance pays 2 units
"""

def calculate_ev(probdf):
    """
    calculates the probability of blackjack if dealer has an A
    and then it calculates the expected value of taking insurance
    returns expected value
    """
    # payout in units
    insurance_payout = 2

    # probability of BlackJack if dealer has A
    prob_10 = probdf_simple.at['10', 'Total_cards'] / sum(probdf_simple.loc[:, 'Total_cards'])
    prob_not_BJ = 1 - prob_10

    return_10 = prob_10 * insurance_payout
    return_not_BJ = -prob_not_BJ
    expected_value = return_10 + return_not_BJ

    return expected_value
