

// save cards in dealer/player hand
var dealer_hand = [];
var player_hand = [];

/* 
registers card to dealer and/or player hand
*/
function onDoubleClick(element) {
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
        document.getElementById("dealer_hand").innerHTML = dealer_hand
        document.getElementById("player_hand").innerHTML = player_hand 
    }
}


/* 
decides what will be done, depending on element clicked
*/
function onClick(element) {
    console.log(element);
    
    // get class of element
    const element_class = element.target.className;
    const image = element.target.alt;
    console.log(element_class);

    // if a card button image is clicked 
    if (element_class === "card_button_image") {
        minus_card(image);
    }
    else if (element_class === "new_round") {
        // empty the hand lists
        dealer_hand.length = 0;
        player_hand.length = 0;
    }
}


// takes one count off of the counter element from a specific card
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


/* changes color to green if ev is positive, otherwise red*/
function adjust_ev_colors() {
    // for every element with this class change background and text color
    document.querySelectorAll('.side_bets_ev').forEach(function(side_bet) {
        if (side_bet.value > 0) {
            side_bet.style.backgroundColor = "green";
            side_bet.style.color = "white";
        }
        else {
            side_bet.style.backgroundColor = "red";
            side_bet.style.color = "white";
        }
    })
}









