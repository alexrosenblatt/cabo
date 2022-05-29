from cardclass import Card
from stack import *
from stack import Stack as s
import random
import constants as c



# setup initial ss with main deck as deal pile, human_deck, computer_deck.
deal_pile = build_deck()
s.shuffle(deal_pile)
human_deck = []
computer_deck = []
s(human_deck)
s(computer_deck)


build_hand(deal_pile,human_deck)
s.show_hand(human_deck)

