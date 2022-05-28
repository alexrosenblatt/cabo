from ast import Pass
import random


class Stack:
    '''Creates a hand and maintains functions related to a stack. '''
    def __init__(self,cards = []):
        self.cards = cards
        #self.length = len(self.cards)
        #self.top_card = self.cards[0]
  
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
            



