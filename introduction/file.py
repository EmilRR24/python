
num1 = 42 # - variable declaration, Numbers
num2 = 2.3 # - variable declaration, Numbers
boolean = True # - variable declaration, Boolean
string = 'Hello World' # - variable declaration , String
pizza_toppings = ['Pepperoni', 'Sausage', 'Jalepenos', 'Cheese', 'Olives'] # - variable declaration, list of strings []
person = {'name': 'John', 'location': 'Salt Lake', 'age': 37, 'is_balding': False} # - variable declaration, dictionary of values {}
fruit = ('blueberry', 'strawberry', 'banana') # - variable declaration, tuples of values ()

print(type(fruit)) # - log statement
print(pizza_toppings[1]) # - log statement
pizza_toppings.append('Mushrooms') # add value to the end of list
print(person['name']) # - log statement
person['name'] = 'George' # - variable declaration of dictionary item 
person['eye_color'] = 'blue' # - variable declaration of dictionary item
print(fruit[2]) # - log statement

if num1 > 45: # conditional if, num1 is > 45
    print("It's greater") # print
else: # conditional else
    print("It's lower") # print

if len(string) < 5: #conditional if, number of items in container is < 5
    print("It's a short word!") # print
elif len(string) > 15: # conditional else if, number of items in container is > 15
    print("It's a long word!") # print
else: # conditional
    print("Just right!") # print

for x in range(5): #for loop, var x range < 5
    print(x) # print
for x in range(2,5): # for loop, var 2 =< x < 5
    print(x) # print
for x in range(2,10,3): # for loop, var 2 =< x < 10; x increments by 3
    print(x) # print
x = 0 # declare var x is 0
while(x < 5): # while loop, var x < 5
    print(x) # print 
    x += 1 # increment x by 1

pizza_toppings.pop() # removes item at default (last)
pizza_toppings.pop(1) # removes item at index 1

print(person) # print dictionary-person
person.pop('eye_color') # removes item 'eye_color' from dictionary
print(person) # print dictionary-person

for topping in pizza_toppings: # for value,var topping in list [pizza_toppings]
    if topping == 'Pepperoni': # conditional if, var topping == 'Pepperoni'
        continue # conditional for loop to continue loop
    print('After 1st if statement') # print
    if topping == 'Olives': # conditional if, var topping == 'Olives'
        break # stops the for loop

def print_hello_ten_times(): # function print_hello_ten_times() with no parameters
    for num in range(10): # for loop, var num in range num < 10
        print('Hello') # print

print_hello_ten_times() # run function print_hello_ten_times()

def print_hello_x_times(x): # function print_hello_x_times(x) with x as the parameter
    for num in range(x): # for loop, var num in range num < x - parameter of function
        print('Hello') # print

print_hello_x_times(4) # run function print_hello_x_times(4) with argument 4

def print_hello_x_or_ten_times(x = 10):  # function print_hello_x_or_ten_times(x = 10) with parameters x or 10 if no argument is set
    for num in range(x): # for loop, var num in range num < x or num < 10
        print('Hello') # print

print_hello_x_or_ten_times() # run function print_hello_x_or_ten_times() no argument is set 
print_hello_x_or_ten_times(4) # run function print_hello_x_or_ten_times(4) argument is 4


"""
Bonus section
"""

print(num3) # - NameError: name <variable name> is not defined
num3 = 72 # variable declaration
fruit[0] = 'cranberry' # change value of list at index 0
print(person['favorite_team']) # - KeyError: 'favorite_team'
print(pizza_toppings[7]) # - IndexError: list index out of range
  print(boolean) # - IndentationError: unexpected indent
fruit.append('raspberry') # - AttributeError: 'tuple' object has no attribute 'append'
fruit.pop(1) #  - delete value at index 1-