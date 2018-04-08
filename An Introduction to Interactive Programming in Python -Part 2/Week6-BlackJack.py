# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

card_back_alt = simplegui.load_image(
        'http://images.all-free-download.com/images/graphiclarge/poker_background_3d_design_red_ribbon_cards_decoration_6829319.jpg')
ALT_SIZE = [600, 598]
ALT_CENTER = [600 // 2, 598 // 2]

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

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
        self.cards = []
        pass	# create Hand object

    def __str__(self):
        ans = " "
        for i in range(len(self.cards)):
            ans += str(self.cards[i]) + " "
        return "Hand contains" + ans 
        pass	# return a string representation of a hand

    def add_card(self, card):
        return self.cards.append(card)
        pass	# add a card object to a hand

    def get_value(self):
        self.value = 0
        #Has_Ace = False
        for card in self.cards:
            self.value += VALUES[card.get_rank()]
        for card in self.cards:
            #self.value += VALUES[card.get_rank()]
            if card.get_rank() == RANKS[0]:
                #Has_Ace = True
                if self.value + 10 <= 21:                   
                     return self.value + 10
                else:                    
                     return self.value        
            else:
                 return self.value
        return self.value
             
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        pass	# compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        for card in self.cards:
            #pos[0] += 90
            card.draw(canvas, pos)
            pos[0] += 90
        pass	# draw a hand on the canvas, use the draw method for cards
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))      
        pass	# create a Deck object

    def shuffle(self):
        return random.shuffle(self.deck)
        # shuffle the deck 
        pass    # use random.shuffle()

    def deal_card(self):
        return random.choice(self.deck)
        pass	# deal a card object from the deck
    
    def __str__(self):
        ans = " "
        for i in range(len(self.deck)):
            ans += str(self.deck[i]) + " "
        return "Hand contains" + ans
        pass	# return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand,deck, score
    
    if in_play:
        outcome =  "You lose! new deal?"
        in_play = False
        score -= 1
        
    player_hand = Hand()
    dealer_hand = Hand()
    deck = Deck()
    deck.shuffle()
    
    for i in range(2):
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
    
    # your code goes here
    outcome = "Hit or Stand?"
    in_play = True

def hit():
    global outcome, in_play, score
    pass	# replace with your code below
 
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You busted! Deal Again?"
            in_play = False
            score -= 1
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global in_play, outcome, score
    pass	# replace with your code below
    if in_play:
        while dealer_hand.get_value() <= 17:            
            dealer_hand.add_card(deck.deal_card())
            
        if dealer_hand.get_value() > 21:
            outcome = "You win! Deal again?"
            in_play = False
            score += 1
        else:
            if dealer_hand.get_value() >= player_hand.get_value():
                outcome = "Dealer win! Deal again?"
                in_play = False
                score -= 1
            else:
                outcome = "You win! Deal Again?"
                in_play = False
                score += 1
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global in_play
    canvas.draw_text("WELCOME TO BLACKJACK!", [20, 60], 30, "Black")
    canvas.draw_text("Dealer", [32, 200], 25, "Black")
    canvas.draw_text("Player", [32, 400], 25, "Black")
    canvas.draw_text("Score: " + str(score), [370, 150], 30, "Orange")
    canvas.draw_text(outcome, [180, 350], 30, "Blue")
    
    dealer_hand.draw(canvas, [120, 180])
    player_hand.draw(canvas, [120, 380])
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          [120 + CARD_CENTER[0], 180 + CARD_CENTER[1]], CARD_SIZE)
        
        canvas.draw_image(card_back_alt, ALT_CENTER, ALT_SIZE, 
                          [120 + CARD_CENTER[0], 180 + CARD_CENTER[1]], CARD_SIZE)
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
