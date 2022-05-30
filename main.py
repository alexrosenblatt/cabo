from __future__ import annotations
from typing import List
from logic import *
from logic import Stack as s
from logic import Game as g



# setup initial ss with main deck as deal pile, human_stack, computer_stack.

deal_stack:list[Card] = build_deck()
shuffle(deal_stack)
human_stack: List[Card] = []
computer_stack: List[Card] = []
discard_stack: List[Card] = []
human_stack = s("Human's hand", human_stack)
computer_stack = s("Computer's Hand", computer_stack)
discard_stack = s("discard pile", discard_stack)
build_hand(deal_stack,human_stack)
build_hand(deal_stack,computer_stack)
transfer(deal_stack,discard_stack,0,0)

game = Game(human_stack, computer_stack, discard_stack)

while game.cabo_called == False:
    g.start_turn(game)
    print(human_stack.retrieve_score())
    transfer(human_stack,discard_stack,1,0)
    transfer(deal_stack,human_stack,0,1)
    #g.turn_count = end_turn(turn_count)

    print(g.cabo_state(game))

    g.start_turn(game)
    print(computer_stack.retrieve_score())

    print(g.cabo_state(game))

    g.start_turn(game)
    print(computer_stack.retrieve_score())

    g.call_cabo(game)

    


