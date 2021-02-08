

var count = 0;
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











