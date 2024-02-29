function showTransactions( customerId, accountId ) {
    window.location = "/transactions/" + customerId + "/" + accountId;
}

function buttonColor() {
var checkbox = document.getElementById("delete");
var editButton = document.getElementById("button");

if (checkbox.checked) {
    editButton.style.background = "red";
    editButton.value = "Delete";
} else {
    editButton.style.background = "#047aed"; 
    editButton.value = "Edit";

    }
}

function buttonClick(customerId) {
    var button = document.getElementById("button");
    if (button.value == "Edit") {
        window.location = "/edit/" + customerId;
    } else {
        if (confirm("Are you sure you want to delete this customer?"));
    }
}