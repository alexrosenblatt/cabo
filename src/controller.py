from __future__ import annotations
from typing import List
from model import *
from model import Pile as s
from view import *

# setup initial ss with main deck as deal pile, human_stack, computer_stack.

# pull cards from deal stack and crea1te human,computer hands + discard pile

# def check_card_count():  #for testing against losing a card
#     total_card_count = len(deal_pile) + len(human_pile) + len(
#         discard_pile) + len(computer_pile)
#     if total_card_count > 54:
#         return ValueError("Too many Cards in play.")

# main routine
# game = Game(
#     human_pile,
#     computer_pile,
#     discard_pile,
#     1,
#     True,
#     False,
# )


def print_currentstate():
    for player in game.player_list:
        print(f"{player.name}'s pile:{player.pile}")
        print(f"{player.name}'s memory:{player.memory}")
    print(f"{game.discard_pile}")
    print(f"{game.deal_pile}")


game = Game()
game.initialize_game()

print_currentstate()
2
while not game.cabo_called:
    for player in game.player_list:
        if player.type == 0:
            Game.start_turn(game, player)
        elif player.type == 1:
            Game.start_turn(game, player)
    Game.end_turn(game)
