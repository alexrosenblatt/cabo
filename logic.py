from __future__ import annotations
from ast import Break, Str
import random
from typing import List
from traitlets import Bool
import constants as c


def build_deck() -> list[Card]:
    new_deck:list[Card] = []
    new_deck.extend([Card(name) for name in c.CARD_COUNTS_4 for i in range(1,5)])
    new_deck.extend([Card(name) for name in c.CARD_COUNTS_2 for i in range(1,3)])
    for card in new_deck:
        Card.update_value(card)
    for card in new_deck:
        Card.update_powers(card) 
    return new_deck

def build_hand(deal_pile:list[Card],human_deck:list[Card]) -> bool:
        n: int
        n = 1 
        while n < 5:
            transfer(deal_pile,human_deck,0,n)
            n += 1
        return True

def transfer(self_name: list[Card],to_name: list[Card],self_index:int,other_index:int) -> bool:
        transfer_card = self_name[self_index]
        del(self_name[self_index])
        to_name.insert(other_index,transfer_card)    
        return True

def shuffle(stack_name:list[Card]) -> bool:
    rng = random.Random()
    rng.shuffle(stack_name)
    return True

def show_hand(stack_name:list[Card]) -> str:
        hand:List[str] = []
        cards:Card
        response:str = ''
        for cards in stack_name:
            hand.append(cards.name)
        response = f"Your hand contains: {hand}"
        return response


class Stack():
    '''Creates a hand and maintains functions related to a stack. '''
    def __init__(self,members: list[Card] = []):
        self.members = members

    def remove(self,index: int ):
        self.members.pop(index)
        return True
    
    def add(self,index:int ,card:Card):
        self.members.insert(index,card)
        return True

    def deal(self):
        return self.members.pop()
    
    def is_empty(self):
        return self.members == []

#add logic to show human hand vs. computer hand
    
        

class Card():
    '''This creates a cabo card.'''
    def __init__(self,name: str,val: int = 0,power: int =0):
        self.name = name
        self.value = val
        self.power = power     

    def get_data(self) -> bool:
        '''This returns the details of a specific card.'''
        print(f'{self.name},{self.value},{self.power}')
        return True

    def update_value(self) -> bool:
        '''This function is used when building deck to update card values from constant.'''
        for key,value in c.CARD_VALUES.items():
            if self.name == key:
                self.value = value
        return True
    
    def update_powers(self) -> bool:
        '''This function is used when building deck to update power values from constant.'''
        for key,value in c.CARD_POWERS.items():
            if self.name == key:
                self.power = value
                return True
            else:
                return False
        return False

# need to add error handling and fix the return function here
    def get_power_string(self) -> str:
        '''This function returns the string related to the objects power.'''
        for key,value in c.POWERS.items():
            if self.power == value:
                return key
        return ''

    
    def show_card(self):
        return self.name
            







            
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