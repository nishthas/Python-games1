# Rock-paper-scissors-lizard-Spock template
import random

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def number_to_name(number):
    # fill in your code below
    if number == 0:
        print "computer chooses rock"
    elif number == 1:
        print "computer chooses spock"
    elif number == 2:
        print "computer chooses paper"
    elif number == 3:
        print "computer chooses lizard"
    elif number == 4:
        print "computer chooses scissors"
      
        
    # convert number to a name using if/elif/else
    # don't forget to return the result!

    
def name_to_number(name):
    # fill in your code below
    print "player chooses",name
    if name == "rock":
        return 0
    elif name == "Spock":
         return 1
    elif name== "paper":
          return 2
    elif name== "lizard":
          return 3
    elif name== "scissors":
          return 4
    else :
          print "invalid choice"
    # convert name to number using if/elif/else
    # don't forget to return the result!


def rpsls(name): 
    # fill in your code below

    # convert name to player_number using name_to_number
    player_number =	name_to_number(name)
    # compute random guess for comp_number using random.randrange()
    comp_number= random.randrange(0,5)
    # compute difference of player_number and comp_number modulo five
    difference= player_number - comp_number
    remain= difference%5
    # use if/elif/else to determine winner

    # convert comp_number to name using number_to_name
    number_to_name(comp_number)
    # print results
    if (remain == 1) or (remain== 2):
        print "Player wins"
    elif (remain ==3) or (remain==4):
        print "computer wins"
    else :
        print "Player and computer tie"
    print " "
# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric

