# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import random
import simplegui

# initialize global variables used in your code
count=0
secret_number=0

# define event handlers for control panel
def init():
    global count
    global secret_number
    count=0
    secret_number=0
    print "select range to play"
    print " "

def range100():
    # button that changes range to range [0,100) and restarts
    
    global count
    global secret_number
    print "New game.Range is from 0 to 100.Enter integers only."
    print "Number of guess remaining 7"
    print " "
    secret_number = random.randrange(0,100)
    count=7
   
def range1000():
    #init()
    global count
    global secret_number
    print "New game.Range is from 0 to 1000.Enter integers only."
    print "Number of guess remaining 10"
    print " "
    secret_number= random.randrange(0,1000)
    count=10

    
def get_input(guess):
    # main game logic goes here	
    global count
    global secret_number
    if count <= 0:
        print "GAME OVER."
        init()
    chosen= int(guess)
    count=count-1
    if not(count <= 0):
        print "Guess was",chosen
    
    if count>0:
        print "Number of guess remaining",count
   
    if chosen > secret_number and  not(count <= 0) :
            print "your chosen number was higher!"
      
    elif chosen == secret_number:
            print "You got it correct.The secret_number was",secret_number
            print "You can select range to play again"
            print " "
            
    elif   not(count <= 0):
            print "your chosen number was lower!"
    print " "   
    
       
    if (count == 0) and not(secret_number == chosen):
        print "You ran out of guesses.Do not enter anymore numbers"
        print "The ans was",secret_number
        print "Restarting the game"
        print " "
        
        init()
      
# create frame

f = simplegui.create_frame("Guess the number", 200, 200)
# register event handlers for control elements
f.add_button("Range is [0,100)", range100, 200) 
f.add_button("Range is [0,1000)", range1000, 200)
f.add_input("Enter a guess", get_input,100)             

init()
    
# start frame

f.start()
# always remember to check your completed program against the grading rubric
