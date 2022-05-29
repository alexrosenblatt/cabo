from logic import *
from logic import Stack as s



# setup initial ss with main deck as deal pile, human_deck, computer_deck.
deal_pile:list = build_deck()
s.shuffle(deal_pile)
human_deck = []
computer_deck = []
s(human_deck)
s(computer_deck)
build_hand(deal_pile,human_deck)
s.show_hand(human_deck)

