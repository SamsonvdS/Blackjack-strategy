#!/usr/bin/env python
# coding: utf-8

# In[172]:


import random
import pandas as pd
import scipy.stats as st


# ---
# # Insurance - calculation
# 
# - The option of insurance is only given if the dealer has an A
# - Insurance pays 2 units

# In[3]:


# all possible card values
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '10', '10', '10', 'A', 
        '2', '3', '4', '5', '6', '7', '8', '9', '10', '10', '10', '10', 'A',
        '2', '3', '4', '5', '6', '7', '8', '9', '10', '10', '10', '10', 'A',
        '2', '3', '4', '5', '6', '7', '8', '9', '10', '10', '10', '10', 'A',]

# create deck
number_of_decks = 8
deck = cards.copy() * number_of_decks
deck_reserve = deck.copy()


# In[4]:


# payout in units
insurance_payout = 2

# probability of BlackJack if dealer has A
prob_10 = deck.count("10") / len(deck)
prob_not_BJ = 1 - prob_10

print("prob_10",  prob_10)
print("prob_not_BJ", prob_not_BJ)
print("--------------------------------------------")

return_10 = prob_10 * insurance_payout
return_not_BJ = -prob_not_BJ
expected_value = return_10 + return_not_BJ

print("expected_value", expected_value)


# In[ ]:


# save simulation data
df = pd.DataFrame()

n_simulations = 15000

# simulate 
for n_cards in range(30, 261, 3): # number of cards to remove from deck
    results2 = []
    
    for i in range(n_simulations):
        deck2 = deck_reserve.copy()

        for v in range(n_cards):
            card2 = random.choice(deck2)
            deck2.remove(card2)
        
        
        # payout in units
        insurance_payout = 2

        # probability of BlackJack if dealer has A
        prob_10 = deck2.count("10") / len(deck2)
        prob_not_BJ = 1 - prob_10

        # expected returns
        return_10 = prob_10 * insurance_payout
        return_not_BJ = -prob_not_BJ
        expected_value = return_10 + return_not_BJ

        

        results2.append(expected_value)
    
    df[str(n_cards)] = results2


df.describe() # this gives description of what your expected return would be


# In[158]:


df.describe()


# In[197]:


# cumulative probability of getting a positive EV bet in an eight deck shoe with penetration of 258 cards (5/8 decks)
cum_prob = 0

for n_cards in df:
    # z-score for EV >= 0
    z_score = abs(df[n_cards].mean() / df[n_cards].std())

    # cumulative probability of z-score * average probability that the dealer gets an A's
    cum_prob += st.norm.cdf(-z_score) * 0.07692307692307687

# correct cumulative probability, because in the simulation steps of 3 are taken
cum_prob *= 3

print("cum_prob", cum_prob)


# In[200]:


# cumulative probability of getting a positive EV bet in an eight deck shoe with penetration of 210 cards (4/8 decks)
cum_prob = 0

for n_cards in df:
    if int(n_cards) <= 210:
        # z-score for EV >= 0
        z_score = abs(df[n_cards].mean() / df[n_cards].std())

        # cumulative probability of z-score * average probability that the dealer gets an A's
        cum_prob += st.norm.cdf(-z_score) * 0.07692307692307687

# correct cumulative probability, because in the simulation steps of 3 are taken
cum_prob *= 3

print("cum_prob", cum_prob)


# In the simulation it can be seen that very often there will be times when the insurance bet is in the player's favour. 
# - On average the player will have a positive EV Insurance bet 1.27 times in eight deck games with a penetration of 258 cards (5/8 decks)
# - On average the player will have a positive EV Insurance bet 0.67 times in eight deck games with a penetration of 210 cards (4/8 decks)
# 

# # End of Insurance - calculation
# ---

# In[157]:


#df.to_csv(r"C:\Users\samso\OneDrive\Python dingen\Probability calculations\Insurance - simulation data.csv")

