#!/usr/bin/env python
# coding: utf-8

# From the book, "Automate the boring stuff with python" written by Al Sweigart. Accessible for free, read [here](https://automatetheboringstuff.com/#toc)

# In[3]:


# Functions
# function begins with the keyword `def` followed by the function name and a colon(:)

def hello():
    print("Howdy!")
    print("Howdy!")
    print("Howdy!")
    
# invoking or calling the function
hello()
    


# In[5]:


# Functions with parameters
def hello(name):
    print("Hello "+name)
hello("Ashish")


# One special thing to note about parameters is that the value stored in a parameter is forgotten when the function returns. When creating a function using the def statement, you can specify what the return value should be with a return statement. A return statement consists of the following:
# 
# - The return keyword
# - The value or expression that the function should return
# 
# In Python there is a value called None, which represents the absence of a value. None is the only value of the NoneType data type. (Other programming languages might call this value null, nil, or undefined.) Just like the Boolean True and False values, None must be typed with a capital N.
# 
# #### Local and Global Scope
# Parameters and variables that are assigned in a called function are said to exist in that function’s *local scope*. Variables that are assigned outside all functions are said to exist in the *global scope*. A variable that exists in a local scope is called a local variable, while a variable that exists in the global scope is called a global variable. A variable must be one or the other; it cannot be both local and global. Think of a scope as a container for variables. When a scope is destroyed, all the values stored in the scope’s variables are forgotten. There is only one global scope, and it is created when your program begins. When your program terminates, the global scope is destroyed, and all its variables are forgotten. 
# 
# Scopes matter for several reasons:
# 
# - Code in the global scope cannot use any local variables.
# - However, a local scope can access global variables.
# - Code in a function’s local scope cannot use variables in any other local scope.
# - You can use the same name for different variables if they are in different scopes. That is, there can be a local variable named spam and a global variable also named spam.
# 

# In[6]:


# Local Variables Cannot Be Used in the Global Scope
def spam():
    eggs = 31337
spam()
print(eggs)


# The error happens because the eggs variable exists only in the local scope created when spam() is called. Once the program execution returns from spam, that local scope is destroyed, and there is no longer a variable named eggs. So when your program tries to run print(eggs), Python gives you an error saying that eggs is not defined. This makes sense if you think about it; when the program execution is in the global scope, no local scopes exist, so there can’t be any local variables. This is why only global variables can be used in the global scope.

# Global Variables Can Be Read from a Local Scope
# Consider the following program:

# In[7]:


def spam():
    print(eggs)
eggs = 42
spam()
print(eggs)


# Since there is no parameter named eggs or any code that assigns eggs a value in the spam() function, when eggs is used in spam(), Python considers it a reference to the global variable eggs. This is why 42 is printed when the previous program is run.

# ##### Local and Global Variables with the Same Name
# To simplify your life, avoid using local variables that have the same name as a global variable or another local variable. But technically, it’s perfectly legal to do so in Python. 

# #### The global Statement
# If you need to modify a global variable from within a function, use the global statement. If you have a line such as global eggs at the top of a function, it tells Python, “In this function, eggs refers to the global variable, so don’t create a local variable with this name.”

# In[8]:


eggs="global"
print("\n In global environment: "+eggs)
def spam():
    global eggs
    eggs="spam"
    print("\n In local environment: "+eggs)
spam()
    


# There are four rules to tell whether a variable is in a local scope or global scope:
# 
# - If a variable is being used in the global scope (that is, outside of all functions), then it is always a global variable.
# - If there is a global statement for that variable in a function, it is a global variable.
# - Otherwise, if the variable is used in an assignment statement in the function, it is a local variable.
# - But if the variable is not used in an assignment statement, it is a global variable.

# #### Exception Handling
# Errors can be handled with *try* and *except* statements. The code that could potentially have an error is put in a try clause. The program execution moves to the start of a following except clause if an error happens

# In[9]:


# This is a guess the number game.
import random
secretNumber = random.randint(1, 20)
print('I am thinking of a number between 1 and 20.')

# Ask the player to guess 6 times.
for guessesTaken in range(1, 7):
    print('Take a guess.')
    guess = int(input())

    if guess < secretNumber:
        print('Your guess is too low.')
    elif guess > secretNumber:
        print('Your guess is too high.')
    else:
        break    # This condition is the correct guess!

if guess == secretNumber:
    print('Good job! You guessed my number in ' + str(guessesTaken) + ' guesses!')
else:
    print('Nope. The number I was thinking of was ' + str(secretNumber))


# In[ ]:




