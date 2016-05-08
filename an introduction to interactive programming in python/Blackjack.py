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

# initialize some useful global variables
in_play = False
outcome = "in play"
score = 0
first_round = True
card_interval = 30
win = 0
lose = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

HEIGHT = 600
WIDTH = 600

dealer_first_card_pos = [WIDTH / 6, HEIGHT / 5]
player_first_card_pos = [WIDTH / 6, HEIGHT * 19 / 30]

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
        self.card_list = []
        self.has_ace = False
    def __str__(self):
        # return a string representation of a hand
        ret_str = ""
        for i in range(len(self.card_list)) :
            ret_str = ret_str + str(self.card_list[i]) + " "
            
        return "Hand contains " + ret_str

    def add_card(self, card):
        self.card_list.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        has_ace = self.has_ace 
        hand_value = 0
        
        for cards in self.card_list :
            hand_value += VALUES[cards.get_rank()]
            if cards.get_rank() == "A" and not has_ace:
                has_ace = True
        
        if has_ace :
            if hand_value + 10 <= 21 :
                return hand_value + 10
            else :
                return hand_value
        else :
            return hand_value
        
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        count = 0
        for cards in self.card_list :
            cards.draw(canvas, [pos[0] + count * card_interval, pos[1]])
            count += 1
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck_list = []
        self.string = ""
        for suit in SUITS :
            for rank in RANKS :
                self.deck_list.append(Card(suit, rank))
                                      
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck_list)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck_list.pop()
    
    def __str__(self):
        ret_str = "Deck contains "
        for cards in self.deck_list :
            ret_str += str(cards) + " "
        
        return ret_str


#define event handlers for buttons
def deal():
    global outcome, in_play, score, lose
    global cur_deck, player_hands, dealer_hands, outcome ,first_round
    
    if not in_play :
        outcome = "Hit or Stand?"
        in_play = True
    else :
        outcome = "lose the round"
        lose += 1
        in_play = False
    
    player_hands = Hand()
    dealer_hands = Hand()
    cur_deck = Deck()
    cur_deck.shuffle()
    # add two cards for both 
    dealer_hands.add_card(cur_deck.deal_card())
    player_hands.add_card(cur_deck.deal_card())
    dealer_hands.add_card(cur_deck.deal_card())
    player_hands.add_card(cur_deck.deal_card())
    
    first_round = False

def hit():
    # if the hand is in play, hit the player
    global in_play, player_hands, cur_deck, score, outcome, win, lose
    
    if in_play :
        player_hands.add_card(cur_deck.deal_card())
    
    # if busted, assign a message to outcome, update in_play and score
    if in_play and player_hands.get_value() > 21 :
        lose += 1
        outcome = "player burst!!"
        in_play = False
    
def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    global in_play, dealer_hands, score, outcome, win, lose
    
    if in_play :
        while dealer_hands.get_value() < 17:
            dealer_hands.add_card(cur_deck.deal_card())

        # assign a message to outcome, update in_play and score
        if dealer_hands.get_value() > 21 :
            outcome = "dealer burst!!"
            win += 1
        else :
            if player_hands.get_value() <= dealer_hands.get_value():
                lose += 1
                outcome = "dealer win!!"
            else :
                win += 1
                outcome = "player win!!"

    in_play = False
# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player_hands, dealer_hands
    
    if not first_round :
        dealer_hands.draw(canvas, dealer_first_card_pos)
        player_hands.draw(canvas, player_first_card_pos)
        canvas.draw_text("Player: " + str(player_hands.get_value()) , [WIDTH * 7 / 12, HEIGHT * 13 / 20], 35 ,"White")
    
    if in_play :
        card_loc = (CARD_BACK_CENTER[0], 
                    CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, 
                          [dealer_first_card_pos[0] + CARD_BACK_CENTER[0] + card_interval, dealer_first_card_pos[1] + CARD_BACK_CENTER[1]],CARD_SIZE)
    score = win - lose    
    canvas.draw_text("Status: " + outcome , [WIDTH * 6 / 12, HEIGHT / 12], 30 ,"White")
    canvas.draw_text("Score: " + str(score) , [WIDTH / 12, HEIGHT / 12], 50 ,"White")
    canvas.draw_text("Win: " + str(win) , [WIDTH / 12, HEIGHT * 9 / 10], 25 ,"White")
    canvas.draw_text("Lose: " + str(lose) , [WIDTH * 8 / 12, HEIGHT * 9 / 10], 25 ,"White")
    canvas.draw_text("Blackjack", [WIDTH / 4 , HEIGHT / 2], 60 ,"Yellow")
    canvas.draw_text("Dealer:", [WIDTH / 6 , HEIGHT / 6], 30 ,"Yellow")
    canvas.draw_text("Player:", [WIDTH / 6 , HEIGHT * 3 / 5], 30 ,"Yellow")
    
    if not in_play and not first_round :
        canvas.draw_text("Dealer:" + str(dealer_hands.get_value()), [WIDTH * 7 / 12, HEIGHT * 7 / 20], 35 ,"White")
        canvas.draw_text("Next deal?", [WIDTH * 6 / 12, HEIGHT * 3 / 12], 30 ,"Red")

# initialization frame
frame = simplegui.create_frame("Blackjack", WIDTH, HEIGHT)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
deal()

# remember to review the gradic rubric