# Blackjack-strategy
<b>At least the first version is for Infinite Blackjack from Evolution Gaming.</b>

- Web interface for calculating strategy of blackjack hands. Exact probabilities for side bets, depending on deck composition, so that you know when to bet. 
- Strategy for blackjack (main bet) on when to bet and how to play a hand.

### requirements
- Python 3.8+

- Django
- Pandas


## Usage
run in command line

To start webapp
```
python3 manage.py runserver
```

<b>Single Click</b><br>
Card will be taken out of deck

<b>Double Click</b>
- Double click to add card to player/dealer hand
The first card will be given to the player<br>
Second card will be given to dealer<br>
Every extra card is given to player<br>

<b>Clicking Mistake</b><br>
- Single click: you can simply add one back to the counter by clicking the arrow up (visible if you hover your mouse over the counter)
- Double click: click on undo, either for the dealer or player hand 









