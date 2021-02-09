

// takes one count off of the counter element from a specific card
function minus_card(element_id) {
    // get specific counter element
    let counter_element = document.getElementById(element_id + "_number");

    // decrease value by one
    count = counter_element.value;
    count--;

    // minimum count is zero
    if (count >= 0) {
        counter_element.value = count;
    }
}

/* changes color to green if ev is positive, otherwise red*/
function adjust_colors() {
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









