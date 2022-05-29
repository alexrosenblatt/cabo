from ast import Pass
import random
import constants as c
from cardclass import Card

def build_deck():
    new_deck = []
    new_deck.extend([Card(name) for name in c.CARD_COUNTS_4 for i in range(1,5)])
    new_deck.extend([Card(name) for name in c.CARD_COUNTS_2 for i in range(1,3)])
    for card in new_deck:
        Card.update_value(card)
    for card in new_deck:
        Card.update_abbrv(card)  
    for card in new_deck:
        Card.update_powers(card) 
    return new_deck

def build_hand(deal_pile,human_deck):
        n: int
        n = 1 
        while n < 5:
            Stack.transfer(deal_pile,human_deck,0,n)
            n += 1

class Stack():
    '''Creates a hand and maintains functions related to a stack. '''
    def __init__(self,members = []):
        self.members = members
    
    def shuffle(self):
        rng = random.Random()
        rng.shuffle(self)

    def remove(self,index):
        self.members.pop(index)
        return True
    
    def add(self,index,card):
        self.members.insert(index,card)
        return True

    def deal(self):
        return self.members.pop()
    
    def is_empty(self):
        return self.members == []
    
    def show_hand(self):
        hand = []
        for cards in self:
            hand.append(cards.name)
        return print(f"Your hand contains: {hand}")
        
    def transfer(self_name,to_name, self_index,other_index):
        transfer_card = self_name[self_index]
        del(self_name[self_index])
        to_name.insert(other_index,transfer_card)    


            







            
''' 
 #commenting out to test inheriting behaviors from the "list"  
    def __delitem__(self, indice):
        del self.members[indice]

# stolen from pycarddealer

    def __getitem__(self, key):
        self_len = len(self)
        if isinstance(key, slice):
            return [self[i] for i in xrange(*key.indices(self_len))]
        elif isinstance(key, int):
            if key < 0 :
                key += self_len
            if key >= self_len:
                raise IndexError("The index ({}) is out of range.".format(key))
            return self.members[key]
        else:
            raise TypeError("Invalid argument type.")
    
    def __len__(self):
        """
        Allows check the Stack length, with len.
        :returns:
            The length of the stack (self.members).
        """
        return len(self.members)
'''  