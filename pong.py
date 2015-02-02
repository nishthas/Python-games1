http://www.codeskulptor.org/#user13_0qdPPsZmr6MuwiG_2.py

# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
s=0.1
x=0
y=0

right=True
# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos=[WIDTH/2,HEIGHT/2]
    u=random.randrange(120, 240)
    t=random.randrange(60, 180)
    if right:
         ball_vel=[u/60,-t/60]
    else:
        ball_vel=[-u/60,-t/60]
    
# define event handlers
def player1():
    global x
    return str(x)
def player2():
    global y
    return str(y)
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global x,y # these are ints
    paddle1_pos=200.0
    paddle2_pos=200.0
    paddle1_vel=0.0
    paddle2_vel=0.0
    x=0
    y=0
    ball_init(random.choice([True, False]))

    
def draw(c):
    global x,y,right, paddle1_pos, paddle2_pos, ball_pos, ball_vel ,paddle1_vel, paddle2_vel
    
    # update paddle's vertical position, keep paddle on the screen
 
    if paddle1_pos + paddle1_vel >= HALF_PAD_HEIGHT:       
            paddle1_pos += paddle1_vel
    if paddle2_pos+paddle2_vel >= HALF_PAD_HEIGHT :
            paddle2_pos+=paddle2_vel
    if paddle1_pos + paddle1_vel >=HEIGHT- HALF_PAD_HEIGHT+1:       
            paddle1_pos -= paddle1_vel
    if paddle2_pos+paddle2_vel >=HEIGHT- HALF_PAD_HEIGHT+1:
            paddle2_pos-=paddle2_vel
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    
    # draw paddles
    c.draw_line([0,paddle1_pos],[PAD_WIDTH,paddle1_pos],80,"white")
    c.draw_line([WIDTH-PAD_WIDTH,paddle2_pos],[WIDTH,paddle2_pos],80,"white")
    
    # update ball
   
    ball_pos[0] += ball_vel[0]
    ball_pos[1]+=ball_vel[1]
    
    
    if ball_pos[1]< BALL_RADIUS:
        ball_vel[1]=-ball_vel[1]
    if ball_pos[1]>HEIGHT-BALL_RADIUS:
        ball_vel[1]=-ball_vel[1]
    if ball_pos[0]-BALL_RADIUS<PAD_WIDTH:
        if ball_pos[1]>paddle1_pos-HALF_PAD_HEIGHT and ball_pos[1]< paddle1_pos+HALF_PAD_HEIGHT:
            ball_vel[0]=-ball_vel[0]
            ball_vel[0]=ball_vel[0]+s*ball_vel[0]
            
        else:
            y=y+1
            right=True
            ball_init(right)
        
    if ball_pos[0]+BALL_RADIUS>WIDTH-PAD_WIDTH:   
        if ball_pos[1]>paddle2_pos-HALF_PAD_HEIGHT and ball_pos[1]< paddle2_pos+HALF_PAD_HEIGHT:
            ball_vel[0]=-ball_vel[0]
            ball_vel[0]=ball_vel[0]+s*ball_vel[0]
            
        else:
            x=x+1
            right=False
            ball_init(right)
    # draw ball and scores
    c.draw_circle(ball_pos,BALL_RADIUS,5,"white","white")    
    c.draw_text(player1(),[200,50],45,"white")
    c.draw_text(player2(),[500,50],45,"white")
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc=4
    if key == simplegui.KEY_MAP['down']:
         paddle2_vel+=acc
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel-=acc
    elif key == simplegui.KEY_MAP['w']:
         paddle1_vel-=acc  
    elif key == simplegui.KEY_MAP['s']:
         paddle1_vel+=acc  
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['down']:
         paddle2_vel=0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel=0
    elif key == simplegui.KEY_MAP['w']:
         paddle1_vel=0 
    elif key == simplegui.KEY_MAP['s']:
         paddle1_vel=0 
    

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("restart",new_game)

# start frame
new_game()
frame.start()
