// get csrftoken 
var csrftoken;
window.addEventListener('DOMContentLoaded', function() {
    csrftoken = document.getElementsByName("csrfmiddlewaretoken");
    csrftoken = csrftoken[0].value;
})



// save cards in dealer/player hand
var dealer_hand = [];
var player_hand = [];

// save the left (new) side of the splitted hand
var player_split_hand = [];


/* 
registers card to dealer and/or player hand
*/
function onDoubleClick(element) {
    // correct the double substraction of card count
    const image = element.target.alt;
    plus_card(image);

    // get class of element
    const element_class = element.target.className

    // only do this if double click was on card image button
    if (element_class === "card_button_image") {
        // skip the .jpg part
        let card = element.target.alt;
        card = card.substring(0, card.length - 4);
        
        const value = card.substring(0, card.length - 1);
        let suit = card.substring(card.length - 1);

        // convert suit to symbol
        if (suit === "H") {
            suit = '\u2665';
        }
        else if (suit === "D") {
            suit = '\u2666';
        }
        else if (suit === "S") {
            suit = '\u2660';
        }
        else if (suit === "C") {
            suit = '\u2663';
        }
        
        // add card + suit to correct hand
        if (player_hand.length === 0) {
            player_hand.push(`${value}${suit}`);
        }
        else if (dealer_hand.length === 0) {
            dealer_hand.push(`${value}${suit}`);
        }
        else {
            player_hand.push(`${value}${suit}`);
        }
        
        // display cards
        display_hand_cards()
    }
}


/* 
decides what will be done, depending on element clicked
*/
function onClick(element) {
    // get class of element
    const element_class = element.target.className;

    // if a card button image is clicked 
    if (element_class === "card_button_image") {
        const image = element.target.alt;
        minus_card(image);
    }
    else if (element_class === "new_round") {
        // empty the hand lists
        dealer_hand.length = 0;
        player_hand.length = 0;
    }
    else if (element_class === "undo_dealer") {
        dealer_hand.pop();
    }
    else if (element_class === "undo_player") {
        player_hand.pop();
    }
    else if (element_class === "split") {
        // split is only possible if two cards in hand
        if (player_hand.length === 2) {
            let card1 = player_hand[0];
            let card2 = player_hand[player_hand.length - 1];
            
            card1 = card1.substring(0, card1.length - 1);
            card2 = card2.substring(0, card2.length - 1);

            // cards with value of 10
            let tens = ['10', 'J', 'Q', 'K'];

            if (tens.includes(card1)) {
                card1 = '10';
            }
            if (tens.includes(card2)) {
                card2 = '10';
            }

            // only split if also the card values are the same
            if (card1 === card2) {
                // add card from player hand to split hand
                player_split_hand.push(player_hand.pop());
            }
        }
        // correct split (unsplit)
        else if (player_hand.length === 1 && player_split_hand.length === 1) {
            player_hand.push(player_split_hand.pop());
        }
    }
    else if (element_class === "second_hand" && player_split_hand.length > 0) {
        // swap player hand and split hand
        let temp = player_hand;
        player_hand = player_split_hand;
        player_split_hand = temp;
    }
    else if (element_class === "new_round") {
        dealer_hand.length = 0;
        player_hand.length = 0;
        player_split_hand.length = 0;


    }
    else if (element_class === "new_shoe") {
        dealer_hand.length = 0;
        player_hand.length = 0;
        player_split_hand.length = 0;


    }
    else if (element_class === "calculate_action") {
        console.log(csrftoken)
        fetch('http://127.0.0.1:8000/strategy/infinite_blackjack/calculate_hand', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'player_hand': player_hand,
            
        }),
        credentials: 'same-origin',
        })
        .then(response => {console.log(response); response.json()})
        .then(data => {
        console.log('Success:', data);
        })
    }

    // display cards
    display_hand_cards()
}




/* displays cards in dealer and player hands */
function display_hand_cards() {
    document.getElementById("dealer_hand").innerHTML = dealer_hand;
    document.getElementById("player_hand").innerHTML = player_hand;
    document.getElementById("player_split_hand").innerHTML = player_split_hand; 
}


/* takes one count off of the counter element from a specific card */
function minus_card(image) {
    // get specific counter element
    const counter_element = document.getElementById(image + "_number");

    // decrease value by one
    let count = counter_element.value;
    count--;

    // minimum count is zero
    if (count >= 0) {
        counter_element.value = count;
    }
}


/* adds one count to the counter element from a specific card */
function plus_card(image) {
    // get specific counter element
    const counter_element = document.getElementById(image + "_number");

    // increase value by one
    let count = counter_element.value;
    count++;
    counter_element.value = count;
}


/* changes color to green if ev is positive, otherwise red */
function adjust_ev_colors() {
    // for every element with this class change background and text color
    document.querySelectorAll('.side_bets_ev').forEach(function(side_bet) {
        if (side_bet.value > 0) {
            side_bet.style.backgroundColor = "green";
        }
        else {
            side_bet.style.backgroundColor = "red";
        }
    })
}









