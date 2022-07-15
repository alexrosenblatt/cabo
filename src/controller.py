from __future__ import annotations
from typing import List
from model import *
from model import Stack as s
from view import *

# setup initial ss with main deck as deal pile, human_stack, computer_stack.
deal_stack = build_deck()
player_1 = s("Player 1 hand", None)
player_2 = s("Player 2 Hand", None)
discard_stack = s("discard pile", None)

# pull cards from deal stack and create human,computer hands + discard pile
shuffle(deal_stack)
build_hand(deal_stack, player_1)
build_hand(deal_stack, player_2)
make_transfer(deal_stack, discard_stack, 0, 0)


def card_count_2():  #for testing against losing a card
    count = len(deal_stack) + len(human_stack) + len(discard_stack) + len(
        computer_stack)
    if count > 54:
        return ValueError("Too many Cards in play.")


# main routine
game = Game({player_1, player_2}, discard_stack, deal_stack, 1, True, False, 1)
#Game.initialize_game(game)
while not game.cabo_called:
    Game.human_turn(game)
    Game.computer_turn(game)
    Game.end_turn(game)
    card_count_2()
