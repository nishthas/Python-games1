http://www.codeskulptor.org/#user15_7bgj4dJVoqvsOlR_0.py

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
score=0
in_play = False
outcome = ""
score = 0
phand=None
dhand=None
u=0
y=0
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
    
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.inhand=[]
        
    def __str__(self):
        # return a string representation of a hand
        ans=""
        for i in range(len(self.inhand)):
            ans +=" "+str(self.inhand[i])
        return "Hand contains"+ans
        
    def add_card(self, card):
        # add a card object to a hand
        self.inhand.append(card)   
    
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        handvalue=0
        flag=0
        for card in self.inhand:
            handvalue+=VALUES[card.get_rank()]
            if VALUES[card.get_rank()]==1:
                flag =1
        if handvalue+10<=21 and flag ==1:
            handvalue+=10
        return handvalue
    
    
    def draw(self, canvas, pos):
         # draw a hand on the canvas, use the draw method for cards
         
         for card in self.inhand:
            card.draw(canvas,pos)
            pos[0] += 80
                
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck=[]
        for suit in SUITS: 
            for rank in RANKS:
                self.cardy=Card(suit,rank)
                self.deck.append(self.cardy)
    
    def shuffle(self):
        # add cards back to deck and shuffle
        # use random.shuffle() to shuffle the deck
        random.shuffle(self.deck)
    
    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
        
    
    def __str__(self):
        # return a string representing the deck
        ans=""
        for i in range(len(self.deck)):
            ans +=" "+str(self.deck[i])
        return "Deck contains"+ans
        
# assign a message to outcome, update in_play and score
def deal():
    global phand,dhand,deck,in_play,score
    if in_play==True:
        score-=1
    in_play=True
    deck = Deck()
    deck.shuffle()
    phand = Hand()
    dhand = Hand()
    for i in range(0,2):
        phand.add_card(deck.deal_card())
        dhand.add_card(deck.deal_card())
    print phand
    print dhand

def hit():
    global phand,deck,in_play,y,u,score
    
    if phand.get_value()<21 and in_play:
        
        phand.add_card(deck.deal_card())
        print phand
    else:
            
            print "you busted"
            u=0
            y=1
            if in_play:	
                score-=1
            in_play=False
   
def stand():    
    global dhand,deck,in_play,phand,u,y,score
   
    if in_play==False:
        print "YOU BUSTED.NO PLAY NOW"
        u=0
    else:

        if dhand.get_value()>=17 and dhand.get_value()<=21 and dhand.get_value()>=phand.get_value():
            print "dealer wins"
            u=0
            y=1
            score-=1
            in_play=False
        else:
         while dhand.get_value()<17 :
            dhand.add_card(deck.deal_card())
            print dhand
         if dhand.get_value()>=phand.get_value()and dhand.get_value()<=21:
                print "dealer wins"
                u=0
                y=1
                score-=1
                in_play=False
         else:
                print "player wins"
                y=0
                u=1
                score+=1
                in_play=False
            
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global score,phand,dhand,CARD_BACK_CENTER, CARD_SIZE,CARD_BACK_SIZE,in_play,u,y
    canvas.draw_text("Dealer",[70,90],40,"black")
    canvas.draw_text("Player",[70,300],40,"black")
    canvas.draw_text("BlackJack",[180,50],60,"Black")
    canvas.draw_text("Score="+str(score),[180,350],40,"black")
    if phand!=None:
        phand.draw(canvas,[50,400])
    if dhand!=None:
        dhand.draw(canvas,[50,100])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                       [88,150], CARD_BACK_SIZE)
        canvas.draw_text("Hit or Stand?",[300,300],40,"black")
    else:
        canvas.draw_text("New Deal?",[300,300],40,"black")
        if u:
            canvas.draw_text("You win",[250,550],40,"black")
        if y:
            canvas.draw_text("You lose",[250,550],40,"black")
        

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
frame.start()


# remember to review the gradic rubric