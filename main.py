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

# setup initial stacks with main deck as deal pile, human_deck, computer_deck.
deal_pile = build_deck()
deal_pile = Stack(deal_pile)
deal_pile.shuffle()
human_deck = []
computer_deck = []
Stack(human_deck)
Stack(computer_deck)

transfer(deal_pile,human_deck,0,0)
transfer(deal_pile,human_deck,0,0)
transfer(deal_pile,human_deck,0,0)
transfer(deal_pile,human_deck,0,0)

def show_hand(deck_name):
    hand = []
    for cards in deck_name:
        hand.append(cards.show_card())
    print(f"Your hand contains: {hand}")
    hand = []

show_hand(human_deck)