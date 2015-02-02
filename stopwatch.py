http://www.codeskulptor.org/#user12_5Hw004hRSEXjs3y_0.py

# template for "Stopwatch: The Game"
import simplegui
# define global variables
stopped=False
started=False
counter=0
a=0
b=0
c=0
d=0
x=0
y=0
# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
        global a, b, c, d
        a=t//600
        d=t%10
        y=t//10
        c=y%10
        u=y%60
        b=u//10
        return str(a)+":"+str(b)+str(c)+"."+str(d)	

def score():
   global x,y
   return str(x)+"/"+str(y) 


# define event handlers for buttons; "Start", "Stop", "Reset"

def start(): 
    global started
    started=True
    timer.start()

def stop():
     global started
     if started :
        global x,y
        y=y+1
        if counter%10==0:
            x=x+1
        timer.stop()
     started=False
        
def reset():
    global counter,started,x,y
    counter=0
    x=0
    y=0
    started=False
    timer.stop()

# define event handler for timer with 0.1 sec interval
def timer_handler() :
    global counter
    counter=counter+1

# define draw handler
def draw(canvas):
    global counter
    canvas.draw_text(format(counter),[75,150],50,"white")
    canvas.draw_text(score(),[240,35],35,"red")
   
# create frame
frame = simplegui.create_frame("STOPWATCH", 300, 300) 

# Register Event Handlers
frame.set_draw_handler(draw)

label = frame.add_label("Get ready...")
frame.add_label("Press 'stop'as close as possible to an integer possible to win")
frame.add_button("Start",start , 75)
frame.add_button("Stop", stop, 75)
frame.add_button("Reset", reset, 75)
timer=simplegui.create_timer(100, timer_handler)
# start frame
frame.start()

# Please remember to review the grading rubric
