from __future__ import annotations
from typing import List
from model import *
from model import Stack as s
from game import Game
from view import *



# setup initial ss with main deck as deal pile, human_stack, computer_stack.
deal_stack = build_deck()

human_stack = s("Human's hand",None)
computer_stack = s("Computer's Hand", None)
discard_stack = s("discard pile", None)

# pull cards from deal stack and create human,computer hands + discard pile
shuffle(deal_stack)
build_hand(deal_stack,human_stack)
build_hand(deal_stack,computer_stack)
make_transfer(deal_stack,discard_stack,0,0)

def card_count_2(): #for testing against losing a card
    count = len(deal_stack)+len(human_stack)+len(discard_stack)+len(computer_stack)
    if count > 54:
        return ValueError("Too many Cards in play.")


game = Game(human_stack, computer_stack, discard_stack,deal_stack,1, True,False)
#Game.initialize_game(game)
while game.cabo_called == False:
    Game.human_turn(game)
    Game.end_turn(game)
    card_count_2()
        
   
    
