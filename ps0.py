import math

def power(a, b):
    c = a ** b
    print('x ** y = ' + str(c))

def logbase2(d):
    e = math.log(d, 2)
    print('log(x) = ' + str(e))

#take input values from user
x = input('Please enter a value for x: \n')
x = int(x)

y = input('Please enter a value for y: \n')
y = int(y)

power(x,y)
logbase2(x)