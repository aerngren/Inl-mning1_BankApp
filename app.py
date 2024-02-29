from flask import Flask, render_template, request, redirect, url_for, jsonify, request
from flask_migrate import Migrate, upgrade
from sqlalchemy import desc
from model import db, seedData, Customer, Account, Transaction, user_datastore
from forms import EditCustomer, NewCustomer
from datetime import datetime
from get import get_account, get_customer
from flask_security import Security, login_required



 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/Bank'
app.config['SECRET_KEY'] = '1234'
app.config['SECURITY_PASSWORD_SALT'] = ('146585145368132386173505678016728509634')


db.app = app
db.init_app(app)
migrate = Migrate(app, db)

security = Security(app, user_datastore)


@app.route("/")
@login_required
def startpage():
    custumers = db.session.query(Customer.Id).count()
    accounts = db.session.query(Account.Id).count()
    total = db.session.query(db.func.sum(Account.Balance)).scalar()
    return render_template("index.html", custumers=custumers, accounts=accounts, total = total, activePage="startPage")

@app.route("/new_customer", methods=["GET", "POST"])
@login_required
def new_customer():
    new_customer_form = NewCustomer()
    if new_customer_form.validate_on_submit():
        new_customer = Customer(GivenName=new_customer_form.name.data,
                                Surname=new_customer_form.surname.data,
                                Streetaddress=new_customer_form.street.data,
                                City=new_customer_form.city.data,
                                Zipcode=new_customer_form.zip.data,
                                Country=new_customer_form.country.data,
                                CountryCode=new_customer_form.country_code.data,
                                NationalId=new_customer_form.national_id.data,
                                Telephone=new_customer_form.phone.data,
                                EmailAddress=new_customer_form.email.data)
        for account in request.form.getlist('account'):
            new_account = Account(AccountType=account, Balance=0, Customer=new_customer, Created=datetime.now())
            db.session.add(new_account)
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for('customer_details', customer_id=new_customer.Id))
    
    return render_template("new_customer.html", new_customer_form=new_customer_form)



@app.route("/customers")
@login_required
def customers():
    sortColumn = request.args.get('sortColumn', 'name')
    sortOrder = request.args.get('sortOrder', 'asc')
    page = int(request.args.get('page', 1))
    searchWord = request.args.get('q', '')
    searchFilter = request.args.get('filter', '')


    persons = Customer.query
    
    if searchFilter and searchWord:
        if searchFilter == 'Id':
            persons = persons.filter(Customer.Id.like(f'%{searchWord}%'))
        elif searchFilter == 'NationalId':
            persons = persons.filter(Customer.NationalId.like(f'%{searchWord}%'))
        elif searchFilter == 'Surname':
            persons = persons.filter(Customer.Surname.like(f'%{searchWord}%'))
        elif searchFilter == 'Adress':
            persons = persons.filter(Customer.Streetaddress.like(f'%{searchWord}%'))
        elif searchFilter == 'City':
            persons = persons.filter(Customer.City.like(f'%{searchWord}%'))



    if sortColumn == 'Id':
        column = Customer.Id
    elif sortColumn == 'Surname':
        column = Customer.Surname
    elif sortColumn == 'NationalId':
        column = Customer.NationalId
    elif sortColumn == 'Streetaddress':
        column = Customer.Streetaddress
    elif sortColumn == 'City':
        column = Customer.City
    else:
        column = Customer.Id

    if sortOrder == 'asc':
        persons = persons.order_by(column.asc())
    else:
        persons = persons.order_by(column.desc())

    paginationObjekt = persons.paginate(page=page, per_page=30, error_out=False)
    return render_template("customers.html", 
                            persons = paginationObjekt.items, 
                            activePage = 'customerPage',
                            page = page,
                            sortColumn = sortColumn,sortOrder=sortOrder,
                            has_next = paginationObjekt.has_next,
                            has_prev = paginationObjekt.has_prev,
                            pages = paginationObjekt.pages,
                            q = searchWord,
                            filter = searchFilter)


@app.route('/customer/<int:customer_id>')
@login_required
def customer_details(customer_id):
    customer = get_customer(customer_id)
    if customer:
        accounts = customer.Accounts
        total_balance = sum(account.Balance for account in accounts)
        return render_template('customer_details.html', 
                               customer=customer,
                               accounts=accounts,
                               total_balance=total_balance,
                               activePage = 'customerPage')
    
@app.route("/edit/<int:customer_id>", methods=["GET", "POST"])
@login_required
def edit_customer(customer_id):
    customer = get_customer(customer_id)
    edit_form = EditCustomer()
    
    
    if request.method == 'GET':
        edit_form.name.data = customer.GivenName
        edit_form.surname.data = customer.Surname
        edit_form.city.data = customer.City
        edit_form.street.data = customer.Streetaddress
        edit_form.phone.data = customer.Telephone
        edit_form.email.data = customer.EmailAddress

    if edit_form.validate_on_submit():
        customer.GivenName = edit_form.name.data
        customer.Surname = edit_form.surname.data
        customer.City = edit_form.city.data
        customer.Streetaddress = edit_form.street.data
        customer.Telephone = edit_form.phone.data
        customer.EmailAddress = edit_form.email.data

        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('customer_details', customer_id=customer.Id))
    
    return render_template("edit.html", customer=customer, edit_form=edit_form)


@app.route('/get-account/<int:to_customer>')
@login_required
def get_accounts(to_customer):
    customer = get_customer(to_customer)
    name = customer.Surname + " " + customer.GivenName
    if customer:
        accounts = customer.Accounts
        account_list = [{'Name': name, 'AccountID': account.Id, 'AccountType': account.AccountType, 'Balance': float(account.Balance)} for account in accounts]
        return jsonify(account_list)
    

@app.route('/transactions/<int:customer_id>/<int:account_id>', methods=["GET", "POST"])
@login_required
def transactions(account_id, customer_id):
    account =  get_account(account_id)
    customer = get_customer(customer_id)
    total_balance = float(account.Balance)
    transaction_type = ["Transfer", "Deposit", "Withdrawal"]
    operation = ["Deposit cash", "Salary", "Transfer from", "Transfer"]
    transactions = Transaction.query.filter_by(AccountId=account_id).order_by(desc(Transaction.Date)).all()
    return render_template("transactions.html", 
                           account=account,
                           customer=customer,
                           total_balance=total_balance,
                           operation=operation,
                           transactions=transactions,
                           transaction_type=transaction_type,
                           activePage = 'customerPage')

    

@app.route('/account_action', methods=["POST"])
def account_action():
    from_account_id = request.form.get('from_account_id')
    action = request.form.get('transaction_type')
    amount = float(request.form.get('amount'))
    from_account = Account.query.get(from_account_id)
    to_account_id = request.form.get('to_account')
    to_account = Account.query.get(to_account_id)

    if action == "Transfer":
        
        if not from_account or not to_account:
            return "One or both accounts do not exist."

        if from_account.Balance < amount or amount <= 0:
            return "Not enough balance or invalid amount."

        from_account.Balance -= amount
        to_account.Balance += amount

        transaction_from = Transaction(Type="Debit", Operation="Transfer to " + str(to_account_id), Date=datetime.now(), Amount=amount, NewBalance=from_account.Balance, AccountId=from_account_id)
        
        transaction_to = Transaction(Type="Debit", Operation="Transfer from " + str(from_account_id), Date=datetime.now(), Amount=amount, NewBalance=to_account.Balance, AccountId=to_account_id)

        db.session.add(transaction_from)
        db.session.add(transaction_to)
        db.session.commit()

        return redirect(url_for('customer_details', customer_id=from_account.Customer.Id))

    elif action == "Deposit":
        if not from_account:
            return "Account do not exist."
        elif amount <= 0:
            return "Invalid amount."

        from_account.Balance += amount
        
        deposit = Transaction(Type="Debit", Operation="Deposit", Date=datetime.now(), Amount=amount, NewBalance=from_account.Balance, AccountId=from_account_id)
        db.session.add(deposit)
        db.session.commit()
        return redirect(url_for('customer_details', customer_id=from_account.Customer.Id))
    
    elif action == "Withdrawal":
        if not from_account:
            return "Account do not exist."
        elif from_account.Balance < amount or amount <= 0:
            return "Not enough balance or invalid amount."
        from_account.Balance -= amount
        
        deposit = Transaction(Type="Debit", Operation="Withdrawal", Date=datetime.now(), Amount=amount, NewBalance=from_account.Balance, AccountId=from_account_id)
        db.session.add(deposit)
        db.session.commit()
        return redirect(url_for('customer_details', customer_id=from_account.Customer.Id))


if __name__  == "__main__":
    with app.app_context(): 
        upgrade()   
        seedData(app, db)
    app.run(debug=True)