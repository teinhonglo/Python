# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random

secret_number = 0
remaining = 7
# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    secret_number = 0   
    print ""
    range100()

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global secret_number
    secret_number = random.randint(0,100)
    global remaining
    remaining = 7
    print "New Game.Range is frome 0 to 100"
    print "Nmber of remaining guess is ",remaining
    print ""

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global secret_number
    secret_number = random.randint(0,1000)
    global remaining
    remaining = 10
    print "New Game.Range is frome 0 to 1000"
    print "Nmber of remaining guess is ",remaining
    print ""
    
def input_guess(guess):
    # main game logic goes here	
    print 'Guess was ' + guess
    guess_num = int(guess)
    
    global remaining
    remaining -= 1
    print 'Number of remainder guess ' + str ( remaining )
    if( remaining > 0 ):
        if ( guess_num > secret_number ) :
            print 'Higher'
        elif ( guess_num < secret_number ) :
            print 'Lower'
        else :
            print 'Correct'
            new_game()
    else :
        print "You run out of guess, The number is",secret_number
        new_game()
    print ""
    
# create frame
frame = simplegui.create_frame("guess_number",200,200)

# register event handlers for control elements and start frame
frame.add_button("rand100",range100,200)
frame.add_button("rand1000",range1000,200)
frame.add_input("guess_number",input_guess,200)

# call new_game 
frame.start()
new_game()


# always remember to check your completed program against the grading rubric
