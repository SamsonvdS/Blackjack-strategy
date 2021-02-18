# database import
from .models import Card_Image

# calculation imports
from .infinite_blackjack.blackjack_hands import make_decision
from .infinite_blackjack.insurance import calculate_ev as calculate_ev_insurance
from .infinite_blackjack.side_hot_3 import calculate_ev as calculate_ev_hot_3
from .infinite_blackjack.side_21_plus_3 import calculate_ev as calculate_ev_21_plus_3
from .infinite_blackjack.side_any_pair import calculate_ev as calculate_ev_any_pair
from .infinite_blackjack.side_bust_it import calculate_ev as calculate_ev_bust_it


def order_cards():
    """
    orders cards for each suit
    returns the sorted lists of cards
    """
    # get all card image objects
    all_card_images = Card_Image.objects.all()

    # filter card images by suit
    hearts = [card for card in all_card_images if card.suit == "Hearts"]
    diamonds = [card for card in all_card_images if card.suit == "Diamonds"]
    spades = [card for card in all_card_images if card.suit == "Spades"]
    clubs = [card for card in all_card_images if card.suit == "Clubs"]
    
    # order cards this way
    card_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    # sort card images in card_order
    hearts.sort(key=lambda card: card_order.index(card.card))
    diamonds.sort(key=lambda card: card_order.index(card.card))
    spades.sort(key=lambda card: card_order.index(card.card))
    clubs.sort(key=lambda card: card_order.index(card.card))

    return hearts, diamonds, spades, clubs

    
def how_to_play_hand(Deckdf, dealer_hand, player_hand):
    """returns how to play your hand against the dealer's open_card"""
    hand_decision, true_count, kelly_pct = make_decision(Deckdf, dealer_hand, player_hand)
    return hand_decision, true_count, kelly_pct

def calculate_insurance(Deckdf):
    """calculates the expected value of taking insurance"""
    return calculate_ev_insurance(Deckdf)

def calculate_side_bets(Deckdf):
    """
    calculates the expected values and optimal bet percentages of the side bets
    returns list of expected values and optimal bets
    """
    ev_hot_3, kelly_pct_hot_3 = calculate_ev_hot_3(Deckdf)
    ev_21_plus_3, kelly_pct_21_plus_3 = calculate_ev_21_plus_3(Deckdf)
    ev_any_pair, kelly_pct_any_pair = calculate_ev_any_pair(Deckdf)
    ev_bust_it, kelly_pct_bust_it = calculate_ev_bust_it(Deckdf)

    expected_values = [ev_hot_3, ev_21_plus_3, ev_any_pair, ev_bust_it]
    kelly_pct = [kelly_pct_hot_3, kelly_pct_21_plus_3, kelly_pct_any_pair, kelly_pct_bust_it]

    return expected_values, kelly_pct







