from __future__ import annotations
from ast import Break, Str
from collections import deque
import random
from tkinter import Variable
from typing import List
from traitlets import Bool
import constants as c
from tabulate import *


def build_deck() -> list[Card]:
    new_deck:list[Card] = []
    new_deck.extend([Card(name) for name in c.CARD_COUNTS_4 for i in range(1,5)])
    new_deck.extend([Card(name) for name in c.CARD_COUNTS_2 for i in range(1,3)])
    for card in new_deck:
        Card.update_value(card)
    for card in new_deck:
        Card.update_powers(card) 
    return new_deck

def build_hand(source_stack:list[Card],dest_stack:list[Card]) -> bool:
        n: int
        n = 0 
        while n < 4:
            transfer(source_stack,dest_stack,0,n)
            n += 1
        return True

def transfer(source_stack: list[Card],dest_stack: list[Card], source_index:int = 0, dest_index:int = 0) -> bool:
        '''Copies a card in one stack to destination stack with:
          - source stack as source_stack
          - destination stack as dest_stack
          - source_index  = source index to copy and delete card from. Default is "top" of deck or index 0
          - dest_index  = destination index to insert'''
        transfer_card = source_stack[source_index]
        del(source_stack[source_index])
        dest_stack.insert(dest_index,transfer_card)    
        return True

def shuffle(stack_name:list[Card]) -> bool:
    rng = random.Random()
    rng.shuffle(stack_name)
    return True

def show_hand(stack_name:list[Card],open_hand:bool = False) -> str:
        hand:List[str] = []
        cards:Card
        response:str = ''
        for cards in stack_name:
            hand.append(cards.name)
        if open_hand == True:
            response = f"The {stack_name.name} contains: {hand}"
        else:
            response = f"The {stack_name.name} contains: Card 1. {hand[0]} 2. {hand[1]}"
        return response

def show_hand_table(stack_name:list[Card]) -> str:
        hand:List[str] = [["Position","Card"]]
        cards:Card
        response:str = ''
        index = 1
        for cards in stack_name:
                hand.append([f"Position: {index}",cards.name])
                index += 1
        table = tabulate(hand,tablefmt="fancy_grid",headers='firstrow')
        response = f"\n\n\n{stack_name.name}: \n\n {table}"
        return response

def get_top_card(stack_name:list[Card]) -> str:
        return stack_name[0].name

# how can i rewrite this to have the default stack?
def show_top_discard(stack_name):
        top_card = get_top_card(stack_name)
        return f"The top card in the discard pile is: {top_card}."

# need to refactor this to not use deque?
class Stack(deque):
    '''Creates a hand and maintains functions related to a stack. '''
    def __init__(self, name: str = '',members: list[Card] = []):
        self.members = members
        self.name = name

    def remove(self,index: int ):
        self.members.pop(index)
        return True
    
    def add(self,index:int ,card:Card):
        self.members.insert(index,card)
        return True

    def retrieve_score(self) -> int:
        sum: int = 0
        for c in self:
            sum += c.value
        return sum

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
 
 
class Game():
    def __init__(self,human_stack, computer_stack, discard_stack,turn_count:int = 0,open_hand:bool = False,cabo_called:bool = False):
        self.turn_count = turn_count
        # set this to see every card in each hand each round
        self.open_hand = open_hand
        self.human_stack = human_stack
        self.computer_stack = computer_stack
        self.discard_stack = discard_stack
        self.cabo_called = cabo_called
        self.turn_count = turn_count

    def start_turn(self) -> bool:
        if self.open_hand == True:
            print(show_hand_table(self.computer_stack))
            print(show_hand_table(self.human_stack))
            print(show_top_discard(self.discard_stack))
            return True
        elif self.turn_count == 0:
            print(show_hand_table(self.human_stack,False))
            return True
        else:
            print(show_top_discard(self.discard_stack))
            return True
    def end_turn(self) -> bool:
        self.turn_count += 1
        print(f"\n \n \n --------------------------------------------------------\n \t \tThat concludes turn {self.turn_count}\n--------------------------------------------------------\n")
        return True

    def call_cabo(self) -> bool:
        self.cabo_called = True
        return True

    def cabo_state(self) -> bool:
        if self.cabo_called == True:
            return True    
        else:
            return False

class Turn():
    def __init__(self,) -> None:
        pass
