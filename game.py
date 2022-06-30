from model import *
from view import *



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
        self.name = ''
    
    def initialize_game(self) -> None: #TODO Enable use of player name and write instructions
        '''Initial setup of game to gather human player information and show instructions. '''
        self.name = present_intro()
        
    def call_cabo_action(self) -> bool:
        '''Sets cabo state evaluated in main game while loop'''
        self.cabo_called = True
        return True

    def discard_card(self) -> bool:
        '''Transfers card from deal stack to discard stack '''
        make_transfer(self.deal_stack,self.discard_stack,0,0,True)
        return True          
    
    def swap_draw_card(self,hand_index: int,players_stack) -> tuple[Stack,Stack]:
        '''Enables a player to swap the "drawn" card with one in their hand 
        and send the one in their hand to the discard pile.
        
        players_stack == players hand'''
        make_transfer(self.human_stack,self.discard_stack,hand_index,0)
        make_transfer(self.deal_stack,self.human_stack,0,hand_index)
        return self.human_stack[0],self.discard_stack[0] 

    def start_round(self) -> bool:
        '''Displays initial information of round to human player.'''
        present_round_spacer(self.turn_count)
        sleep(1)
        if self.open_hand == True:
            Stack.print_hand_table(self.computer_stack,True)
            Stack.print_hand_table(self.human_stack,True)
            sleep(2)
            return True
        elif self.turn_count == 1 and self.open_hand == False:
            Stack.show_placeholder_hand(self.computer_stack)
            Stack.print_hand_table(self.human_stack)
            sleep(2)
            return True
        else:
            Stack.show_placeholder_hand(self.computer_stack)
            Stack.show_placeholder_hand(self.human_stack)
            return True

    def human_turn(self):
        '''Gather human turn input and triggers game play mechanics. '''
        self.start_round()
        discard_card = self.discard_stack.top_card()
        r = present_swap_discard_prompt(discard_card)
        if r == 1:
            while True:
                try:
                    hand_index: int = present_swap_card_prompt() - 1
                    sr = swap(self.discard_stack,self.human_stack,0,hand_index)
                    present_swap_results(sr,hand_index)
                except (IndexError,ValueError):
                    present_card_index_error()
                else:
                    break
            return True
        elif r == 0:
            while True:
                sleep(1)
                Stack.present_draw_card_preview(self.deal_stack)
                Card.present_card_powers_string(self.deal_stack[0])
                actions = present_action_prompt()
                try:
                    if actions == 5: #end game
                        exit()
                    elif actions == 4: #call cabo
                        if self.call_cabo_action() == True:
                            present_cabo()
                        return True
                    elif actions == 3:
                        while True:
                            hand_index: int = present_swap_card_prompt() - 1
                            try:
                                r = self.swap_draw_card(hand_index,self.human_stack)
                                present_swap_draw_results(r,hand_index)
                            except IndexError:
                                present_card_index_error()
                            else:
                                break
                        return True
                    elif actions == 2: # discard
                        self.discard_card()
                        sleep(3)
                        return True
                    elif actions == 1: 
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
                        present_card_index_error()
                    if actions == 1:
                        present_card_power_error()
                    else:
                        present_card_index_error()
                else:
                    break
            return True

        
    def computer_turn(self): #TODO make this work lol
        return


    def end_turn(self) -> bool:
        '''Ends turn, increments turn count, and prints terminal indicator.'''
        present_end_round(self.turn_count)
        self.turn_count_increment()
        return True

    def turn_count_increment(self) -> bool:
        '''increments turn count indicator'''
        self.turn_count += 1
        return True
