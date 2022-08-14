from __future__ import annotations
from typing import List
from model import *
from model import Stack as s
from view import *

# setup initial ss with main deck as deal pile, human_stack, computer_stack.
deal_pile = build_deck()
human_pile = s("Human's hand", None)
computer_pile = s("Computer's Hand", None)
discard_pile = s("discard pile", None)

# pull cards from deal stack and create human,computer hands + discard pile
shuffle(deal_pile)
build_hand(deal_pile, human_pile)
build_hand(deal_pile, computer_pile)
make_transfer(deal_pile, discard_pile, 0, 0)
# TODO refactor this to the right place
computer_pile_memory = s("computer_pile_memory", None)
computer_pile_memory.insert(0, computer_pile[0])
computer_pile_memory.insert(1, computer_pile[1])


def check_card_count():  #for testing against losing a card
    total_card_count = len(deal_pile) + len(human_pile) + len(
        discard_pile) + len(computer_pile)
    if total_card_count > 54:
        return ValueError("Too many Cards in play.")


# main routine
game = Game(
    human_pile,
    computer_pile,
    discard_pile,
    deal_pile,
    computer_pile_memory,
    1,
    True,
    False,
)
#Game.initialize_game(game)
while not game.cabo_called:
    Game.start_human_turn(game)
    Game.computer_turn(game)
    Game.end_turn(game)
    check_card_count()
