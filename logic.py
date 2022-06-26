from __future__ import annotations
from collections import deque
import random
from typing import Any, List, Optional
import constants as c
from tabulate import tabulate
from time import sleep

class Stack(deque): #TODO need to refactor this to not inherit from deque?
    '''Creates a hand and maintains functions related to a stack.
    Takes in a name string and a list of cards.'''
    def __init__(self, name: str,members: List[Card]):
        self.members = members
        self.name = name

    def retrieve_sum_value(self) -> int:
        '''Returns sum of the value of all cards in current stack.'''
        #sum: int = 0
        #for c in self:
        #sum += c.value
        return sum(c.value for c in self)
    
    def format_draw_card_preview(self,index:int = 0) -> str: #TODO refactor this to a presentation class
        '''Prints to the terminal the name of the Stacks current card in index.'''
        drawn_card = self[index]
        return f"\n You've drawn a {drawn_card.name}."
    
    def top_card(self) -> Card:
        '''Returns the top card of the stack AKA card in index 0'''
        return self[0]

    def show_placeholder_hand(self) -> str:
        '''Returns a string containing the name of the hand and a 
        table of the masked set of cards in a hand -- using the tabulate table module as defined in tabulate(). '''
        hand:List[List[str]] = [["Position","Card"]]
        cards:Card
        index = 1
        for cards in self:
                hand.append([f"Position: {index}",'x'])
                index += 1
        table = tabulate(hand,tablefmt="fancy_grid",headers='firstrow')
        response = f"\n\n\n{self.name}: \n\n {table}"
        return response

    def show_hand_table(self,open_hand: bool = False) -> str:
        '''Returns a string containing a table of the masked set of cards in a hand -- using the tabulate table module as defined in tabulate().
            If open hand == False, it reveals the first two cards to the player. If open_hand == True, it shows all cards.
            '''
        hand:list[list[str]] = [["Position","Card"]]
        cards:Card
        index = 1
        if not open_hand:
            for cards in self:
                    if index < 3:
                        hand.append([f"Position: {index}",cards.name])
                        index += 1
                    else:
                        hand.append([f"Position: {index}",'x'])
                        index += 1
        else:
            for cards in self:
                    hand.append([f"Position: {index}",cards.name])
                    index += 1
        response = self.tabulate_hand(hand,self)
        return response
    
    def tabulate_hand(self,hand:list[list[str]],stack_name:Stack) -> str:
        '''Uses tabulate module to produce terminal formatted tables.'''
        table = tabulate(hand,tablefmt="fancy_grid",headers='firstrow')
        response = f"\n\n\n{self.name}: \n\n {table}"
        return response

        

class Card():  #TODO add logic to show human hand vs. computer hand
    '''This creates a cabo card.'''
    def __init__(self,name: str,val: int = 0,power: int =0):
        self.name = name
        self.value = val
        self.power = power     

    def get_card_data(self) -> str:
        '''Returns name attribute of Card'''
        return self.name
    

    def update_value(self) -> bool: 
        '''This function is used when building deck 
        to update card values from constant.'''
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
        return False

    def return_card_powers(self) -> str:
        '''Returns value associated with the power defined in Constants of the Card'''
        for key,value in c.POWERS.items():
            if self.power == value:
                power_value = key
                return power_value
        
    def print_card_powers_string(self) -> str:
        '''Prints a string to terminal of the power associated with the Card'''
        power_string = self.return_card_powers()
        power_string = f"This top card has the ability to:{power_string}" # TODO fix this to show strings
        return power_string



def build_deck() -> list[Card]:
    '''Initial construction of the deck by creating cards defined in CARD_COUNTS_* and then iterating over them 
        to update the value and power as defined in constants'''
    new_deck:list[Card] = []
    new_deck.extend([Card(name) for name in c.CARD_COUNTS_4 for i in range(1,5)])
    new_deck.extend([Card(name) for name in c.CARD_COUNTS_2 for i in range(1,3)])
    for card in new_deck:
        Card.update_value(card)
    for card in new_deck:
        Card.update_powers(card)
    return new_deck

def build_hand(source_stack:Stack,dest_stack:Stack) -> bool:
    '''Creates initial hands for players with four cards'''        
    n:int = 0 
    while n < 4:
        print_transfer(source_stack,dest_stack,0,n)
        n += 1
    return True
        
def transfer_action(source_stack: Stack,dest_stack: Stack, source_index:int = 0, dest_index:int = 0,describe:bool = False) -> tuple[str,str]:
    ''' ***use Transfer()***
    Copies a card in one stack to destination stack with:
        - source stack as source_stack
        - destination stack as dest_stack
        - source_index  = source index to copy and delete card from. 
        Default is "top" of deck or index 0
        - dest_index  = destination index to insert'''
    transfer_card:Card = source_stack[source_index]
    del(source_stack[source_index])
    dest_stack.insert(dest_index,transfer_card)    
    return transfer_card.name,dest_stack.name

def print_transfer(source_stack: Stack,dest_stack: Stack, source_index:int = 0, dest_index:int = 0,describe:bool = False) -> bool:
    '''Copies a card in one stack to destination stack with:
          - source stack as source_stack
          - destination stack as dest_stack
          - source_index  = source index to copy and delete card from. 
            Default is "top" of deck or index 0
          - dest_index  = destination index to insert
          
          Set 'describe' to True to print a record of the transfer to the terminal.'''    
    transfer_results = transfer_action(source_stack,dest_stack,source_index,dest_index)
    if describe == True:
        print(f"{transfer_results[0]} was transferred to {transfer_results[1]}.")
    return True

def swap(source_stack: Stack,dest_stack: Stack, source_index:int, dest_index:int) -> tuple[str,str]:
    '''Switches Card from source_stack in source_index with Card in dest_stack to dest_index '''
    swap_card1:Card = source_stack[source_index]
    swap_card2:Card = dest_stack[dest_index]
    del(source_stack[source_index])
    del(dest_stack[dest_index])
    dest_stack.insert(dest_index,swap_card1)    
    source_stack.insert(source_index,swap_card2)   
    return swap_card1.name,swap_card2.name

def shuffle(stack_name: Stack) -> bool:
    '''Shuffles cards of a Stack using random function.'''
    rng = random.Random()
    rng.shuffle(stack_name)
    return True


def get_drawn_card(stack_name: Stack) -> Card:
    '''Returns the draw card from the deal stack. Use this on the deal_stack due to bug where deal_stack can't be a Stack.'''
    return stack_name[0]


def power_controller(drawn_card_power: int, human_stack: Stack,computer_stack: Stack,dest_position:int | None = None, source_position:int | None = None) -> tuple[Any,Any]: #TODO fix typing here
    '''Defines and triggers card power actions. '''
    if source_position != None: 
        source_index = (source_position) - 1
    if dest_position != None:
        dest_index = int(dest_position) -1 
    if drawn_card_power == 1:
        card_name = Card.get_card_data(human_stack[dest_index])
        return card_name,dest_position
    elif drawn_card_power == 2:
        card_name = Card.get_card_data(computer_stack[source_index])
        return card_name,source_position
    elif drawn_card_power == 3:
        swap(human_stack,computer_stack,source_index,dest_index)
    elif drawn_card_power == 4:
        swap_results = swap(human_stack,computer_stack,source_index,dest_index)
        return swap_results


def use_power(drawn_card_power: int,human_stack: Stack,computer_stack: Stack) -> bool:
    '''Collects necessary input from human to trigger correct card powers '''
    if drawn_card_power == 1: #TODO rewrite to show revealed card with table rather than sentence
        peek_index = int(input("Which of your own cards would you like to look at? Respond with position number: \n"))
        r = power_controller(drawn_card_power,human_stack,computer_stack,peek_index)
        card_name:str = r[0]
        index_n:int = r[1] 
        print(f"{card_name} is in position {index_n} in your hand.")
        sleep(4)
        return True
      
    elif drawn_card_power == 2:
        peek_index = int(input("Which of your opponents cards would you like to look at? Respond with position number: \n"))
        r = power_controller(drawn_card_power,human_stack,computer_stack,None,peek_index)
        card_name = r[0]
        index_n = r[1] 
        print(f"{card_name} is in position {index_n} in your opponents hand.")
        sleep(4)
        return True
      
    elif drawn_card_power == 3:
        source_index = int(input("Which of your cards would you like to swap? Please enter position number."))
        dest_index = int(input("Which of your opponents cards would you like to swap with? Please enter position number."))
        r = power_controller(drawn_card_power,human_stack,computer_stack,dest_index,source_index)
        print(f"Your card at position {source_index} was swapped with your opponents card at position {dest_index}.")
        sleep(4)
        return True
      
    elif drawn_card_power == 4:
        source_index = int(input("Which of your cards would you like to swap? Please enter position number."))
        dest_index = int(input("Which of your opponents cards would you like to swap with? Please enter position number."))
        r = power_controller(drawn_card_power,human_stack,computer_stack,dest_index,source_index)
        c1 = r[0]
        c2 = r[1]
        print(f"{c1} at position {source_index} was swapped with {c2} at position {dest_index} ")
        sleep(4)
        return True
    else:
        return False
 
