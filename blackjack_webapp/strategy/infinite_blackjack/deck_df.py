import pandas


def create_simple_probdf(probdf):
    """creates simplified probdf where J, Q, K are seen as a 10"""
    probdf_simple = probdf.copy()
    
    # add the number of cards for each suit of J, Q, and K to 10
    probdf_simple.loc['10', :] += probdf_simple.loc['J':'K', :].sum()
    probdf_simple.drop(['J', 'Q', 'K'], inplace=True)
    
    return probdf_simple


def create_prob_df(number_of_decks):
    """
    create a pandas dataframe containing the number of
    each card of each suit in the deck
    """
    # cards in deck
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']

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

    # sum total cards of a face value
    probdf['Total_cards'] = probdf.loc[:, suits].sum(axis=1)

    return probdf