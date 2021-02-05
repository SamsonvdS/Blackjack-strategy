#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# # Blackjack - how to play hands calculation

# <i>I simply use the Zen count with full indices from </i>
# 
# The rules are as follows:
# * Eight decks
# * Dealer inmediately takes a hole(closed) card
# * Dealer stands on soft 17
# * Double down on any two cards
# * Split all cards of equal value
# * Maximum of one split
# * If Aces are splitted only one extra card will be dealt to each split ace
# * No double down after split
# * Six card Charlie (you win automatically if you don't bust after taking six cards)
# * Blackjack pays 1.5 units
# * Push when hands tie

# In[2]:


# cards in deck
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']

number_of_decks = 8

# total number of cards of a specific face value of a specific suit at the start of a deck
total_start_cards = number_of_decks


# In[3]:


# number of cards in this column for each card
start_cards_column = [total_start_cards for i in range(len(cards))]

# create starting dataframe
probdf = pd.DataFrame({
    'Clubs': start_cards_column,
    'Diamonds': start_cards_column,
    'Hearts': start_cards_column,
    'Spades': start_cards_column,
}, index=cards)

# sum total cards of a face value
probdf['Total_cards'] = probdf.loc[:, suits].sum(axis=1)


# In[4]:


probdf


# In[5]:


def create_simple_probdf(probdf):
    """creates simplified probdf for bust it side bet, doesn't work with normal probdf"""
    probdf_simple = probdf.loc[:, 'Total_cards'].copy()
    probdf_simple.at['10'] += sum(probdf_simple['J':'K'])
    probdf_simple.drop(['J', 'Q', 'K'], inplace=True)
    return probdf_simple

probdf_simple = create_simple_probdf(probdf)


# In[6]:


possible_hands = ['Hard 2','Hard 3','Hard 4','Hard 5','Hard 6','Hard 7','Hard 8',
                 'Hard 9','Hard 10','Hard 11','Hard 12','Hard 13','Hard 14',
                  'Hard 15','Hard 16','Hard 17','Hard 18','Hard 19','Hard 20',
                  'Hard 21','Soft 12','Soft 13','Soft 14','Soft 15','Soft 16',
                  'Soft 17','Soft 18','Soft 19','Soft 20','Soft 21','2/2','3/3',
                  '4/4','5/5','6/6','7/7','8/8','9/9','10/10','A/A']


# In[11]:


basic_strategy = pd.DataFrame({
    card:'hit' for card in probdf_simple.index
}, index=possible_hands[::-1])


# In[12]:


# fill in the basic strategy chart with six card charlie
basic_strategy.loc['Hard 9', '3':'6'] = 'double/hit'
basic_strategy.loc['Hard 10', :'9'] = 'double/hit'
basic_strategy.loc['Hard 11', :'10'] = 'double/hit'

# hit2/1 is hit if 2/1 cards away from six card charlie, otherwise stand
basic_strategy.loc['Hard 12', '4':'6'] = 'hit2'
basic_strategy.loc['Hard 13', '2'] = 'hit2'
basic_strategy.loc['Hard 13', '3':'6'] = 'hit1'
basic_strategy.loc['Hard 14', '2':'6'] = 'hit1'
basic_strategy.loc['Hard 15', '2':'6'] = 'hit1'
basic_strategy.loc['Hard 16', '2':'3'] = 'hit1'
basic_strategy.loc['Hard 16', '4':'6'] = 'stand'
basic_strategy.loc['Hard 17', '2':'7'] = 'stand'
basic_strategy.loc['Hard 17', '8':'A'] = 'hit1'
basic_strategy.loc['Hard 18', :] = 'stand'
basic_strategy.loc['Hard 19', :] = 'stand'
basic_strategy.loc['Hard 20', :] = 'stand'
basic_strategy.loc['Hard 21', :] = 'stand'

basic_strategy.loc['Soft 13', '6'] = 'double/hit'
basic_strategy.loc['Soft 14', '5':'6'] = 'double/hit'
basic_strategy.loc['Soft 15', '5':'6'] = 'double/hit'
basic_strategy.loc['Soft 16', '4':'6'] = 'double/hit'
basic_strategy.loc['Soft 17', '3':'6'] = 'double/hit'
basic_strategy.loc['Soft 18', ['2', '6']] = 'hit2'
basic_strategy.loc['Soft 18', '7'] = 'hit1'
basic_strategy.loc['Soft 18', '3':'6'] = 'double/hit2'
basic_strategy.loc['Soft 19', :] = 'hit1'
basic_strategy.loc['Soft 19', '10'] = 'hit2'
basic_strategy.loc['Soft 20', :] = 'hit1'
basic_strategy.loc['Soft 21', :] = 'hit1'

# here add pairs
basic_strategy.loc['A/A', :] = 'split'
basic_strategy.loc['10/10', :] = 'stand'
basic_strategy.loc['9/9', :] = 'split'
basic_strategy.loc['9/9', ['7', '10', 'A']] = 'stand'
basic_strategy.loc['8/8', :] = 'split'
basic_strategy.loc['7/7', '2':'7'] = 'split'
basic_strategy.loc['6/6', '3':'6'] = 'split'
basic_strategy.loc['5/5', '2':'9'] = 'double/hit'
basic_strategy.loc['3/3', '4':'7'] = 'split'
basic_strategy.loc['2/2', '5':'7'] = 'split'



# In[45]:


basic_strategy


# In[ ]:





# In[43]:


# adjust basic strategy for some deviations
true_count = 0

if true_count >= 0:
    basic_strategy.at['Hard 16', '10'] = 'stand'

if true_count >= 1:
    basic_strategy.at['Hard 12', '4'] = 'stand'
    basic_strategy.at['Soft 18', '2'] = 'double/hit2' 

if true_count >= 2:
    basic_strategy.at['Hard 9', '2'] = 'double/hit'
    basic_strategy.loc['Soft 19', ['5', '6']] = 'double/hit1'
    basic_strategy.at['Soft 17', '2'] = 'double/hit'
    
if true_count >= 3:
    basic_strategy.at['Hard 12', '3'] = 'stand'
    
if true_count >= 4:
    basic_strategy.at['Hard 8', '6'] = 'double/hit'
    basic_strategy.at['3/3', '3'] = 'split'
    basic_strategy.at['2/2', '3'] = 'split'
    basic_strategy.at['6/6', '2'] = 'split'
    
if true_count >= 5:
    basic_strategy.at['Soft 19', '4'] = 'double/hit1' 
    
if true_count >= 6:
    basic_strategy.at['Hard 15', '10'] = 'stand'
    basic_strategy.at['Hard 12', '2'] = 'stand'
    
if true_count >= 7:
    basic_strategy.at['Soft 19', '3'] = 'double/hit1'
    basic_strategy.at['Hard 9', '7'] = 'double/hit'
    
if true_count >= 8:
    basic_strategy.at['Hard 16', '9'] = 'stand'
    
    


# In[49]:


"""select correct action for player"""

dealer_hand = ['6']
player_hand = ['A', '5']

open_card = dealer_hand[0]

card1 = player_hand[0]
card2 = player_hand[1]


player_hand = [int(card) if card != 'A' else 11 for card in player_hand]


# correct player hand for A's
if 11 in player_hand and sum(player_hand) > 21:
    while sum(player_hand) > 21 and 11 in player_hand:
        player_hand[player_hand.index(11)] = 1

        
# select type of hand
if 11 in player_hand:
    hand_type = 'Soft'
else:
    hand_type = 'Hard'
    
    
# stand at six cards or if player busts
if len(player_hand) == 6 or sum(player_hand) > 21:
    action = 'stand'

# things for first two cards
elif len(player_hand) == 2:
    # if hand is pair
    if card1 == card2:
        action = basic_strategy.loc[f"{card1}/{card2}", open_card]
    else:
        # get action from basic_strategy chart
        action = basic_strategy.loc[f"{hand_type} {sum(player_hand)}", open_card].split('/')[0]
    
else:
    # get action from basic_strategy chart
    action = basic_strategy.loc[f"{hand_type} {sum(player_hand)}", open_card].split('/')[-1]
    

# adjust action if hit1/2
if action == "hit1":
    if len(player_hand) == 5:
        action = "hit"
    else:
        action = "stand"
    
elif action == "hit2":
    if len(player_hand) in [4, 5]:
        action = "hit"
    else:
        action = "stand"


print(action)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




