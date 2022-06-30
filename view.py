def present_cabo() -> bool:
    '''Triggers cabo_called() to trigger final round and prints cabo back to terminal. Sets cabo called game class to True.'''
    print("CABOOOOOOO!")
    return True

def present_round_spacer(turn_count) -> None:
    print(f"\n \n \n --------------------------------------------------------\n \t \t This is the start of turn {turn_count}\n---------------------------------------------------------\n")

def present_swap_discard_prompt(discard_card) -> int:
    while True:
        try:    
            r = int(input(f"\n The discard pile contains a {discard_card.name}. \
                        \n \n Would you like to swap this with a card in your own hand? \
                        \n \n  If so, press 1. Otherwise, 0 to draw a card. \n "))
            return r
        except ValueError:
                print(f"\n Please enter a valid number. Let's try again. \n")
                sleep(1)
        else:
            break 

def present_swap_card_prompt() -> int:
    n = int(input("Which card would you like to replace?"))
    return n 

def present_swap_results(sr,hand_index) -> None:
        print(f"You swapped discarded card {sr[1]} for a {sr[0]} at position {hand_index} in your hand.")
        sleep(2)


def present_card_index_error() -> None:
        print(f"\n Sorry - that card or position doesn't exist. Let's try again. \n")
        sleep(1)

def present_action_prompt() -> int:
        a = int(input("\n What actions would you like to take?  \
                                            \n \t 1. Use power on drawn card  \
                                            \n \t 2. Discard drawn card \
                                            \n \t 3. Swap drawn card with one in hand \
                                            \n \t 4. Call Cabo! \
                                            \n \t 5. End game  \
                                            \n \n \t Please respond with 1,2,3,4 \n \n"))
        return a

def present_swap_draw_results(r,hand_index):
    print(f"{r[0].name} is now in position {hand_index} in your hand. {r[1].name} has been sent to the discard pile.")
    sleep(2)

def present_card_power_error() -> None:
        print(f"\n Sorry - your card does not have a power. Let's try again. \n")
        sleep(1)

def present_end_round(turn_count) -> None:
    print(f"\n \n \n --------------------------------------------------------\n \t \tThat concludes turn {turn_count}\n---------------------------------------------------------\n")
    cls = lambda: print('\n' * 100)
    cls()
    sleep(2)

def present_intro():
    print("Welcome to Cabo!")
    name:str = input(f"Please tell me your name! \n")
    played_before:str = input(f"Have you played before? Enter Yes or No \n")
    played_before = played_before.lower()
    if played_before == 'yes':
        return True
    if played_before == 'no':
        print(f"/n Placeholder for Instructions \n")
        return False
    return name