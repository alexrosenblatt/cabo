from cardclass import Card
from stack import Stack
import random
import constants as c

def build_deck():
        new_deck = []
        new_deck += [Card(name) for name in c.CARD_COUNTS_4 for i in range(1,5)]
        new_deck += [Card(name) for name in c.CARD_COUNTS_2 for i in range(1,3)]
        for card in new_deck:
            Card.update_value(card)
        for card in new_deck:
            Card.update_abbrv(card)  
        for card in new_deck:
            Card.update_powers(card) 
        return new_deck

def transfer(self_name,to_name, self_index,other_index):
        transfer_card = self_name.cards[self_index]
        del self_name[other_index]
        to_name.insert(self_index,transfer_card)


deck = build_deck()
deal_pile = Stack(deck)
deal_pile.shuffle()
test_deck = []
Stack(test_deck)

transfer(deal_pile,test_deck,2,0)
transfer(deal_pile,test_deck,2,1)
transfer(deal_pile,test_deck,2,2)
transfer(deal_pile,test_deck,2,3)

for cards in test_deck:
    print(cards.show_card())