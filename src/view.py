from time import sleep
from tabulate import tabulate
from model import *


def present_cabo() -> bool:
    '''Triggers cabo_called() to trigger final round and prints cabo back to terminal. Sets cabo called game class to True.'''
    print("CABOOOOOOO!")
    return True


def present_round_spacer(turn_count) -> None:
    print(
        f"\n \n \n --------------------------------------------------------\n \t \t This is the start of turn {turn_count}\n---------------------------------------------------------\n"
    )


def present_swap_discard_prompt(discard_card) -> int:
    while True:
        try:
            r = int(
                input(f"\n The discard pile contains a {discard_card.name}. \
                        \n \n Would you like to swap this with a card in your own hand? \
                        \n \n  If so, press 1. Otherwise, 0 to draw a card. \n "
                     ))
            return r
        except ValueError:
            print(f"\n Please enter a valid number. Let's try again. \n")
            sleep(1)
        else:
            break


def present_swap_card_prompt() -> int:
    n = int(input("Which card would you like to replace?"))
    return n


def present_swap_results(sr, hand_index) -> None:
    print(
        f"You swapped discarded card {sr[1]} for a {sr[0]} at position {hand_index} in your hand."
    )
    sleep(2)


def present_card_index_error() -> None:
    print(
        f"\n Sorry - that card or position doesn't exist. Let's try again. \n")
    sleep(1)


def present_action_prompt() -> int:
    a = int(
        input("\n What actions would you like to take?  \
                                            \n \t 1. Use power on drawn card  \
                                            \n \t 2. Discard drawn card \
                                            \n \t 3. Swap drawn card with one in hand \
                                            \n \t 4. Call Cabo! \
                                            \n \t 5. End game  \
                                            \n \n \t Please respond with 1,2,3,4 \n \n"
             ))
    return a


def present_swap_draw_results(r, hand_index):
    print(
        f"{r[0].name} is now in position {hand_index} in your hand. {r[1].name} has been sent to the discard pile."
    )
    sleep(2)


def present_card_power_error() -> None:
    print(f"\n Sorry - your card does not have a power. Let's try again. \n")
    sleep(1)


def present_end_round(turn_count) -> None:
    print(
        f"\n \n \n --------------------------------------------------------\n \t \tThat concludes turn {turn_count}\n---------------------------------------------------------\n"
    )
    cls = lambda: print('\n' * 100)
    cls()
    sleep(2)


def present_intro():
    print("Welcome to Cabo!")
    name: str = input(f"Please tell me your name! \n")
    played_before: str = input(f"Have you played before? Enter Yes or No \n")
    played_before = played_before.lower()
    if played_before == 'yes':
        return True
    if played_before == 'no':
        print(f"/n Placeholder for Instructions \n")
        return False
    return name


def present_card_powers_string(card_obj) -> None:
    '''Prints a string to terminal of the power associated with the Card'''
    print(f"This top card has the ability to:{card_obj.return_card_powers()}"
         )  # TODO fix this to show strings)


def present_reveal_card(card_name, index_n):
    print(f"{card_name} is in position {index_n} in your hand.")
    sleep(4)


def present_transfer(source_card, dest_card) -> None:
    print(f"{source_card} was transferred to {dest_card}.")


def present_open_swap(source_index, dest_index, c1, c2):
    print(
        f"{c1} at position {source_index} was swapped with {c2} at position {dest_index} "
    )
    sleep(4)


def present_blind_swap(source_index, dest_index):
    print(
        f"Your card at position {source_index} was swapped with your opponents card at position {dest_index}."
    )
    sleep(4)


def present_open_swap_prompt():
    source_index = int(
        input(
            "Which of your cards would you like to swap? Please enter position number."
        ))
    dest_index = int(
        input(
            "Which of your opponents cards would you like to swap with? Please enter position number."
        ))
    return source_index, dest_index


def present_blind_swap_prompt():
    source_index = int(
        input(
            "Which of your cards would you like to swap? Please enter position number."
        ))
    dest_index = int(
        input(
            "Which of your opponents cards would you like to swap with? Please enter position number."
        ))
    return source_index, dest_index


def present_peek_self_prompt():
    peek_index = int(
        input(
            "Which of your own cards would you like to look at? Respond with position number: \n"
        ))
    return peek_index


def present_peek_card_prompt():
    peek_index = int(
        input(
            "Which of your opponents cards would you like to look at? Respond with position number: \n"
        ))
    return peek_index


def present_peek_card(card_name, index_n):
    print(f"{card_name} is in position {index_n} in your opponents hand.")
    sleep(4)


def present_draw_card_preview(card_obj) -> None:
    '''Prints to the terminal the name of the Stacks current card in index.'''
    print(f"\n You've drawn a {card_obj.name}.")


def print_hand_table(stack_obj, open_hand: bool = False) -> None:
    '''Returns a string containing a table of the masked set of cards in a hand -- using the tabulate table module as defined in tabulate().
            If open hand == False, it reveals the first two cards to the player. If open_hand == True, it shows all cards.
            '''
    hand: list[list[str]] = [["Position", "Card"]]
    cards: Card
    index = 1
    if not open_hand:
        for cards in stack_obj:
            if index < 3:
                hand.append([f"Position: {index}", cards.name])
                index += 1
            else:
                hand.append([f"Position: {index}", 'x'])
                index += 1
    else:
        for cards in stack_obj:
            hand.append([f"Position: {index}", cards.name])
            index += 1
    response = tabulate_hand(stack_obj, hand)
    print(response)


def tabulate_hand(stack_obj, hand: list[list[str]]) -> str:  # TODO
    '''Uses tabulate module to produce terminal formatted tables.'''
    table = tabulate(hand, tablefmt="fancy_grid", headers='firstrow')
    response = f"\n\n\n{stack_obj.name}: \n\n {table}"
    return response
