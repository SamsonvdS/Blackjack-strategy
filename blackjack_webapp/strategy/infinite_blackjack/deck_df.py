import pandas as pd

# number of cards in a standard deck
N_CARDS_IN_DECK = 52


class Deckdf:
    """this is a deck dataframe object"""

    def __init__(self, number_of_decks):
        """initialize variables"""
        # cards in deck
        self.cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        self.number_of_decks = number_of_decks
        self.number_of_decks_remaining = number_of_decks

        self.probdf = create_prob_df()
        self.probdf_simple = create_simple_probdf()


    def create_simple_probdf(self):
        """creates simplified probdf where J, Q, K are seen as a 10"""
        probdf_simple = self.probdf.copy()
        
        # add the number of cards for each suit of J, Q, and K to 10
        probdf_simple.loc['10', :] += probdf_simple.loc['J':'K', :].sum()
        probdf_simple.drop(['J', 'Q', 'K'], inplace=True)
        
        return probdf_simple


    def create_prob_df(self):
        """
        create a pandas dataframe containing the number of
        each card of each suit in the deck
        """
        # total number of cards of a specific face value of a specific suit at the start of a deck
        total_start_cards = self.number_of_decks

        # number of cards in this column for each card
        start_cards_column = [total_start_cards for i in range(len(self.cards))]

        # create starting dataframe
        probdf = pd.DataFrame({
            'Clubs': start_cards_column,
            'Diamonds': start_cards_column,
            'Hearts': start_cards_column,
            'Spades': start_cards_column,
        }, index=self.cards)

        # sum total cards of a face value
        probdf['Total_cards'] = probdf.loc[:, self.suits].sum(axis=1)

        return probdf


    def update_prob_df(self, clubs, diamonds, hearts, spades):
        """
        create a pandas dataframe containing the number of
        each card of each suit in the deck
        """
        # create starting dataframe
        probdf = pd.DataFrame({
            'Clubs': clubs,
            'Diamonds': diamonds,
            'Hearts': hearts,
            'Spades': spades,
        }, index=self.cards)

        # sum total cards of a face value
        probdf['Total_cards'] = probdf.loc[:, self.suits].sum(axis=1)

        self.number_of_decks_remaining = sum(probdf['Total_cards']) / N_CARDS_IN_DECK

        return probdf








