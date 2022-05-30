from __future__ import annotations
from typing import List
from logic import *
from logic import Stack as s



# setup initial ss with main deck as deal pile, human_deck, computer_deck.
deal_pile:list[Card] = build_deck()
shuffle(deal_pile)
human_deck: List[Card] = []
computer_deck: List[Card] = []
s(human_deck)
s(computer_deck)
build_hand(deal_pile,human_deck)
print(show_hand(human_deck))

