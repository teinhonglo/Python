# implementation of card game - Memory

import simplegui
import random

WIDTH = 800
HEIGHT = 100

memory = []
exposed = []
turns = 0

first_card = -1
second_card = -1

# helper function to initialize globals
def new_game():
    global memory
    global turns
    global exposed
    global state
    global first_card
    global second_card
    
    # init state
    state = 0
    memory = []
    exposed = []
    item= [1,2,3,4,5,6,7,8]
    
    # shuffle one times
    random.shuffle(item)
    memory.extend(item)
    
    # shuffle two times
    random.shuffle(item)
    memory.extend(item)
    
    random.shuffle(item)
    
    # init exposed
    for num in memory :
        exposed.append(False)
    
    # init attempt times
    turns = 0
    
    # init track of postion
    first_card = -1
    second_card = -1
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed
    global state
    global first_card
    global second_card
    global turns
    # first, should be in area
    if ( pos[1] >=0 and pos[1] <= HEIGHT ) and ( pos[0] >= 0 and pos[0] <= WIDTH ) :
        # second, cannot touch the same card again
        if not exposed [ pos[0] // 50 ] :
            if state == 0 :
                exposed [ pos[0] // 50 ] = True
                first_card = pos[0] // 50 
                state = 1
            elif state == 1 :
                exposed [ pos[0] // 50 ] = True
                second_card = pos[0] // 50 
                state = 2
            else :
                if memory[first_card] != memory[second_card] :
                    exposed[first_card] = False
                    exposed[second_card] = False
                state = 0
                turns += 1
                mouseclick(pos)
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    # text position
    text_hor =  WIDTH // 16 // 2 - 15
    text_ver = HEIGHT // 2 + 20
    text_hor_interval = WIDTH // 16
    
    for num in memory :
        canvas.draw_text(str(num), [text_hor, text_ver], 70, 'White')
        text_hor += text_hor_interval
    
    # init the green card
    card_hor = WIDTH // 16 // 2
    card_ver = HEIGHT
    # draw the green card
    for exp in exposed :
        if not exp :
            canvas.draw_line( (card_hor,0), (card_hor,card_ver), 50 , 'Green')
        card_hor += 50
    
    # init the red line
    line_hor = WIDTH // 16 // 2
    line_ver = HEIGHT 
    canvas.draw_line( (0,0), (0,line_ver),5 , 'Red')
    # draw the red line
    for exp in exposed :
        canvas.draw_line( (line_hor + 25,0), (line_hor + 25,line_ver),5 , 'Red')
        line_hor += 50
    
    # count the attempt times
    label.set_text("Turns = " + str(turns))

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(turns))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric