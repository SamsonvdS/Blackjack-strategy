# Blackjack-strategy
<b>At least the first version is for Infinite Blackjack from Evolution Gaming.</b>

- Web interface for calculating strategy of blackjack hands. Exact probabilities for side bets, depending on deck composition, so that you know when to bet. 
- Strategy for blackjack (main bet) on when to bet and how to play a hand.

### Requirements
- Python 3.8+

- Django
- Pandas


## Usage
Run in command line

To start webapp
```
python3 manage.py runserver
```
In browser type: http://127.0.0.1:8000/strategy and then select the correct Blackjack version

### Clicking on the card images
<b>Single Click</b><br>
Card will be taken out of deck

<b>Right Click</b>
- Right click to add card to player/dealer hand
The first card will be given to the player<br>
Second card will be given to dealer<br>
Every extra card is given to player<br>

<b>Clicking Mistake</b><br>
- Single click: you can simply add one back to the counter by clicking the arrow up (visible if you hover your mouse over the counter)
- Right click: click on undo, either for the dealer or player hand. (Undo will not add one back to the counter)

<b>Buttons</b>
- New Shoe button will reset the shoe and recalculates all side bet probabilities
- New Round button will recalculate the side bet probabilities, and resets the cards in the dealer and player hands
- Calculate Action button will calculate the appropriate action to take for the specific dealer and player hand combination
- Undo button will take the last added card to the hand out of the hand
- Split button will split the cards in your hand into two hands (max one split, and only for cards with same value)
- Second Hand card will change the second/splitted hand into your current hand that is being played












