# Blackjack-strategy
**At least the first version is for *Infinite Blackjack from Evolution Gaming*.** (currently there is only one version)

This is a web interface for calculating strategy of blackjack hands. 

- The betting strategy depends on the deck composition (what cards are left in the deck and how many)
- Exact probabilities are calculated for the side bets, so that you know when to bet. Also Kelly Criterion is used to calculate the optimal amount to bet.
- Strategy for blackjack (the main bet) on when to bet and how to play a hand. Also Kelly Criterion is used to calculate the optimal amount to bet.
- The main bet is not exactly calculated, but the tables from the book *Basic Blackjack by Stanford Wong* are used.

### Requirements
- Python 3.8+
- Django
- Pandas

- Large computer screen to fit both this webapplication and the Blackjack game, or two computer screens.

## Usage
Run in command line

To start webapp
```
python3 manage.py runserver
```
In browser type: http://127.0.0.1:8000/strategy and then select the correct Blackjack version (currently there is only one version)

- Once you are on the Blackjack page (where the cards are displayed), fill in the size of your bankroll and click on the New Shoe button. This will make sure that your bankroll size is taken into account when calculating your optimal bet size.
- If you forget to click on the New Shoe button before you start playing Blackjack, don't worry. Just fill in your bankroll and next time you click the New Round button, it will register your bankroll.

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

### Displayed (red) colored boxes
Every (side) bet has its own colored boxes to display the statistical edge, the percentage of your bankroll to bet, and the amount of money to bet.

#### For every group of boxes

<b>Left top</b><br>
These boxes display the statistical edge that you have for only that specific bet:
- Negative and red means that the casino has the statistical edge
- Positive and green means that you have the statistical edge

<b>Left bottom</b><br>
These boxes display the percentage of your bankroll to bet (you don't have to look at this. It is actually unnecessary information)
- It is red if you should not bet and green if you should bet

<b>Right bottom</b><br>
These boxes display the amount of money that you should bet:
- It is red if you should not bet and green if you should bet
- Never bet more money than the amount displayed, because this optimal amount of money to bet is calculated with Kelly Criterion. 
- It is advised to bet slightly less than the amount of displayed.






