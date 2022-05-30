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
# figure out why this doesn't work:
    # deal_stack = s("Deal Pile", deal_stack)
human_stack = s("Human's hand", human_stack)
computer_stack = s("Computer's Hand", computer_stack)
discard_stack = s("discard pile", discard_stack)
build_hand(deal_stack,human_stack)
build_hand(deal_stack,computer_stack)
transfer(deal_stack,discard_stack,0,0)

game = Game(human_stack, computer_stack, discard_stack,0, True)

while game.cabo_called == False:
    g.start_turn(game)
    print(human_stack.retrieve_score())
    transfer(human_stack,discard_stack,1,0)
    transfer(deal_stack,human_stack,0,1)
    g.end_turn(game)

    print(g.cabo_state(game))

    g.start_turn(game)
    print(computer_stack.retrieve_score())
    g.end_turn(game)

    g.start_turn(game)
    print(computer_stack.retrieve_score())
    g.end_turn(game)

    g.call_cabo(game)
    print(f"Was cabo called? {g.cabo_state(game)}")

    g.end_turn(game)

    


