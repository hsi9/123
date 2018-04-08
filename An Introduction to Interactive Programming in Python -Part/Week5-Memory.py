# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global cards, exposed, state, previous_click, turns
    numbers = "0011223344556677"
    cards = list(numbers)
    exposed = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    random.shuffle(cards)
    previous_click = []
    state = 0
    turns = 0
    label.set_text("Turn = 0")
    pass  

     
# define event handlers
def mouseclick(pos):
    global state, previous_click, exposed, turns
    #previous_click = []
    
    n = pos[0] // 50
    
    if exposed[n] == 0:
        
        if state == 0:
            state = 1
            #label.set_text("Turn = 0")
        elif state == 1:       
            state = 2
            turns += 1
            label.set_text("Turn = "+str(turns))
        else: 
            if cards[previous_click[-1]] != cards[previous_click[-2]]:
                exposed[previous_click[-1]] = 0
                exposed[previous_click[-2]] = 0
                
            #first = previous_click.pop()
            #second = previous_click.pop()
            #if cards[first]!= cards[second]:
            #    exposed[first] = 0
            #    exposed[second] = 0
            state = 1

        previous_click.append(n)
        exposed[n] = 1
    
    
    pass
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for card_index in range(len(cards)):
        card_pos = 50 * card_index
        canvas.draw_text(str(cards[card_index]), [card_pos,70], 60, "White")  
        
    #exposed = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #status = False
    for i in range(len(exposed)):
        if exposed[i] == 0:
            position = 50 * i
            #status = False
            canvas.draw_polygon([[0 + position,0],[50 + position,0],[50 + position,100],[0 + position,100]],1,"Black","Green")
        else:
            #status = True
            position = 50 * i
            canvas.draw_polygon([[0 + card_pos,0],[50 + card_pos,0],[50 + card_pos,100],[0 + card_pos,100]],1,"Black")                            
    #if (pos[0] > 50 * i) and (pos[0] <= 50 + 50 * i):
    #    canvas.draw_polygon ([[0 + card_pos,0],[50 + card_pos,0],[50 + card_pos,100],[0 + card_pos,100]],1,"Black","Red")
    pass


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")
#label.set_text("Turn = "+str(turns))
# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
