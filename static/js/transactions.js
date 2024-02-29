document.getElementById("amount").addEventListener("input", inputChange);
    document.getElementById("to_customer").addEventListener("input", GetAccounts);
    
    function GetAccounts() {
        var to_customer = document.getElementById("to_customer").value;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/get-account/" + to_customer, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var accounts = JSON.parse(xhr.responseText);
                displayAccounts(accounts);
            }
        };

        xhr.send();
    }

    function displayAccounts(accounts) {
        var table = document.createElement("table");
        var thead = document.createElement("thead");
        var tbody = document.createElement("tbody");

        var customerRow = document.createElement("tr");
        var customerHeader = document.createElement("th");
        var customerName = "Customer: " + accounts[0].Name;
        document.getElementById("name").innerHTML = customerName;

        var tr = document.createElement("tr");
        var th = document.createElement("th");
        th.appendChild(document.createTextNode("Account Type"));
        tr.appendChild(th);
        th = document.createElement("th");
        th.appendChild(document.createTextNode("Balance"));
        tr.appendChild(th);
        thead.appendChild(tr);
        table.appendChild(thead);

        for (var i = 0; i < accounts.length; i++) {
            tr = document.createElement("tr");
            var td = document.createElement("td");
            td.appendChild(document.createTextNode(accounts[i].AccountType));
            tr.appendChild(td);
            td = document.createElement("td");
            td.appendChild(document.createTextNode(accounts[i].Balance));
            tr.appendChild(td);
            tbody.appendChild(tr);

            tr.addEventListener("click", function() {
            var accountId = this.getAttribute("data_account_id");
            document.getElementById("to_account_list").innerHTML = "Account ID: " + accountId;
            document.getElementById("to_account").value = accountId;
        });

        tr.setAttribute("data_account_id", accounts[i].AccountID);
        }

    

        
        tbody.classList.add("customer_table");
        table.appendChild(tbody);

        var div = document.getElementById("accounts");
        div.innerHTML = "";
        div.appendChild(table);
    }


    function inputChange() {
    var to_account = document.getElementById("to_account").value;
    var amountField = document.getElementById("amount");
    var trabutton = document.getElementById("button");
    var amount = parseFloat(amountField.value);
    var selectElement = document.querySelector("#transaction_type");
    var total_balance = parseFloat(document.getElementById("total_balance").getAttribute("data-total-balance"));
    console.log("Amount:", amount);
    console.log("Total Balance:", total_balance);
    console.log("To Account:", to_account);

    if (selectElement.value === "Withdrawal") {
        if (isNaN(amount) || amount <= 0 || amount > total_balance) {
            amountField.style.backgroundColor = "red";
            trabutton.type = "hidden";
        } else {
            amountField.style.backgroundColor = "white";
            trabutton.type = "submit";
            trabutton.value = "Withdrawal";
        }
    } else if (selectElement.value === "Deposit") {
        if (isNaN(amount) || amount <= 0) {
            amountField.style.backgroundColor = "red";
            trabutton.type = "hidden";
        } else {
            amountField.style.backgroundColor = "white";
            trabutton.type = "submit";
            trabutton.value = "Deposit";
        }
    } else if (selectElement.value === "Transfer") {
        if (isNaN(amount) || amount <= 0 || amount > total_balance || to_account === "") {
            amountField.style.backgroundColor = "red";
            trabutton.type = "hidden";
        } else {
            amountField.style.backgroundColor = "white";
            trabutton.type = "submit";
            trabutton.value = "Transfer";
        }
    } 
}

    document.addEventListener("DOMContentLoaded", function() {
    var selectElement = document.querySelector("#transaction_type");
    var toCustomerField = document.getElementById("to_customer");
    var nameField = document.getElementById("name");
    var accountsField = document.getElementById("accounts");
    var toAccountList = document.getElementById("to_account_list");

    selectElement.addEventListener("change", function() {
        var selectedValue = this.value;

        if (selectedValue === "Transfer") {
            toCustomerField.style.display = "block";
            nameField.style.display = "block";
            accountsField.style.display = "block";
            toAccountList.style.display = "block";
        } else {
            toCustomerField.style.display = "none";
            nameField.style.display = "none";
            accountsField.style.display = "none";
            toAccountList.style.display = "none";
        }
    });
});