from __future__ import annotations
from typing import List
from model import *
from model import Pile as s
from view import *

# setup initial ss with main deck as deal pile, human_stack, computer_stack.

# pull cards from deal stack and crea1te human,computer hands + discard pile


def print_currentstate():
    for player in game.player_list:
        print(f"{player.name}'s pile:{player.pile}")
        print(f"{player.name}'s memory:{player.memory}")
    print(f"{game.discard_pile}")
    print(f"{game.deal_pile}")


game = Game()
game.initialize_game()

print_currentstate()

while not game.cabo_called:
    for player in game.player_list:
        if player.type == 0:
            Game.start_turn(game, player)
        elif player.type == 1:
            Game.start_turn(game, player)
    Game.end_turn(game)
