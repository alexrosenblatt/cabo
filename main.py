from cardclass import Card
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

deck = build_deck()


for card in deck:
    print(id(card))
    print(vars(card))
