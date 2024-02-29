from model import Customer, Account

def get_account(account_id):
    account = Account.query.get(account_id)
    return account

def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    return customer