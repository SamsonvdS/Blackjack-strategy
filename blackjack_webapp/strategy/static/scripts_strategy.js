// set necessary variables
var csrftoken;
var current_url;

// things to be done at page load
window.addEventListener('DOMContentLoaded', function() {
    // get csrftoken 
    csrftoken = document.getElementsByName("csrfmiddlewaretoken");
    csrftoken = csrftoken[0].value;

    // get current url
    current_url = window.location.href;
})



// save cards in dealer/player hand
var dealer_hand = [];
var player_hand = [];

// save the left (new) side of the splitted hand
var player_split_hand = [];


/* 
registers card to dealer and/or player hand
*/
function onRightClick(element) {
    // get class of element
    const element_class = element.target.className

    // only do this if double click was on card image button
    if (element_class === "card_button_image") {
        let card = element.target.alt;

        // decrease count
        minus_card(card);

        // skip the .jpg part
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

        // prevent showing menu
        element.preventDefault()
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
    else if (element_class === "calculate_action") {
        // disable all buttons
        disable_buttons()

        // create data dictionary
        let data = get_card_counts();
        data['player_hand'] = player_hand;
        data['dealer_hand'] = dealer_hand;
        data['bankroll'] = document.getElementById('bankroll').value;

        // send data to server
        fetch(`${current_url}/calculate_hand`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data)
        })
        // turn response into json (dictionary)
        .then(response => response.json())

        .then(data => {
            let element;
            // adjust ev of insurance and results in html
            for (var key in data) {
                element = document.getElementById(key);
                element.value = data[key];
            }

            // adjust ev and results colors
            adjust_ev_colors()
            adjust_result_colors()

            // activate all buttons
            activate_buttons()
        })
    }
    else if (element_class === "new_round") {
        // disable all buttons
        disable_buttons()

        // create data dictionary
        let data = get_card_counts();
        data['bankroll'] = document.getElementById('bankroll').value;

        // send data to server
        fetch(`${current_url}/new_round`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data)
        })

        // turn response into json (dictionary)
        .then(response => response.json())

        .then(data => {
            let element;
            // change expected values in html
            for (var key in data) {
                element = document.getElementById(key);
                element.value = data[key];
            }

            // adjust ev colors
            adjust_ev_colors()

            // activate all buttons
            activate_buttons()

            // empty dealer and player hands
            dealer_hand.length = 0;
            player_hand.length = 0;
            player_split_hand.length = 0;
        })
    }
    else if (element_class === "new_shoe") {
        // disable all buttons
        disable_buttons()
        data = {
            'bankroll': document.getElementById('bankroll').value,
        }

        // send data to server
        fetch(`${current_url}/new_shoe`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data)
        })

        // turn response into json (dictionary)
        .then(response => response.json())

        .then(data => {
            let element;
            // change expected values in html
            for (var key in data) {
                element = document.getElementById(key);
                element.value = data[key];
            }

            const number_of_decks = document.getElementById('number_of_decks').value;
            // reset counts of cards
            document.querySelectorAll('.card_button_number').forEach(function (card_count) {
                card_count.value = number_of_decks;
            })

            // adjust ev colors
            adjust_ev_colors()

            // activate all buttons
            activate_buttons()

            // empty dealer and player hands
            dealer_hand.length = 0;
            player_hand.length = 0;
            player_split_hand.length = 0;
        })
    }

    // display cards
    display_hand_cards()
}





/*
--------------------------------------------------------
helper functions
--------------------------------------------------------
*/

/* disables all buttons */
function disable_buttons() {
    document.querySelectorAll('button').forEach(function(button) {
        button.disabled = true;
    })
}

/* activates all buttons */
function activate_buttons() {
    document.querySelectorAll('button').forEach(function(button) {
        button.disabled = false;
    })
}


/* 
gets count for each card
returns dictionary of counts per suit 
*/
function get_card_counts() {
    let save_counts = {
        'Hearts': [],
        'Diamonds': [],
        'Spades': [],
        'Clubs': [],
    };
    let id;

    document.querySelectorAll('.card_button_number').forEach(function (element) {
        // get first three characters of id
        id = element.id.substring(0, 3);
        
        // save value of element at correct place
        if (id.includes('H')) {
            save_counts['Hearts'].push(element.value);
        }
        else if (id.includes('D')) {
            save_counts['Diamonds'].push(element.value);
        }
        else if (id.includes('S')) {
            save_counts['Spades'].push(element.value);
        }
        else if (id.includes('C')) {
            save_counts['Clubs'].push(element.value);
        }
    })

    return save_counts
}


/* displays cards in dealer and player hands */
function display_hand_cards() {
    document.getElementById("dealer_hand").innerHTML = dealer_hand;
    document.getElementById("player_hand").innerHTML = player_hand.toString().replace(/,/g, ' '); // change commas into spaces
    document.getElementById("player_split_hand").innerHTML = player_split_hand.toString().replace(/,/g, ' ');
}


/* takes one count off of the counter element from a specific card */
function minus_card(image) {
    // get specific counter element
    const counter_element = document.getElementById(image + "_number");

    // decrease value by one
    let count = counter_element.value;
  
    // minimum count is zero
    if (count > 0) {
        count--;
        counter_element.value = count;
    }
}


/* changes color to green if ev is positive, otherwise red */
function adjust_ev_colors() {
    // for every element with side_bets_ev class change background
    document.querySelectorAll('.side_bets_ev').forEach(function(side_bet) {
        if (side_bet.value > 0) {
            side_bet.style.backgroundColor = "forestgreen";
        }
        else {
            side_bet.style.backgroundColor = "red";
        }
    })

    // for every element with kelly_pct class change background
    document.querySelectorAll('.kelly_pct').forEach(function(kelly_pct) {
        if (kelly_pct.value > 0) {
            kelly_pct.style.backgroundColor = "forestgreen";
        }
        else {
            kelly_pct.style.backgroundColor = "red";
        }
    })

    // for every element with optimal_bet class change background
    document.querySelectorAll('.optimal_bet').forEach(function(optimal_bet) {
        if (optimal_bet.value > 0) {
            optimal_bet.style.backgroundColor = "darkgreen";
        }
        else {
            optimal_bet.style.backgroundColor = "red";
        }
    })

}

/* changes colors of results */
function adjust_result_colors() {
    // for every element with results_input class change background
    document.querySelectorAll('.results_input').forEach(function(result) {
        if (result.id === "true_count") {
            if (result.value >= 2.6) {
                result.style.backgroundColor = "forestgreen";
            }
            else if (result.value < 2.6) {
                result.style.backgroundColor = "red";
            }
            else {
                result.style.backgroundColor = "white";
            }
        }
        else if (result.id === "hand_decision") {
            if (result.value === "Stand") {
                result.style.backgroundColor = "yellow";
            }
            else if (result.value === "Hit") {
                result.style.backgroundColor = "tomato";
            }
            else if (result.value.includes('Double')) {
                result.style.backgroundColor = "dodgerblue";
            }
            else if (result.value.includes("Split")) {
                result.style.backgroundColor = "limegreen";
            }
            else {
                result.style.backgroundColor = "white";
                result.value = "";
            }
        }
        // change color of kelly_pct and optimal_bet for true count
        else {
            if (result.value > 0) {
                result.style.backgroundColor = "forestgreen";
            }
            else if (result.value <= 0) {
                result.style.backgroundColor = "red";
            }
            else {
                result.style.backgroundColor = "white";
            }
        }
    })
}









