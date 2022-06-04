from __future__ import annotations
from collections import deque
from operator import truediv
import random
from typing import List
import constants as c
from tabulate import tabulate
from time import sleep


def build_deck() -> list[Card]:
    new_deck:list[Card] = []
    new_deck.extend([Card(name) for name in c.CARD_COUNTS_4 for i in range(1,5)])
    new_deck.extend([Card(name) for name in c.CARD_COUNTS_2 for i in range(1,3)])
    for card in new_deck:
        Card.update_value(card)
    for card in new_deck:
        Card.update_powers(card) 
    return new_deck

def build_hand(source_stack:Stack,dest_stack:Stack) -> bool:
        n: int
        n = 0 
        while n < 4:
            transfer(source_stack,dest_stack,0,n)
            n += 1
        return True

def transfer_action(source_stack: Stack,dest_stack: Stack, source_index:int = 0, dest_index:int = 0,describe:bool = False) -> tuple[str,str]:
        transfer_card:Card = source_stack[source_index]
        del(source_stack[source_index])
        dest_stack.insert(dest_index,transfer_card)    
        return transfer_card.name,dest_stack.name

def transfer(source_stack: Stack,dest_stack: Stack, source_index:int = 0, dest_index:int = 0,describe:bool = False) -> bool:
    '''Copies a card in one stack to destination stack with:
          - source stack as source_stack
          - destination stack as dest_stack
          - source_index  = source index to copy and delete card from. Default is "top" of deck or index 0
          - dest_index  = destination index to insert'''
    transfer_results = transfer_action(source_stack,dest_stack,source_index,dest_index)
    if describe == True:
        print(f"{transfer_results[0]} was transferred to {transfer_results[1]}. ")
    return True

def swap(source_stack: Stack,dest_stack: Stack, source_index:int = 0, dest_index:int = 0,describe:bool = False) -> tuple[str,str]:
        swap_card1:Card = source_stack[source_index]
        swap_card2:Card = dest_stack[dest_index]
        del(source_stack[source_index])
        del(dest_stack[dest_index])
        dest_stack.insert(dest_index,swap_card1)    
        source_stack.insert(source_index,swap_card2)    
        return swap_card1.name,swap_card2.name



def shuffle(stack_name: Stack) -> bool:
    rng = random.Random()
    rng.shuffle(stack_name)
    return True


def show_hand_table(stack_name:Stack,open_hand: bool = False) -> str:
        hand:list[list[str]] = [["Position","Card"]]
        cards:Card
        response:str = ''
        index = 1
        if open_hand == False:
            for cards in stack_name:
                    if index < 3:
                        hand.append([f"Position: {index}",cards.name])
                        index += 1
                    else:
                        hand.append([f"Position: {index}",'x'])
                        index += 1

        else:
            for cards in stack_name:
                    hand.append([f"Position: {index}",cards.name])
                    index += 1
        response = tabulate_hand(hand,stack_name)
        return response

def tabulate_hand(hand:list[list[str]],stack_name:Stack) -> str:
        table = tabulate(hand,tablefmt="fancy_grid",headers='firstrow')
        response = f"\n\n\n{stack_name.name}: \n\n {table}"
        return response


def show_placeholder_hand(stack_name: Stack) -> str:
        hand:List[List[str]] = [["Position","Card"]]
        cards:Card
        response:str = ''
        index = 1
        for cards in stack_name:
                hand.append([f"Position: {index}",'x'])
                index += 1
        table = tabulate(hand,tablefmt="fancy_grid",headers='firstrow')
        response = f"\n\n\n{stack_name.name}: \n\n {table}"
        return response

def get_top_card(stack_name: Stack) -> str:
        return stack_name[0].name

def get_drawn_card(stack_name: Stack) -> Card:
        return stack_name[0]

# how can i rewrite this to have the default stack? #TODO seperate the presentation logic
def show_top_discard(stack_name: Stack) -> str:
        top_card = get_top_card(stack_name)
        return f"\n The top card in the discard pile is: {top_card}."

def action_presenter(drawn_card_power: int, card_name1: str = '',card_name2: str = '', peek_position: int = 0, source_index: int = 0, dest_index: int = 0) -> str:
    if drawn_card_power == 1:
        print(f"{card_name1} is in position {peek_position} in your hand.")
    elif drawn_card_power == 2:
        print(f"{card_name1} is in position {peek_position} in your opponents hand.")
    elif drawn_card_power == 3:
        print(f"Your card at position {source_index} was swapped with your opponents card at position {dest_index}.")
    elif drawn_card_power == 4:
        print(f"{card_name1} at position {source_index} was swapped with {card_name2} at position {dest_index} ")
    elif drawn_card_power == 5:
        pass




def use_power(drawn_card_power: int,human_stack: Stack,computer_stack: Stack) -> bool:
    if drawn_card_power == 1: #TODO rewrite to show revealed card with table rather than sentence
        peek_index = input("Which of your own cards would you like to look at? Respond with position number: \n")
        peek_position = int(peek_index)-1
        card_name = Card.get_card_data(human_stack[peek_position])
        action_presenter(drawn_card_power, card_name, peek_index)
        return True
    elif drawn_card_power == 2:
        peek_index = input("Which of your opponents cards would you like to look at? Respond with position number: \n")
        peek_position = int(peek_index)-1
        card_name = Card.get_card_data(computer_stack[peek_position])
        action_presenter(drawn_card_power,card_name,peek_index)
        return True
    elif drawn_card_power == 3:
        source_index = int(input("Which of your cards would you like to swap? Please enter position number."))
        dest_index = int(input("Which of your opponents cards would you like to swap with? Please enter position number."))
        source_position = source_index-1
        dest_position = source_position-1
        transfer(human_stack,computer_stack,source_position,dest_position)
        action_presenter(drawn_card_power,'',0,source_index,dest_index) # TODO lol bad fix this
        return True
    elif drawn_card_power == 4:
        source_index = int(input("Which of your cards would you like to swap? Please enter position number."))
        dest_index = int(input("Which of your opponents cards would you like to swap with? Please enter position number."))
        source_position = source_index-1
        dest_position = dest_index-1
        swap_results = swap(human_stack,computer_stack,source_position,dest_position,True)
        action_presenter(drawn_card_power,swap_results[0],swap_results[1],0,source_index,dest_index)
        return True
    else:
        return False
        


class Stack(deque): #TODO need to refactor this to not use deque?
    '''Creates a hand and maintains functions related to a stack. '''
    def __init__(self, name: str,members: List[Card]):
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
    
    def print_draw_card_preview(self,index:int = 0) -> str:
        drawn_card = self[index]
        return f"\n You've drawn a {drawn_card.name}."
        
    
    def draw_card(self,index:int = 0) -> Card:
        drawn_card = self.pop(index)
        return drawn_card

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

    def get_card_data(self) -> str:
        return self.name
    

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
        return False

    def return_card_powers(self) -> str:
        for key,value in c.POWERS.items():
            if self.power == value:
                power_value = key
        return power_value

            
    
    def print_card_powers_string(self) -> str:
        power_string = self.return_card_powers()
        power_string = f"This top card has the ability to:{power_string}" # TODO fix this to show strings
        return power_string


        



# TODO need to add error handling and fix the return function here and/or get rid of
#   def get_power_string(self) -> str:
#        '''This function returns the string related to the objects power.'''
#        for key,value in c.POWERS.items():
#            if self.power == value:
#                return key

    
    def show_card(self):
        return self.name
 
 
class Game():
    def __init__(self,human_stack, computer_stack, discard_stack,deal_stack,turn_count:int = 1,open_hand:bool = False,cabo_called:bool = False):
        self.turn_count = turn_count
        self.open_hand = open_hand # set this to see every card in each hand each round
        self.human_stack = human_stack
        self.computer_stack = computer_stack
        self.discard_stack = discard_stack
        self.cabo_called = cabo_called
        self.turn_count = turn_count
        self.deal_stack = deal_stack
    
    def initialize_game(self) -> bool:
        print("Welcome to Cabo!")
        name:str = input(f"Please tell me your name! \n")
        played_before:str = input(f"Have you played before? Enter Yes or No \n")
        played_before = played_before.lower()
        if played_before == 'yes':
            return True
        if played_before == 'no':
            print(f"/n Placeholder for Instructions \n")
            return False
        return True

    def call_cabo(self) -> bool:
        print("CABOOOOOOO!")
        self.call_cabo_action()
        return True
    
    def call_cabo_action(self) -> bool:
        self.cabo_called = True
        return True

    def cabo_state(self) -> bool:
        if self.cabo_called == True:
            return True    
        else:
            return False

    def start_round(self) -> bool:
        print(f"\n \n \n --------------------------------------------------------\n \t \t This is the start of turn {self.turn_count}\n---------------------------------------------------------\n")
        if self.open_hand == True:
            print(show_hand_table(self.computer_stack,True))
            print(show_hand_table(self.human_stack,True))
            print(show_top_discard(self.discard_stack))
            print(Stack.print_draw_card_preview(self.deal_stack))
            print(Card.print_card_powers_string(self.deal_stack[0]))
            return True
        elif self.turn_count == 0 and self.open_hand == False:
            print(show_placeholder_hand(self.computer_stack))
            print(show_hand_table(self.human_stack))
            print(show_top_discard(self.discard_stack))
            print(Stack.print_draw_card_preview(self.deal_stack))
            return True
        else:
            print(show_placeholder_hand(self.computer_stack))
            print(show_placeholder_hand(self.human_stack))
            print(show_top_discard(self.discard_stack))
            print(Stack.print_draw_card_preview(self.deal_stack))
            return True


    def human_turn(self) -> bool:
        while True:
            actions:int = int(input(f"\n What actions would you like to take? \n \t 1. Use power on drawn card \n \t 2. Swap draw card with card in your own hand \n \t 3. Discard drawn card \n \t 4. Call Cabo! \n \t 5. End game \n Please respond with 1,2,3,4, or 5. \n" ))
            try:
                if actions == 5: #end game
                    exit()
                elif actions == 4: #call cabo
                    self.call_cabo()
                    return True
                elif actions == 3: # discard
                    transfer(self.deal_stack,self.discard_stack,0,0,True) #TODO update method description to describe discard scenario
                    #figure out how to end turn here
                    return True
                elif actions == 2: # swap draw card
                    while True:
                        hand_index: int = int(input("Which card would you like to replace?")) - 1
                        try:
                            transfer(self.human_stack,self.discard_stack,hand_index,0)
                            transfer(self.deal_stack,self.human_stack,0,hand_index)
                        except IndexError:
                            print(f"\n Sorry - that card doesn't exist. Let's try again. \n")
                        else:
                            break
                    return True
                elif actions == 1: #use power
                    top_card = get_drawn_card(self.deal_stack)
                    drawn_card_power = top_card.power
                    if drawn_card_power == 0:
                        raise ValueError
                    else:
                        use_power(drawn_card_power,self.human_stack,self.computer_stack) #TODO make this agnostic to number/type of players
                        return True
                elif actions > 6:
                    raise ValueError #to make sure number is in range
            except ValueError:
                if actions == 2:
                    print(f"\n Sorry - that is not a valid card position. Let's try again. \n")
                if actions == 1:
                    print(f"\n Sorry - your card does not have a power. Let's try again. \n")
                else:
                    print(f"\n Sorry - that is not a valid operation. Let's try again. \n")
            else:
                break
        return True
   
    def computer_turn(self):
        return


    def end_round(self) -> bool:
        print(f"\n \n \n --------------------------------------------------------\n \t \tThat concludes turn {self.turn_count}\n---------------------------------------------------------\n")
        self.turn_count_increment()
        sleep(2)
        return True
    
    def turn_count_increment(self) -> bool:
        self.turn_count += 1
        return True
    
