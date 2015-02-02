http://www.codeskulptor.org/#user14_g1GmNTJCH2yp9Jl_2.py

# implementation of card game - Memory

import simplegui
import random
counts=0
# helper function to initialize globals
def init():
    global list,pos,posrec,poslin,exposed,state,a,b,counts
    list1=range(8)
    list2=range(8)
    list=list1+list2
    pos=[0,80]
    posrec=[0,50]
    poslin=[0,0]
    state=0
    counts=0
    label.set_text("Move="+str(counts))
    random.shuffle(list)
    exposed=[False,False, False,False,False,False,False, False,
             False,False,False,False, False,False,False,False]
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global i,exposed,state,a,b,counts
    i=0
    i= pos[0]//50
    if not exposed[i]:
     if state == 0:
        a=i
        state = 1
     elif state == 1:
        b=i
        counts+=1
        label.set_text("Moves="+str(counts))
        state = 2
     else:
        if list[a]==list[b]:
            exposed[a]=True
            exposed[b]=True
            a=i
        elif list[i]==list[a]:
            exposed[a]=True
            exposed[i]=True
            a=b
        elif list[i]==list[b]:
            exposed[b]=True
            exposed[i]=True
        else:
            exposed[a]=False
            exposed[b]=False
            a=i
        state=1
    exposed[i]=True 
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global pos,posrec,poslin,exposed,i,a,b,counts
    pos[0]=0
    posrec[0]=0
    poslin[0]=0
    for i in range(16):
        if exposed[i]==True:
            canvas.draw_text(str(list[i]),pos,80,"white")
        pos[0]=pos[0]+50
        if exposed[i]==False:
            canvas.draw_line(posrec,[posrec[0]+50,50],100,"green")
        posrec[0]+=50
        canvas.draw_line([poslin[0],0],[poslin[0],100],1,"black")
        poslin[0]+=50
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()


# Always remember to review the grading rubric