# template for "Stopwatch: The Game"
import simplegui
# define global variables
interval = 100
total_seconds = 0
width = 400
height = 300
isUpdate = False
success = 0
attempt = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    fromat_str = ""
    minutes = 0
    tenths_of_seconds = t % 10
    seconds = ( t - tenths_of_seconds ) // 10
    
    if seconds > 60 :
        seconds -= 60
        minutes += 1
    
    if seconds < 10 :
        return str(minutes) + ":0" + str(seconds) + "." + str(tenths_of_seconds)
    else :
        return str(minutes) + ":" + str(seconds) + "." + str(tenths_of_seconds)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button():
    global isUpdate
    isUpdate = True

def stop_button():
    global isUpdate
    global success
    global attempt
    if isUpdate :
        isUpdate = False
        if total_seconds % 10 == 0 :
            success += 1

        attempt += 1

def reset_button():
    global total_seconds
    global isUpdate
    global success
    global attempt
    total_seconds = 0
    isUpdate = False
    success = 0
    attempt = 0
    
# define event handler for timer with 0.1 sec interval
def tick():
    if isUpdate :
        global total_seconds
        total_seconds +=1

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(str(success) + "/" + str(attempt) ,(  width * 4 / 5 , height / 5 ) ,25 ,"Green")
    canvas.draw_text(str(format(total_seconds)) ,( width * 2 / 5 ,height / 2 ) ,45 ,"Red")
    
# create frame
frame = simplegui.create_frame("StopWatch",width,height)

# register event handlers
frame.set_draw_handler(draw_handler)
frame.add_button("Start",start_button,200)
frame.add_button("Stop",stop_button,200)
frame.add_button("Reset",reset_button,200)
timer = simplegui.create_timer(interval,tick)


# start frame
frame.start()
timer.start()

# Please remember to review the grading rubric
