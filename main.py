from __future__ import annotations
from typing import List
from logic import *
from logic import Stack as s
from logic import Game as g



# setup initial ss with main deck as deal pile, human_stack, computer_stack.

deal_stack:list[Card] = build_deck()
setup_card = Card("blank")
human_stack = s("Human's hand",[setup_card])
computer_stack: list[Card]  = []
discard_stack: list[Card]  = []
# TODO figure out why this doesn't work:
    # deal_stack = s("Deal Pile", deal_stack)
#human_stack = s("Human's hand", human_stack)  # TODO figure out type errors here
computer_stack = s("Computer's Hand", computer_stack)
discard_stack = s("discard pile", discard_stack)

# pull cards from deal stack and create human,computer hands + discard pile
shuffle(deal_stack)
build_hand(deal_stack,human_stack)
build_hand(deal_stack,computer_stack)
transfer(deal_stack,discard_stack,0,0)

def card_count_2():
    count = len(deal_stack)+len(human_stack)+len(discard_stack)+len(computer_stack)
    return count

game = Game(human_stack, computer_stack, discard_stack,deal_stack,0, True)
    #g.initialize_game(game)
while card_count_2() == 54:
    g.start_round(game)
    g.human_turn(game)
    g.end_round(game)
    g.start_round(game)
    g.human_turn(game)
    g.end_round(game)
    g.start_round(game)
    g.human_turn(game)
    g.end_round(game)
    g.start_round(game)
    g.human_turn(game)
    g.end_round(game)
    g.start_round(game)
    g.human_turn(game)
    g.end_round(game)



#print(s.retrieve_score(human_stack))