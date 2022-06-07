from logic import *

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
    
    def initialize_game(self) -> bool: #TODO Enable use of player name and write instructions
        '''Initial setup of game to gather human player information and show instructions. '''
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
        '''Triggers cabo_called() to trigger final round and prints cabo back to terminal.'''
        print("CABOOOOOOO!")
        self.call_cabo_action()
        return True
    
    def call_cabo_action(self) -> bool:
        '''Sets cabo state evaluated in main game while loop'''
        self.cabo_called = True
        return True

    def discard_card(self) -> bool:
        '''Transfers card from deal stack to discard stack '''
        print_transfer(self.deal_stack,self.discard_stack,0,0,True)
        return True          
    
    def swap_draw_card(self,hand_index: int,players_stack) -> tuple[Stack,Stack]:
        '''Enables a player to swap the "drawn" card with one in their hand 
        and send the one in their hand to the discard pile.
        
        players_stack == players hand'''
        print_transfer(self.human_stack,self.discard_stack,hand_index,0)
        print_transfer(self.deal_stack,self.human_stack,0,hand_index)
        return self.human_stack[0],self.discard_stack[0] 

    def start_round(self) -> bool:
        '''Displays initial information of round to human player.'''
        print(f"\n \n \n --------------------------------------------------------\n \t \t This is the start of turn {self.turn_count}\n---------------------------------------------------------\n")
        sleep(1)
        if self.open_hand == True:
            print(Stack.show_hand_table(self.computer_stack,True))
            print(Stack.show_hand_table(self.human_stack,True))
            sleep(2)
            return True
        elif self.turn_count == 1 and self.open_hand == False:
            print(Stack.show_placeholder_hand(self.computer_stack))
            print(Stack.show_hand_table(self.human_stack))
            sleep(2)
            return True
        else:
            print(Stack.show_placeholder_hand(self.computer_stack))
            print(Stack.show_placeholder_hand(self.human_stack))
            return True

    def human_turn(self) -> bool:
        '''Gather human turn input and triggers game play mechanics. '''
        self.start_round()
        discard_card = self.discard_stack.get_top_card()
        r = int(input(f"\n The discard pile contains a {discard_card.name}. \
            \n \n Would you like to swap this with a card in your own hand? \
            \n \n  If so, press 1. Otherwise, 0 to draw a card. \n "))
        if r == 1:
            while True:
                hand_index: int = int(input("Which card would you like to replace?")) - 1
                try:
                    r = swap(self.discard_stack,self.human_stack,0,hand_index)
                    print(f"You swapped discarded card {r[1]} for a {r[0]} at position {hand_index} in your hand.")
                    sleep(2)
                except IndexError:
                    print(f"\n Sorry - that card doesn't exist. Let's try again. \n")
                    sleep(1)
                else:
                    break
            return True
        elif r == 0:
            while True:
                sleep(1)
                print(Stack.print_draw_card_preview(self.deal_stack))
                print(Card.print_card_powers_string(self.deal_stack[0]))
                actions:int = int(input("\n What actions would you like to take?  \
                                        \n \t 1. Use power on drawn card  \
                                        \n \t 2. Discard drawn card \
                                        \n \t 3. Swap drawn card with one in hand \
                                        \n \t 4. Call Cabo! \
                                        \n \t 5. End game  \
                                        \n \n \t Please respond with 1,2,3,4 \n \n"))
                try:
                    if actions == 5: #end game
                        exit()
                    elif actions == 4: #call cabo
                        self.call_cabo()
                        return True
                    elif actions == 3:
                        while True:
                            hand_index: int = int(input("Which card would you like to replace?")) - 1
                            try:
                                r = self.swap_draw_card(hand_index,self.human_stack)
                                print(f"{r[0].name} is now in position {hand_index} in your hand. {r[1].name} has been sent to the discard pile.")
                                sleep(2)
                            except IndexError:
                                print(f"\n Sorry - that card doesn't exist. Let's try again. \n")
                                sleep(1)
                            else:
                                break
                        return True
                    elif actions == 2: # discard
                        self.discard_card()
                        sleep(3)
                        return True
                    elif actions == 1: #TODO could probably refactor this to make this presentation only. 
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
        
    def computer_turn(self): #TODO make this work lol
        return


    def end_turn(self) -> bool:
        '''Ends turn, increments turn count, and prints terminal indicator.'''
        print(f"\n \n \n --------------------------------------------------------\n \t \tThat concludes turn {self.turn_count}\n---------------------------------------------------------\n")
        self.turn_count_increment()
        sleep(2)
        cls = lambda: print('\n' * 100)
        cls()
        return True
    
    def turn_count_increment(self) -> bool:
        '''increments turn count indicator'''
        self.turn_count += 1
        return True