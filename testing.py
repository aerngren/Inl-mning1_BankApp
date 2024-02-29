import unittest
from app import app

# Make sure account "1" dont have to much money 
class TestAccountActions(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_withdrawal_not_enough_balance(self):
        data = {
            'from_account_id': '1',
            'transaction_type': 'Withdrawal',
            'amount': '10000000.0' 
        }
        response = self.app.post('/account_action', data=data, follow_redirects=True)
        self.assertEqual('Not enough balance or invalid amount.', response.data.decode())

    def test_witdrawal_negative_amount(self):
        data = {
            'from_account_id': '1',
            'transaction_type': 'Withdrawal',
            'amount': '-100.0' 
        }
        response = self.app.post('/account_action', data=data, follow_redirects=True)
        self.assertEqual('Not enough balance or invalid amount.', response.data.decode())

    def test_withdrawl_no_account(self):
        data = {
            'from_account_id': '',
            'transaction_type': 'Withdrawal',
            'amount': '100.0' 
        }
        response = self.app.post('/account_action', data=data, follow_redirects=True)
        self.assertEqual('Account do not exist.', response.data.decode())

    def test_depostit_negative_amount(self):
        data = {
            'from_account_id': '1',
            'transaction_type': 'Deposit',
            'amount': '-100.0' 
        }
        response = self.app.post('/account_action', data=data, follow_redirects=True)
        self.assertEqual('Invalid amount.', response.data.decode())

    def test_deposit_no_account(self):
        data = {
            'from_account_id': '',
            'transaction_type': 'Deposit',
            'amount': '100.0' 
        }
        response = self.app.post('/account_action', data=data, follow_redirects=True)
        self.assertEqual('Account do not exist.', response.data.decode())

    def test_transfer_from_no_account(self):
        data = {
            'from_account_id': '',
            'transaction_type': 'Transfer',
            'amount': '100.0', 
            'to_account': '5'
        }
        response = self.app.post('/account_action', data=data, follow_redirects=True)
        self.assertEqual('One or both accounts do not exist.', response.data.decode())
    
    def test_transfer_to_no_account(self):
        data = {
            'from_account_id': '1',
            'transaction_type': 'Transfer',
            'amount': '100.0', 
            'to_account': ''
        }
        response = self.app.post('/account_action', data=data, follow_redirects=True)
        self.assertEqual('One or both accounts do not exist.', response.data.decode())
    
    def test_transfer_to_high_amount(self):
        data = {
            'from_account_id': '1',
            'transaction_type': 'Transfer',
            'amount': '1000000.0', 
            'to_account': '10'
        }
        response = self.app.post('/account_action', data=data, follow_redirects=True)
        self.assertEqual("Not enough balance or invalid amount.", response.data.decode())
    
    def test_transfer_negative_amount(self):
        data = {
            'from_account_id': '1',
            'transaction_type': 'Transfer',
            'amount': '-10.0', 
            'to_account': '10'
        }
        response = self.app.post('/account_action', data=data, follow_redirects=True)
        self.assertEqual("Not enough balance or invalid amount.", response.data.decode())

if __name__ == '__main__':
    unittest.main()