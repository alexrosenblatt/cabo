from ast import Pass
import random
from collections import deque as d


class Stack:
    '''Creates a hand and maintains functions related to a stack. '''
    def __init__(self,cards = []):
        self.cards = d(cards)
        #self.length = len(self.cards)
        #self.top_card = self.cards[0]
    
    def __delitem__(self, indice):
        del self.cards[indice]
# stolen from card
    def __getitem__(self, key):
        self_len = len(self)
        if isinstance(key, slice):
            return [self[i] for i in xrange(*key.indices(self_len))]
        elif isinstance(key, int):
            if key < 0 :
                key += self_len
            if key >= self_len:
                raise IndexError("The index ({}) is out of range.".format(key))
            return self.cards[key]
        else:
            raise TypeError("Invalid argument type.")
    
    def __len__(self):
        """
        Allows check the Stack length, with len.
        :returns:
            The length of the stack (self.cards).
        """
        return len(self.cards)
    
    #def show_hand(self):
        #return self.cards

    def shuffle(self):
        rng = random.Random()
        rng.shuffle(self.cards)

    def remove(self,index):
        self.cards.pop(index)
        return True
    
    def add(self,index,card):
        self.cards.insert(index,card)
        return True

    def deal(self):
        return self.cards.pop()
    
    def is_empty(self):
        return self.cards == []
            



