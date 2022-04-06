
class BankAccount:
    population = 0
    # don't forget to add some default values for these parameters!
    def __init__(self, int_rate, balance): 
        # your code here! (remember, instance attributes go here)
        self.int_rate = int_rate
        self.balance = balance
        BankAccount.population += 1
        # don't worry about user info here; we'll involve the User class soon
    def deposit(self, amount):
        self.balance += amount
        return self
    def withdraw(self, amount):
        if self.balance > amount:
            self.balance -= amount
        else:
            print('Insufficient funds: Charging a $5 fee')
            self.balance -= 5
        return self
    def display_account_info(self):
        return self.balance
    def yield_interest(self):
        if self.balance > 0:
            interest = self.balance * self.int_rate
            self.balance += interest
            return self
    @classmethod
    def user_population(cls): 
        print(f"Number of Bank Accounts: {cls.population}")

ba1 = BankAccount(.05, 100)
ba2 = BankAccount(.05, 40)

class User:		# here's what we have so far
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.accounts = []
    # view user account balance
    def display_user_balance(self, acc = 0):
        print(f"{self.name}, {self.accounts[acc].display_account_info()}")
        return self
    # adding the deposit method
    def make_deposit(self, acc, amount):	# takes an argument that is the amount of the deposit
        self.accounts[acc].deposit(amount)
        return self
    # adding the withdrawal method
    def make_withdrawal(self, acc, amount):	# takes an argument that is the amount of the withdraw
        self.accounts[acc].withdraw(amount)	# the specific user's account decreases by the amount of the value withdrawn
        return self
    def new_account(self, param):
        self.accounts.append(param)
        return self

guido = User("Guido van Rossum", "guido@python.com")
monty = User("Monty Python", "monty@python.com")
jane  = User("Jane Doe", "jane@python.com")

# guido.new_account(ba1.balance).new_account(ba2.balance).make_deposit(0, 100).make_deposit(1, 50).display_user_balance().display_user_balance(1)
guido.new_account(ba1).new_account(ba2).make_deposit(0, 100).make_deposit(1, 50).display_user_balance().display_user_balance(1)
print(ba1.display_account_info())
print(ba2.display_account_info())