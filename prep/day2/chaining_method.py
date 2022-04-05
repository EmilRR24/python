class User:		# here's what we have so far
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.account_balance = 0
    # view user account balance
    def display_user_balance(self):
        print(f"{self.name}, {self.account_balance}")
        return self
    # adding the deposit method
    def make_deposit(self, amount):	# takes an argument that is the amount of the deposit
        self.account_balance += amount	# the specific user's account increases by the amount of the value received
        return self
    # adding the withdrawal method
    def make_withdrawal(self, amount):	# takes an argument that is the amount of the withdraw
        self.account_balance -= amount	# the specific user's account decreases by the amount of the value withdrawn
        return self
guido = User("Guido van Rossum", "guido@python.com")
monty = User("Monty Python", "monty@python.com")
jane  = User("Jane Doe", "jane@python.com")

# Have the first user make 3 deposits and 1 withdrawal and then display their balance
guido.make_deposit(100).make_deposit(100).make_deposit(100).make_withdrawal(100).display_user_balance()

# Have the second user make 2 deposits and 2 withdrawals and then display their balance
monty.make_deposit(100).make_deposit(100).make_withdrawal(50).make_withdrawal(20).display_user_balance()

# Have the third user make 1 deposits and 3 withdrawals and then display their balance
jane.make_deposit(100).make_withdrawal(10).make_withdrawal(20).make_withdrawal(20).display_user_balance()