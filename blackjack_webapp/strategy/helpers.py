from .models import Card_Image


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