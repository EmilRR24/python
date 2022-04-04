"""
1. Basic - Print all integers from 0 to 150.
2. Multiples of Five - Print all the multiples of 5 from 5 to 1,000
3. Counting, the Dojo Way - Print integers 1 to 100. If divisible by 5, print "Coding" instead. If divisible by 10, print "Coding Dojo".
4. Whoa. That Sucker's Huge - Add odd integers from 0 to 500,000, and print the final sum.
5. Countdown by Fours - Print positive numbers starting at 2018, counting down by fours.
6. Flexible Counter - Set three variables: lowNum, highNum, mult. Starting at lowNum and going through highNum, print only the integers that are a multiple of mult. For example, if lowNum=2, highNum=9, and mult=3, the loop should print 3, 6, 9 (on successive lines)
"""
# 1. Basic - Print all integers from 0 to 150.
def basic():
    for x in range(0, 151):
        print(x)
basic()

# 2. Multiples of Five - Print all the multiples of 5 from 5 to 1,000
def multiple_fives():
    for x in range(5, 1001, 5):
        print(x)
multiple_fives()

# 3. Counting, the Dojo Way - Print integers 1 to 100. If divisible by 5, print "Coding" instead. If divisible by 10, print "Coding Dojo".
def dojo_way():
    for x in range(1, 101):
        if x%10 == 0:
            print("Coding Dojo")
        elif x%5 == 0:
            print("Coding")
        else:
            print(x)
dojo_way()

# 4. Whoa. That Sucker's Huge - Add odd integers from 0 to 500,000, and print the final sum.
def sum(start, end):
    sum = 0
    for x in range(start, end+1):
            sum = sum + x
    print(sum)
sum(0, 500000)

# 5. Countdown by Fours - Print positive numbers starting at 2018, counting down by fours.
def countdown():
    for x in range (2018, 0, -4):
        if x > 0:
            print(x)
countdown()

# 6. Flexible Counter - Set three variables: lowNum, highNum, mult. Starting at lowNum and going through highNum, print only the integers that are a multiple of mult. For example, if lowNum=2, highNum=9, and mult=3, the loop should print 3, 6, 9 (on successive lines)
def counter(lowNum, highNum, mult):
    for x in range (lowNum, highNum+1):
        if x%mult == 0:
            print(x)
counter(2, 9, 3)