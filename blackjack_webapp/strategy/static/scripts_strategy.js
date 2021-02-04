

var count = 0;
// takes one count off of the counter element from a specific card
function minus_card(element_id) {
    let counter_element = document.getElementById(element_id + "_number");
    count = counter_element.value;
    count++; // verander dit naar count--
    counter_element.value = count;
}











